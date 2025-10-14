output "vpc_id" {
  value = module.vpc.vpc_id
}

output "alb_dns" {
  value = module.alb.lb_dns_name
}

output "ecs_cluster" {
  value = module.ecs.cluster_name
}

output "rds_endpoint" {
  value = module.rds.cluster_endpoint
}

output "redis_endpoint" {
  value = module.elasticache.primary_endpoint
}
