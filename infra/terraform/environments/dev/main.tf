terraform {
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "genai-rag-aws-mlops/dev.tfstate"
    region = var.aws_region
  }
}
provider "aws" { region = var.aws_region }

variable "aws_region"        { default = "us-east-1" }
variable "sagemaker_role_arn" { type = string }

module "networking" {
  source = "../../modules/networking"
  env    = "dev"
}
module "storage" {
  source = "../../modules/storage"
  env    = "dev"
}
module "compute" {
  source              = "../../modules/compute"
  env                 = "dev"
  bedrock_model       = "anthropic.claude-v2"
  opensearch_endpoint = module.storage.vector_db.endpoint
  aws_region          = var.aws_region
}
module "ml" {
  source                       = "../../modules/ml"
  env                          = "dev"
  sagemaker_role_arn           = var.sagemaker_role_arn
  sm_pipeline_name             = "GenAIRAGPipeline-dev"
  sm_model_package_group_name  = "GenAIRAGModels-dev"
}