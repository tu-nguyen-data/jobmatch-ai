from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_match_score(
    candidate_text: str,
    offer_text: str,
) -> float:
    documents = [
        candidate_text,
        offer_text,
    ]

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
    )

    tfidf_matrix = vectorizer.fit_transform(documents)

    score = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2],
    )[0][0]

    return round(float(score) * 100, 2)

def calculate_match_scores(
    candidate_text: str,
    offer_texts: list[str],
) -> list[float]:
    if not offer_texts:
        return []

    documents = [
        candidate_text,
        *offer_texts,
    ]

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
    )

    tfidf_matrix = vectorizer.fit_transform(documents)

    candidate_vector = tfidf_matrix[0:1]
    offer_vectors = tfidf_matrix[1:]

    scores = cosine_similarity(
        candidate_vector,
        offer_vectors,
    )[0]

    return [
        round(float(score) * 100, 2)
        for score in scores
    ]