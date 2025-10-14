variable "kms_key_id" {
  type        = string
  description = "KMS Key para cifrar secretos"
}

variable "secrets" {
  description = "Mapa de secretos"
  type = map(object({
    name        = string
    description = optional(string, "")
    value       = map(string)
  }))
}

variable "tags" {
  type        = map(string)
  description = "Etiquetas"
  default     = {}
}
