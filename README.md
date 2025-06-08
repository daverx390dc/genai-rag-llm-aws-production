# GenAI RAG AWS MLOps

## Setup

1. Copy `.env.example` → `.env` and fill in values:
   - AWS credentials (or use IAM role)
   - `BEDROCK_EMBEDDINGS_MODEL_ID`, `BEDROCK_LLM_MODEL_ID`
   - `OPENSEARCH_ENDPOINT`, `OPENSEARCH_INDEX`
   - `SM_PIPELINE_NAME`, `SM_PIPELINE_ROLE_ARN`, `SM_MODEL_PACKAGE_GROUP`
   - `S3_ARTIFACT_BUCKET`, `PROCESSOR_IMAGE_URI`, `TRAINING_IMAGE_URI`

2. Provision infra (dev):
   ```bash
   cd infra/terraform/environments/dev
   terraform init
   terraform apply -auto-approve