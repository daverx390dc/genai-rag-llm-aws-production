import os
import boto3
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langchain_aws.embeddings import BedrockEmbeddings
from langchain_aws.llms import Bedrock
from langchain.vectorstores import OpenSearch
from langchain.chains import RetrievalQA
from opensearchpy import OpenSearch as OSClient

load_index = None

class QueryRequest(BaseModel):
    question: str

router = APIRouter()

@router.post("/query")
async def query_rag(request: QueryRequest):
    # Initialize embeddings
    embeddings = BedrockEmbeddings(
        region_name=os.getenv("AWS_DEFAULT_REGION"),
        model_id=os.getenv("BEDROCK_EMBEDDINGS_MODEL_ID")
    )

    # Connect to OpenSearch
    os_host = os.getenv("OPENSEARCH_ENDPOINT")
    client = OSClient(
        hosts=[os_host],
        http_auth=(os.getenv("AWS_ACCESS_KEY_ID"), os.getenv("AWS_SECRET_ACCESS_KEY")),
        use_ssl=True,
        verify_certs=True
    )

    # Load vectorstore
    try:
        vectorstore = OpenSearch.from_existing_index(
            index_name=os.getenv("OPENSEARCH_INDEX"),
            embeddings=embeddings,
            client=client
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to index: {e}")

    retriever = vectorstore.as_retriever()

    # Initialize Bedrock LLM
    bedrock_client = boto3.client(
        service_name="bedrock-runtime",
        region_name=os.getenv("AWS_DEFAULT_REGION")
    )
    llm = Bedrock(
        client=bedrock_client,
        model_id=os.getenv("BEDROCK_LLM_MODEL_ID"),
        temperature=0.0
    )

    # Build and run RAG chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
    result = qa_chain.run(request.question)

    # Collect sources
    sources = [doc.metadata.get("source") for doc in result.source_documents if doc.metadata.get("source")]

    return {"answer": result.result, "sources": sources}