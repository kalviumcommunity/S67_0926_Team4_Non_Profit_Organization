from src.evaluation.evaluate import evaluate_dataset, evaluate_single


def test_evaluate_single():
    result = evaluate_single(
        "What does the grant support?",
        {
            "answer": "It supports shelter operations [Source 1].",
            "sources": [{"source_file": "grant.pdf", "page_number": 1}],
            "retrieved_chunks": 1,
        },
        expected_sources=[1],
    )

    assert result["citation_valid"] is True
    assert result["source_recall"] == 1.0


def test_evaluate_single_reference_answer():
    result = evaluate_single(
        "What is the grant amount?",
        {
            "answer": "The grant amount is $50,000 [Source 1].",
            "sources": [{"source_file": "grant.pdf", "page_number": 1}],
        },
        expected_answer="The grant amount is $50,000 [Source 1].",
    )

    assert result["reference_answer_match"] is True


def test_evaluate_dataset():
    def fake_ask(question):
        return {
            "answer": f"Answer for {question} [Source 1].",
            "sources": [{"source_file": "grant.pdf", "page_number": 1}],
            "retrieved_chunks": 1,
        }

    report = evaluate_dataset(
        [
            {"question": "Question one", "expected_sources": [1]},
            {"question": "Question two", "expected_sources": [1]},
        ],
        fake_ask,
    )

    assert report["total_questions"] == 2
    assert report["citation_valid_rate"] == 1.0
    assert report["average_source_recall"] == 1.0
