import requests
import time


def get_paper_id_from_url(seed_url):

    # Example:
    # https://www.semanticscholar.org/paper/abc123
    # Extract the last part

    parts = seed_url.strip().split("/")

    return parts[-1]


def get_similar_papers(paper_id, max_results=10):

    url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}/related"

    params = {
        "fields": "title,authors,abstract,url,venue,openAccessPdf",
        "limit": max_results
    }

    response = requests.get(url, params=params)

    if response.status_code == 429:
        print("Rate limit reached. Waiting 60 seconds...")
        time.sleep(60)
        response = requests.get(url, params=params)

    data = response.json()

    papers = []

    for item in data.get("data", []):

        paper = item.get("paper")

        if not paper:
            continue

        pdf = None
        if paper.get("openAccessPdf"):
            pdf = paper["openAccessPdf"]["url"]

        papers.append({
            "title": paper.get("title"),
            "authors": [a["name"] for a in paper.get("authors", [])],
            "summary": paper.get("abstract"),
            "pdf_url": pdf if pdf else paper.get("url"),
            "venue": paper.get("venue"),
            "source": "semantic_similar"
        })

    return papers


def get_citation_papers(paper_id, max_results=10):

    url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}/citations"

    params = {
        "fields": "title,authors,abstract,url,venue,openAccessPdf",
        "limit": max_results
    }

    response = requests.get(url, params=params)

    if response.status_code == 429:
        print("Rate limit reached. Waiting 60 seconds...")
        time.sleep(60)
        response = requests.get(url, params=params)

    data = response.json()

    papers = []

    for item in data.get("data", []):

        paper = item.get("citingPaper")

        if not paper:
            continue

        pdf = None
        if paper.get("openAccessPdf"):
            pdf = paper["openAccessPdf"]["url"]

        papers.append({
            "title": paper.get("title"),
            "authors": [a["name"] for a in paper.get("authors", [])],
            "summary": paper.get("abstract"),
            "pdf_url": pdf if pdf else paper.get("url"),
            "venue": paper.get("venue"),
            "source": "semantic_citations"
        })

    return papers