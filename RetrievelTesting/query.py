def query_search_by_similarity(tx, query_text, embedding_model, top_k = 5):

    query_embedding = embedding_model.embed_query(query_text)

    query = """
        CALL db.index.vector.queryNodes('GeminiEmbeddingIndex', $top_k, $query_embedding)
        YIELD node, score
        MATCH (node)-[:FROM]-()-[:OF]-(o:Opinion)-[:HAS_OPINION]-(c:Case)-[d:DECIDED_IN]-(court:Court)
        WHERE d.Status IS NULL
        RETURN DISTINCT c.WestLawCaseName AS Case, c.FiledDate AS FiledDate, score, court.Name AS CourtName, o.Summary AS Summary, c.pagerank AS CasePageRank, court.pagerank AS CourtPageRank
        ORDER BY score DESC
    """

    return tx.run(query, top_k = top_k*5, query_embedding = query_embedding).to_df()


def query_get_citation(tx, cases):

    query = """
        MATCH (c:Case)-[:CITED]->(cited:Case)-[:HAS_OPINION]-(o:Opinion)
        WHERE c.WestLawCaseName IN $cases
        RETURN DISTINCT cited.WestLawCaseName AS Case, cited.FiledDate AS FiledDate, cited.pagerank AS CasePageRank, o.Summary AS Summary
        ORDER BY CasePageRank DESC
    """

    return tx.run(query, cases = cases).to_df()