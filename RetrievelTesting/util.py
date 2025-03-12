import os 
from neo4j import GraphDatabase
from typing import List
import polars as pl
from google import genai
from query import query_search_by_similarity

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
        self.top_k = 5
        self.driver = driver

    def search_similar_cases(self, text, embedder=gemini_embedder):

        with driver.session() as session:
            df = pl.from_pandas(session.execute_read(query_search_by_similarity, text, embedder, self.top_k))
            
            df = df.group_by(["Case", "FiledDate", "CourtName"]).max().sort("score", descending = True).top_k(self.top_k, by = "score")

        return df

