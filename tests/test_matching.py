from app.services.matching import calculate_match_score


def test_related_offer_scores_higher_than_unrelated_offer():
    candidate_text = "Python SQL Power BI data analysis"

    related_offer = (
        "Recherche alternant Data Analyst "
        "avec Python SQL et Power BI"
    )

    unrelated_offer = (
        "Développeur Java Spring Boot microservices"
    )

    related_score = calculate_match_score(
        candidate_text,
        related_offer,
    )

    unrelated_score = calculate_match_score(
        candidate_text,
        unrelated_offer,
    )

    assert related_score > unrelated_score


def test_match_score_is_between_zero_and_one_hundred():
    score = calculate_match_score(
        "Python SQL Power BI",
        "Python SQL data analysis",
    )

    assert 0 <= score <= 100