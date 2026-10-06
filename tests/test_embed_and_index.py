from src.embeddings.embed_and_index import embed_chunks, index_chunks

class FakeResponse:
    def __init__(self, vectors):
        self.data = [type("Item", (), {"embedding": v}) for v in vectors]

class FakeClient:
    class embeddings:
        @staticmethod
        def create(model, input):
            return FakeResponse([[float(len(x)), 1.0, 2.0] for x in input])

class FakeIndex:
    def __init__(self):
        self.calls = []
    def upsert(self, **kwargs):
        self.calls.append(kwargs)

def chunks():
    return [
        {"document_id":"doc-1","chunk_id":"doc-1-chunk-0","page_number":1,
         "section":"Eligibility","text":"Eligible animal welfare organizations.",
         "source_file":"guidelines.json"},
        {"document_id":"doc-1","chunk_id":"doc-1-chunk-1","page_number":2,
         "section":"Funding","text":"Funding may support veterinary care.",
         "source_file":"guidelines.json"},
    ]

def test_embed_chunks():
    result = embed_chunks(chunks(), client=FakeClient(), model="test-model")
    assert len(result) == 2
    assert result[0]["chunk_id"] == "doc-1-chunk-0"
    assert result[0]["section"] == "Eligibility"
    assert result[0]["embedding_model"] == "test-model"

def test_index_chunks():
    embedded = embed_chunks(chunks(), client=FakeClient(), model="test-model")
    index = FakeIndex()
    assert index_chunks(embedded, index=index, namespace="folio-test") == 2
    assert len(index.calls) == 1
    assert index.calls[0]["namespace"] == "folio-test"
    assert len(index.calls[0]["vectors"]) == 2

def test_empty():
    assert embed_chunks([], client=FakeClient()) == []
    assert index_chunks([], index=FakeIndex()) == 0
