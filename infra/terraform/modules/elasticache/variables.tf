variable "name" {
  type        = string
  description = "Nombre del replication group"
}

variable "subnet_ids" {
  type        = list(string)
  description = "Subredes privadas"
}

variable "security_group_ids" {
  type        = list(string)
  description = "Security groups permitidos"
}

variable "node_type" {
  type        = string
  description = "Tipo de nodo"
  default     = "cache.r6g.large"
}

variable "node_count" {
  type        = number
  description = "Cantidad de nodos"
  default     = 2
}

variable "engine_version" {
  type        = string
  description = "Versión de Redis"
  default     = "7.1"
}

variable "parameter_group" {
  type        = string
  description = "Nombre del parameter group"
  default     = "default.redis7"
}

variable "maintenance_window" {
  type        = string
  description = "Ventana de mantenimiento"
  default     = "sun:05:00-sun:06:00"
}

variable "tags" {
  type        = map(string)
  description = "Etiquetas"
  default     = {}
}
