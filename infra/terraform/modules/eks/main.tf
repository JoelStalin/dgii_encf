terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}

data "aws_iam_policy_document" "cluster_assume" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["eks.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "cluster" {
  name               = "${var.name}-cluster"
  assume_role_policy = data.aws_iam_policy_document.cluster_assume.json
  tags               = var.tags
}

resource "aws_iam_role_policy_attachment" "cluster" {
  role       = aws_iam_role.cluster.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
}

resource "aws_security_group" "cluster" {
  name        = "${var.name}-cluster"
  description = "Security group del control plane"
  vpc_id      = var.vpc_id
  tags        = merge(var.tags, { Name = "${var.name}-cluster" })
}

resource "aws_eks_cluster" "this" {
  name     = var.name
  role_arn = aws_iam_role.cluster.arn

  version = var.version

  vpc_config {
    subnet_ids              = var.subnet_ids
    endpoint_private_access = true
    endpoint_public_access  = var.enable_public_endpoint
    security_group_ids      = [aws_security_group.cluster.id]
  }

  enabled_cluster_log_types = ["api", "audit", "authenticator", "controllerManager", "scheduler"]

  tags = var.tags
}

data "aws_iam_policy_document" "node_assume" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "node" {
  name               = "${var.name}-node"
  assume_role_policy = data.aws_iam_policy_document.node_assume.json
  tags               = var.tags
}

resource "aws_iam_role_policy_attachment" "node_worker" {
  role       = aws_iam_role.node.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
}

resource "aws_iam_role_policy_attachment" "node_cni" {
  role       = aws_iam_role.node.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
}

resource "aws_iam_role_policy_attachment" "node_registry" {
  role       = aws_iam_role.node.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

resource "aws_eks_node_group" "default" {
  cluster_name    = aws_eks_cluster.this.name
  node_group_name = "${var.name}-default"
  node_role_arn   = aws_iam_role.node.arn
  subnet_ids      = var.node_subnet_ids
  capacity_type   = var.capacity_type
  scaling_config {
    desired_size = var.node_desired
    max_size     = var.node_max
    min_size     = var.node_min
  }
  ami_type             = var.ami_type
  instance_types       = var.instance_types
  disk_size            = var.disk_size
  force_update_version = true
  tags                 = var.tags
}

output "cluster_name" {
  value = aws_eks_cluster.this.name
}

output "cluster_endpoint" {
  value = aws_eks_cluster.this.endpoint
}

output "cluster_ca" {
  value = aws_eks_cluster.this.certificate_authority[0].data
}

output "node_role_arn" {
  value = aws_iam_role.node.arn
}
