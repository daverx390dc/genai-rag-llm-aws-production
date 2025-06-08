variable "env" { type = string }
variable "bedrock_model" { type = string }
variable "opensearch_endpoint" { type = string }
variable "aws_region" { type = string }

resource "aws_ecr_repository" "api" {
  name                 = "genai-rag-api-${var.env}"
  image_tag_mutability = "MUTABLE"
}

resource "aws_ecs_cluster" "cluster" {
  name = "genai-rag-cluster-${var.env}"
}

resource "aws_iam_role" "ecs_task_execution" {
  name = "ecs-task-exec-role-${var.env}"
  assume_role_policy = data.aws_iam_policy_document.ecs_task_execution.json
}

data "aws_iam_policy_document" "ecs_task_execution" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_ecs_task_definition" "api_task" {
  family                   = "genai-rag-task-${var.env}"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "512"
  memory                   = "1024"
  execution_role_arn       = aws_iam_role.ecs_task_execution.arn

  container_definitions = jsonencode([
    {
      name       = "api"
      image      = "${aws_ecr_repository.api.repository_url}:latest"
      portMappings = [{ containerPort = 8000 }]
      environment = [
        { name = "BEDROCK_LLM_MODEL_ID", value = var.bedrock_model },
        { name = "OPENSEARCH_ENDPOINT",    value = var.opensearch_endpoint }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = "/ecs/genai-rag-${var.env}"
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "api"
        }
      }
    }
  ])
}