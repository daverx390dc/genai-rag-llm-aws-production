terraform {
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "genai-rag-aws-mlops/prod.tfstate"
    region = var.aws_region
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "sagemaker_role_arn" {
  type = string
}

module "networking" {
  source = "../../modules/networking"
  env    = "prod"
}

module "storage" {
  source = "../../modules/storage"
  env    = "prod"
}

module "compute" {
  source              = "../../modules/compute"
  env                 = "prod"
  bedrock_model       = "anthropic.claude-v2"
  opensearch_endpoint = module.storage.vector_db.endpoint
  aws_region          = var.aws_region
}

module "ml" {
  source                       = "../../modules/ml"
  env                          = "prod"
  sagemaker_role_arn           = var.sagemaker_role_arn
  sm_pipeline_name             = "GenAIRAGPipeline-prod"
  sm_model_package_group_name  = "GenAIRAGModels-prod"
}