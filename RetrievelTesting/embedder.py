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

    def search_similar_cases(self, text, top_k, embedder=gemini_embedder, include_citation = False, similarity_weight = 0, citation_weight = 0, court_weight = 0):

        with driver.session() as session:

            df = pl.from_pandas(session.execute_read(query_search_by_similarity, text, embedder, top_k))

            df = df.group_by(["Case", "FiledDate", "CourtName"]).max().sort("score", descending = True).top_k(top_k, by = "score")

            if include_citation:
                df_cited = pl.from_pandas(session.execute_read(query_get_citation, df["Case"].to_list())).top_k(top_k, by = "CasePageRank")

        return df

