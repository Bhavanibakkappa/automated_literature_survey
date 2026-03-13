from search_module.keyword_extraction import extract_keywords
from search_module.paper_search import search_all_papers
from search_module.seed_paper_search import (
    get_paper_id_from_url,
    get_similar_papers,
    get_citation_papers
)
from search_module.paper_ranking import rank_papers
from search_module.download_papers import download_papers


# Step 1: User input
title = input("Enter the project title: ")
abstract = input("Enter the project abstract: ")
paper_link = input("Enter one relevant paper link: ")

print("\n------ User Input Received ------")
print("Title:", title)
print("Abstract:", abstract)
print("Relevant Paper:", paper_link)


# Step 2: Keyword extraction
combined_text = title + " " + abstract
keywords = extract_keywords(combined_text)

print("\nExtracted Keywords:", keywords)


# Step 3: Paper search
query = " ".join(keywords)

print("\nSearching research papers...\n")

papers = search_all_papers(query)

print(f"\nInitial papers found: {len(papers)}")


# Step 4: Seed paper retrieval
paper_id = get_paper_id_from_url(paper_link)

print("\nFetching similar papers from seed paper...")
similar_papers = get_similar_papers(paper_id)

print("Fetching citation papers from seed paper...")
citation_papers = get_citation_papers(paper_id)


# Step 5: Merge results
papers = papers + similar_papers + citation_papers

print("\nTotal papers after seed-paper expansion:", len(papers))


# Step 6: Remove duplicates
seen_titles = set()
unique_papers = []

for p in papers:
    title = p.get("title", "").lower()

    if title not in seen_titles:
        unique_papers.append(p)
        seen_titles.add(title)

papers = unique_papers

print("Unique papers after duplicate removal:", len(papers))


# Step 7: Ranking papers
print("\nRanking papers by relevance...")

papers = rank_papers(papers, combined_text)

print("Ranking completed.")


# Step 8: Display top papers
print("\nTop ranked papers:\n")

for i, paper in enumerate(papers[:50]):

    print(f"Paper {i+1}")
    print("Title:", paper.get("title"))
    print("Authors:", paper.get("authors"))

    if paper.get("venue"):
        print("Venue:", paper.get("venue"))

    print("Score:", round(paper.get("score", 0), 4))
    print("Source:", paper.get("source"))
    print("Link:", paper.get("pdf_url"))
    print()


# Step 9: Download top papers
print("\nDownloading top papers...\n")

download_papers(papers[:50])

print("Download completed.")