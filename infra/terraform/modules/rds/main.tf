terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}

resource "aws_db_subnet_group" "this" {
  name       = "${var.identifier}-subnet-group"
  subnet_ids = var.subnet_ids
  tags       = var.tags
}

resource "aws_rds_cluster" "this" {
  cluster_identifier      = var.identifier
  engine                  = "aurora-postgresql"
  engine_mode             = "provisioned"
  engine_version          = var.engine_version
  database_name           = var.database_name
  master_username         = var.master_username
  master_password         = var.master_password
  port                    = 5432
  db_subnet_group_name    = aws_db_subnet_group.this.name
  vpc_security_group_ids  = var.security_group_ids
  storage_encrypted       = true
  backup_retention_period = var.backup_retention_days
  preferred_backup_window = var.preferred_backup_window
  copy_tags_to_snapshot   = true
  deletion_protection     = var.deletion_protection

  serverlessv2_scaling_configuration {
    max_capacity = var.max_capacity
    min_capacity = var.min_capacity
  }

  tags = var.tags
}

resource "aws_rds_cluster_instance" "this" {
  count              = var.instance_count
  identifier         = "${var.identifier}-${count.index}"
  cluster_identifier = aws_rds_cluster.this.id
  instance_class     = var.instance_class
  engine             = aws_rds_cluster.this.engine
  engine_version     = aws_rds_cluster.this.engine_version
  publicly_accessible = false
  db_subnet_group_name = aws_db_subnet_group.this.name
  tags               = var.tags
}

output "cluster_endpoint" {
  value = aws_rds_cluster.this.endpoint
}

output "cluster_reader_endpoint" {
  value = aws_rds_cluster.this.reader_endpoint
}

output "cluster_arn" {
  value = aws_rds_cluster.this.arn
}
