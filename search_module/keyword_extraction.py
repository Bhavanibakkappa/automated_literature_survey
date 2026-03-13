import re

def extract_keywords(text):

    # convert text to lowercase
    text = text.lower()

    # find all words
    words = re.findall(r'\b[a-z]+\b', text)

    # remove common words (stopwords)
    stopwords = [
        "the","is","and","in","to","of","for","a","an","this",
        "that","with","on","by","using","from","we","our"
    ]

    keywords = [word for word in words if word not in stopwords]

    # remove duplicates
    keywords = list(set(keywords))

    # return top keywords
    return keywords[:10]