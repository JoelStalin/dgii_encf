terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}

resource "aws_secretsmanager_secret" "this" {
  for_each = var.secrets

  name        = each.value.name
  description = each.value.description
  kms_key_id  = var.kms_key_id
  tags        = var.tags
}

resource "aws_secretsmanager_secret_version" "this" {
  for_each = var.secrets

  secret_id     = aws_secretsmanager_secret.this[each.key].id
  secret_string = jsonencode(each.value.value)
}

output "secret_arns" {
  value = { for key, secret in aws_secretsmanager_secret.this : key => secret.arn }
}
