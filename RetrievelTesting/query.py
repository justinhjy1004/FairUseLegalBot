def query_search_by_similarity(tx, query_text, embedding_model, top_k = 5):

    query_embedding = embedding_model.embed_query(query_text)

    query = """
        CALL db.index.vector.queryNodes('GeminiEmbeddingIndex', $top_k, $query_embedding)
        YIELD node, score
        MATCH (node)-[:FROM]-()-[:OF]-(o:Opinion)-[:HAS_OPINION]-(c:Case)-[:DECIDED_IN]-(court:Court)
        RETURN DISTINCT c.WestLawCaseName as Case, c.FiledDate AS FiledDate, score, court.Name AS CourtName
        ORDER BY score DESC
    """
    
    return tx.run(query, top_k = top_k*3, query_embedding = query_embedding).to_df()