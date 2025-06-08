terraform {
  required_version = ">= 1.2"
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "genai-rag-aws-mlops/terraform.tfstate"
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