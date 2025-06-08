from fastapi import FastAPI
from api.routes.question_answering import router as qa_router

app = FastAPI(
    title="GenAI RAG Service",
    description="RAG API using AWS Bedrock & OpenSearch",
    version="1.0.0"
)
app.include_router(qa_router, prefix="/api")