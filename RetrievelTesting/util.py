import os 
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from neo4j import GraphDatabase
from typing import List
import polars as pl
from google import genai
import time

load_dotenv()

URI = os.environ["AURA_URI"]
AUTH = (os.environ["AURA_user"], os.environ["AURA_password"])

#URI = "bolt://localhost:7687"
#AUTH = ("neo4j", "fairusecases")

driver = GraphDatabase.driver(URI, auth=AUTH)

class Mini_Embeddings:
    def __init__(self):
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2', token = os.environ["HUGGING_FACE"])
            
    def embed_query(self, query: str) -> List[float]:
        return self.model.encode([query])[0]
    
class Gemini_Embeddings:
    def __init__(self):
        self.model = genai.Client(api_key=os.environ["GEMINI_API"])
            
    def embed_query(self, query: str) -> List[float]:
        result = self.model.models.embed_content(
            model="text-embedding-004",
            contents=query)

        return list(result.embeddings[0])[0][1]
   
mini_embedder = Mini_Embeddings()
gemini_embedder = Gemini_Embeddings()

def query_search_similar_cases(tx, query_text, embedding_model, top_k=5):

    query_embedding = embedding_model.embed_query(query_text)

    query = """
    CALL db.index.vector.queryNodes('GeminiEmbeddingIndex', $top_k, $query_embedding)
    YIELD node, score
    MATCH (node)-[:FROM]-()-[:OF]-(o:Opinion)-[:HAS_OPINION]-(c:Case)-[:DECIDED_IN]-(court:Court)
    RETURN DISTINCT c.WestLawCaseName as Case, c.FiledDate AS FiledDate, score, court.Name AS CourtName
    ORDER BY score DESC
    """
    
    return tx.run(query, top_k = top_k*3, query_embedding = query_embedding).to_df()

def search_similar_cases(text, top_k=5, embedder = gemini_embedder):

    with driver.session() as session:
        df = pl.from_pandas(session.execute_read(query_search_similar_cases, text, embedder)).group_by(["Case", "FiledDate", "CourtName"]).max().sort("score", descending = True).top_k(top_k, by = "score")

    return df
