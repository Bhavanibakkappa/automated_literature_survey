import requests
import time

def search_semantic_scholar(query, max_results=25):

    url = "https://api.semanticscholar.org/graph/v1/paper/search"

    params = {
        "query": query,
        "limit": max_results,
        "fields": "title,authors,year,abstract,url,venue,openAccessPdf"
    }

    print("Sending request to Semantic Scholar...")

    response = requests.get(url, params=params)

    # Handle rate limit
    if response.status_code == 429:
        print("Rate limit reached. Waiting 60 seconds...")
        time.sleep(60)

        response = requests.get(url, params=params)

    print("Semantic Scholar status:", response.status_code)

    data = response.json()

    papers = []

    for paper in data.get("data", []):

        pdf = None

        if paper.get("openAccessPdf"):
            pdf = paper["openAccessPdf"]["url"]

        papers.append({
            "title": paper.get("title"),
            "authors": [a["name"] for a in paper.get("authors", [])],
            "summary": paper.get("abstract"),
            "pdf_url": pdf if pdf else paper.get("url"),
            "venue": paper.get("venue"),
            "source": "semantic_scholar"
        })

    print("Semantic Scholar returned:", len(papers), "papers")

    # IMPORTANT: avoid hitting rate limit again
    time.sleep(2)

    return papers