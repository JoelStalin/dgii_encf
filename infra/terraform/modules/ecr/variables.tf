variable "repositories" {
  description = "Lista de repositorios ECR a crear"
  type        = list(string)
}

variable "tags" {
  description = "Etiquetas a aplicar"
  type        = map(string)
  default     = {}
}
