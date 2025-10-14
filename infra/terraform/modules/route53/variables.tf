variable "zone_id" {
  type        = string
  description = "Zone ID de Route53"
}

variable "record_name" {
  type        = string
  description = "Nombre del registro"
}

variable "alias_name" {
  type        = string
  description = "DNS del ALB"
}

variable "alias_zone_id" {
  type        = string
  description = "Zone ID del ALB"
}
