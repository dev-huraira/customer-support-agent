from dotenv import load_dotenv
load_dotenv()

from rag.vector_store import vector_store

RELEVANCE_TEST_CASES = [
    {"query": "why is the app so laggy", "expected_title": "Slow loading times"},
    {"query": "I forgot my login credentials", "expected_title": "Resetting your password"},
    {"query": "how do I add extra security to my account", "expected_title": "Two-factor authentication setup"},
    {"query": "the app keeps closing right after I open it", "expected_title": "App crashes on startup"},
]

IRRELEVANT_QUERIES = [
    "what's the weather like today",
    "can you recommend a good pizza place",
]


def run_relevance_tests():
    print("=== Relevance Tests (paraphrased queries) ===\n")
    passed = 0
    for case in RELEVANCE_TEST_CASES:
        results = vector_store.similarity_search_with_score(case["query"], k=1)
        top_doc, score = results[0]
        top_title = top_doc.metadata.get("title")
        status = "PASS" if top_title == case["expected_title"] else "FAIL"
        passed += status == "PASS"

        print(f"[{status}] Query: {case['query']!r}")
        print(f"       Expected: {case['expected_title']} | Got: {top_title} (score: {score:.4f})\n")

    print(f"{passed}/{len(RELEVANCE_TEST_CASES)} relevance tests passed.\n")


def run_irrelevance_checks():
    print("=== Irrelevant Query Checks ===\n")
    for query in IRRELEVANT_QUERIES:
        results = vector_store.similarity_search_with_score(query, k=1)
        top_doc, score = results[0]
        print(f"Query: {query!r}")
        print(f"       Closest (unrelated) match: {top_doc.metadata.get('title')} (score: {score:.4f})\n")


if __name__ == "__main__":
    run_relevance_tests()
    run_irrelevance_checks()