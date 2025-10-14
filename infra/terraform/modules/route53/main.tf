terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}

resource "aws_route53_record" "this" {
  zone_id = var.zone_id
  name    = var.record_name
  type    = "A"

  alias {
    evaluate_target_health = true
    name                   = var.alias_name
    zone_id                = var.alias_zone_id
  }
}

output "record_fqdn" {
  value = aws_route53_record.this.fqdn
}
