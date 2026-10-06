import os
import pandas as pd

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader
)


DATA_DIR = "data"
VECTOR_DB_DIR = "chroma_db"


# --------------------------------------------------
# 1. Load CSV
# --------------------------------------------------

def load_csv(path):
    df = pd.read_csv(path)

    documents = []

    for _, row in df.iterrows():

        # Don't put sensitive identifiers into searchable text
        text = f"""
        Donor age group: {row['age_group']}
        Gender: {row['gender']}
        Country: {row['country']}
        Donation type: {row['donation_type']}
        Donation amount: {row['donation_amount']}
        Donation date: {row['donation_date']}
        Payment method: {row['payment_method']}
        Newsletter opt-in: {row['newsletter_opt_in']}
        Referral channel: {row['referral_channel']}
        Sector: {row['sector']}
        Campaign: {row['campaign']}
        """

        metadata = {
            "source": path,
            "type": "csv",
            "donor_id": row["donor_id"],
            "country": row["country"],
            "campaign": row["campaign"],
            "donation_type": row["donation_type"],
        }

        documents.append(
            Document(
                page_content=text.strip(),
                metadata=metadata
            )
        )

    return documents


# --------------------------------------------------
# 2. Load PDF
# --------------------------------------------------

def load_pdf(path):
    loader = PyPDFLoader(path)

    documents = loader.load()

    for doc in documents:
        doc.metadata["type"] = "pdf"
        doc.metadata["source"] = path

    return documents


# --------------------------------------------------
# 3. Load TXT
# --------------------------------------------------

def load_txt(path):
    loader = TextLoader(path)

    documents = loader.load()

    for doc in documents:
        doc.metadata["type"] = "txt"
        doc.metadata["source"] = path

    return documents


# --------------------------------------------------
# 4. Load DOCX
# --------------------------------------------------

def load_docx(path):
    loader = Docx2txtLoader(path)

    documents = loader.load()

    for doc in documents:
        doc.metadata["type"] = "docx"
        doc.metadata["source"] = path

    return documents


# --------------------------------------------------
# 5. Load everything
# --------------------------------------------------

def load_all_data():

    documents = []

    # CSV
    csv_path = os.path.join(DATA_DIR, "donors.csv")

    if os.path.exists(csv_path):
        documents.extend(load_csv(csv_path))

    # Other files
    for root, dirs, files in os.walk(DATA_DIR):

        for filename in files:

            path = os.path.join(root, filename)

            if filename.endswith(".pdf"):
                documents.extend(load_pdf(path))

            elif filename.endswith(".txt"):
                documents.extend(load_txt(path))

            elif filename.endswith(".docx"):
                documents.extend(load_docx(path))

    return documents


def run_indexing(data_dir=DATA_DIR, vector_db_dir=VECTOR_DB_DIR):
    documents = load_all_data()
    print("Documents loaded:", len(documents))

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    chunks = text_splitter.split_documents(documents)
    print("Chunks created:", len(chunks))

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=vector_db_dir,
        collection_name="donor_knowledge"
    )

    print("Indexing completed.")
    return vectorstore


if __name__ == "__main__":
    run_indexing()