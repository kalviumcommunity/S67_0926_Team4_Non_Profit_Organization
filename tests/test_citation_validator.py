from src.evaluation.citation_validator import validate_citations


def _sources():
    return [
        {"source_file": "grant.pdf", "page_number": 1},
        {"source_file": "agreement.pdf", "page_number": 2},
    ]


def test_valid_citations():
    result = validate_citations(
        "The grant supports shelter operations [Source 1].",
        _sources(),
    )
    assert result["valid"] is True
    assert result["cited_sources"] == [1]


def test_invalid_citation_number():
    result = validate_citations(
        "The grant supports shelter operations [Source 3].",
        _sources(),
    )
    assert result["valid"] is False
    assert result["invalid_citations"] == [3]


def test_no_information_response_is_valid():
    result = validate_citations(
        "I could not find enough information in the provided documents.",
        [],
    )
    assert result["valid"] is True
    assert result["no_information"] is True


def test_missing_citation_is_invalid():
    result = validate_citations(
        "The grant supports shelter operations.",
        _sources(),
    )
    assert result["valid"] is False


def test_multiple_valid_citations():
    result = validate_citations(
        "The agreement requires reporting [Source 1] and donor approval [Source 2].",
        _sources(),
    )
    assert result["valid"] is True
    assert result["cited_sources"] == [1, 2]
