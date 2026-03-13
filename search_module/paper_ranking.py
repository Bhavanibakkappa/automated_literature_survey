from sentence_transformers import SentenceTransformer, util

# load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def rank_papers(papers, query):

    ranked = []

    query_embedding = model.encode(query, convert_to_tensor=True)

    for paper in papers:

        text = (paper.get("title", "") + " " + str(paper.get("summary", "")))

        paper_embedding = model.encode(text, convert_to_tensor=True)

        score = util.cos_sim(query_embedding, paper_embedding).item()

        paper["score"] = score

        ranked.append(paper)

    # sort papers by similarity score
    ranked.sort(key=lambda x: x["score"], reverse=True)

    return ranked