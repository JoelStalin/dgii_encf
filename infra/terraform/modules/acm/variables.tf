variable "domain_name" {
  type        = string
  description = "Dominio principal"
}

variable "subject_alternative_names" {
  type        = list(string)
  description = "SANs"
  default     = []
}

variable "zone_id" {
  type        = string
  description = "Hosted zone para validación"
}

variable "tags" {
  type        = map(string)
  description = "Etiquetas"
  default     = {}
}
