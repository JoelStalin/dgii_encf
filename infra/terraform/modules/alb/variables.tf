variable "name" {
  type        = string
  description = "Nombre del ALB"
}

variable "subnet_ids" {
  type        = list(string)
  description = "Subredes públicas"
}

variable "security_group_ids" {
  type        = list(string)
  description = "Security groups"
}

variable "vpc_id" {
  type        = string
  description = "VPC donde vive el ALB"
}

variable "certificate_arn" {
  type        = string
  description = "Certificado TLS en ACM"
}

variable "target_port" {
  type        = number
  description = "Puerto del target group"
  default     = 8080
}

variable "health_check_path" {
  type        = string
  description = "Ruta de health check"
  default     = "/readyz"
}

variable "enable_http_redirect" {
  type        = bool
  description = "Habilita redirección HTTP->HTTPS"
  default     = true
}

variable "deletion_protection" {
  type        = bool
  description = "Protección contra eliminación"
  default     = true
}

variable "tags" {
  type        = map(string)
  description = "Etiquetas"
  default     = {}
}
