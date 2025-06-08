import os
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_aws.embeddings import BedrockEmbeddings
from langchain.vectorstores import OpenSearch
from opensearchpy import OpenSearch as OSClient

load_dotenv()

S3_DOC_DIR = os.getenv("DOC_LOCAL_PATH", "docs")


def load_documents(doc_dir: str):
    docs = []
    for fname in os.listdir(doc_dir):
        path = os.path.join(doc_dir, fname)
        if fname.lower().endswith(".pdf"):
            loader = PyPDFLoader(path)
        elif fname.lower().endswith(".txt"):
            loader = TextLoader(path)
        else:
            continue
        for d in loader.load():
            d.metadata["source"] = fname
            docs.append(d)
    return docs


def chunk_documents(documents, size=500, overlap=50):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=size,
        chunk_overlap=overlap
    )
    return splitter.split_documents(documents)


def main():
    print("Loading documents...")
    docs = load_documents(S3_DOC_DIR)
    if not docs:
        print("No documents found in {S3_DOC_DIR}")
        return

    print(f"Chunking {len(docs)} docs...")
    chunks = chunk_documents(docs)

    print(f"Embedding {len(chunks)} chunks...")
    embeddings = BedrockEmbeddings(
        region_name=os.getenv("AWS_DEFAULT_REGION"),
        model_id=os.getenv("BEDROCK_EMBEDDINGS_MODEL_ID")
    )

    print("Connecting to OpenSearch...")
    client = OSClient(
        hosts=[os.getenv("OPENSEARCH_ENDPOINT")],
        http_auth=(os.getenv("AWS_ACCESS_KEY_ID"), os.getenv("AWS_SECRET_ACCESS_KEY")),
        use_ssl=True,
        verify_certs=True
    )

    vectorstore = OpenSearch.from_documents(
        documents=chunks,
        embeddings=embeddings,
        index_name=os.getenv("OPENSEARCH_INDEX"),
        client=client
    )
    print("Indexing complete.")


if __name__ == "__main__":
    main()