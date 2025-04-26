import os 
from neo4j import GraphDatabase
from typing import List
import polars as pl
from google import genai
from query import query_search_by_similarity, query_get_citation

##===================================
## Initialize Database and Embedder
##===================================

## Database Connections
URI = os.environ["AURA_URI"]
AUTH = (os.environ["AURA_user"], os.environ["AURA_password"])

driver = GraphDatabase.driver(URI, auth=AUTH)

class Gemini_Embeddings:
    def __init__(self):
        self.model = genai.Client(api_key=os.environ["GEMINI_API"])
            
    def embed_query(self, query: str) -> List[float]:
        result = self.model.models.embed_content(
            model="text-embedding-004",
            contents=query)

        return list(result.embeddings[0])[0][1]
    
gemini_embedder = Gemini_Embeddings()

class Retriever:
    def __init__(self, embedding_model=gemini_embedder, driver=driver):
        self.embedding_model = embedding_model
        self.driver = driver

    def search_similar_cases(self, text, top_k, similarity_weight, court_weight, case_weight, embedder=gemini_embedder):

        with self.driver.session() as session:

            df = pl.from_pandas(session.execute_read(query_search_by_similarity, text, embedder, top_k))

            df = df.filter( pl.col("OpinionType") != "040dissent" ).with_columns(
                (pl.col("TextSimilarity") - pl.col("TextSimilarity").min())/((pl.col("TextSimilarity").max() - pl.col("TextSimilarity").min())),
                (pl.col("CasePageRank") - pl.col("CasePageRank").min())/((pl.col("CasePageRank").max() - pl.col("CasePageRank").min())),
                (pl.col("CourtPageRank") - pl.col("CourtPageRank").min())/((pl.col("CourtPageRank").max() - pl.col("CourtPageRank").min()))
            ).with_columns(
                pl.struct(["TextSimilarity", "CasePageRank", "CourtPageRank"]).map_elements(lambda x: similarity_weight*x["TextSimilarity"] + court_weight*x["CourtPageRank"] + case_weight*x["CasePageRank"]).alias("FinalScore")
            ).group_by(["Case", "FiledDate", "CourtName"]).max().sort("FinalScore", descending = True).top_k(top_k, by = "FinalScore")
        
        return df
    
    # TODO: Write retrieve cited cases
    def get_cited_cases(self, cases, top_k):

        with self.driver.session() as session:

            df_cited = pl.from_pandas(session.execute_read(query_get_citation, cases)).filter( pl.col("OpinionType") != "040dissent" ).top_k(top_k, by = "CasePageRank")

            return df_cited