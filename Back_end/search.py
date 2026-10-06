from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma


embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)


vectorstore = Chroma(
    persist_directory="chroma_db",
    collection_name="donor_knowledge",
    embedding_function=embeddings
)


query = input("Ask something: ")


results = vectorstore.similarity_search_with_score(
    query,
    k=5
)


for doc, score in results:

    print("\n-------------------------")

    print("Score:", score)

    print("Source:", doc.metadata.get("source"))

    print("Type:", doc.metadata.get("type"))

    print("Content:")
    print(doc.page_content)