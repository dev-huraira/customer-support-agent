from rag.vector_store import vector_store

RELEVANCE_THRESHOLD = 0.40

RELEVANCE_CASES = [
    ("why is the app so laggy", "Slow loading times"),
    ("I forgot my login credentials", "Resetting your password"),
    ("how do I add extra security to my account", "Two-factor authentication setup"),
    ("the app keeps closing right after I open it", "App crashes on startup"),
]

IRRELEVANT_QUERIES = [
    "what's the weather like today",
    "can you recommend a good pizza place",
]


def test_relevant_queries_match_expected_article():
    for query, expected_title in RELEVANCE_CASES:
        results = vector_store.similarity_search_with_score(query, k=1)
        top_doc, score = results[0]
        assert top_doc.metadata.get("title") == expected_title
        assert score < RELEVANCE_THRESHOLD


def test_irrelevant_queries_exceed_threshold():
    for query in IRRELEVANT_QUERIES:
        results = vector_store.similarity_search_with_score(query, k=1)
        _, score = results[0]
        assert score >= RELEVANCE_THRESHOLD