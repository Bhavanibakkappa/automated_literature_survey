from search_module.arxiv_search import search_arxiv
from search_module.semantic_search import search_semantic_scholar


def search_all_papers(query):

    print("Searching arXiv...")
    arxiv_papers = search_arxiv(query, max_results=25)

    print("Searching Semantic Scholar...")
    semantic_papers = search_semantic_scholar(query, max_results=25)

    # merge results
    all_papers = arxiv_papers + semantic_papers

    # remove duplicates using title
    unique = {}
    for paper in all_papers:

        title = paper["title"].lower()

        if title not in unique:
            unique[title] = paper

    final_papers = list(unique.values())

    print(f"\narXiv papers found: {len(arxiv_papers)}")
    print(f"Semantic Scholar papers found: {len(semantic_papers)}")
    print(f"Unique papers after merge: {len(final_papers)}\n")

    return final_papers