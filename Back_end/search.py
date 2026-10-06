from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma


def get_vectorstore(persist_directory="chroma_db", collection_name="donor_knowledge"):
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )
    return Chroma(
        persist_directory=persist_directory,
        collection_name=collection_name,
        embedding_function=embeddings
    )


def search_donor_knowledge(query: str, k: int = 5):
    vectorstore = get_vectorstore()
    return vectorstore.similarity_search_with_score(query, k=k)


if __name__ == "__main__":
    query = input("Ask something: ")
    results = search_donor_knowledge(query, k=5)
    for doc, score in results:
        print("\n-------------------------")
        print("Score:", score)
        print("Source:", doc.metadata.get("source"))
        print("Type:", doc.metadata.get("type"))
        print("Content:")
        print(doc.page_content)