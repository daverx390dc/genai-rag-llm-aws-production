variable "env" { type = string }

resource "aws_s3_bucket" "docs" {
  bucket = "genai-rag-docs-${var.env}"
  acl    = "private"
  tags   = { Name = "genai-rag-docs-${var.env}" }
}

resource "aws_opensearch_domain" "vector_db" {
  domain_name    = "vector-db-${var.env}"
  engine_version = "OpenSearch_2.3"

  cluster_config {
    instance_type  = "t3.small.search"
    instance_count = 1
  }
  ebs_options {
    ebs_enabled = true
    volume_size = 10
  }
  advanced_options = {
    "rest.action.multi.allow_explicit_index" = "true"
  }
  tags = { Name = "vector-db-${var.env}" }
}