variable "env"                          { type = string }
variable "sagemaker_role_arn"           { type = string }
variable "sm_pipeline_name"             { type = string }
variable "sm_model_package_group_name"  { type = string }

resource "aws_sagemaker_pipeline" "rag_pipeline" {
  pipeline_name = var.sm_pipeline_name
  role_arn      = var.sagemaker_role_arn
  definition    = file("${path.module}/rag_pipeline_definition.json")
}

resource "aws_sagemaker_model_package_group" "rag_group" {
  model_package_group_name = var.sm_model_package_group_name
}