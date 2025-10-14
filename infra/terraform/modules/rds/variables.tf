variable "identifier" {
  type        = string
  description = "Identificador del clúster"
}

variable "database_name" {
  type        = string
  description = "Nombre de la base de datos"
}

variable "master_username" {
  type        = string
  description = "Usuario administrador"
}

variable "master_password" {
  type        = string
  description = "Contraseña del administrador"
  sensitive   = true
}

variable "engine_version" {
  type        = string
  description = "Versión del motor"
  default     = "15.3"
}

variable "instance_class" {
  type        = string
  description = "Clase de las instancias"
  default     = "db.r6g.large"
}

variable "instance_count" {
  type        = number
  description = "Cantidad de instancias"
  default     = 2
}

variable "subnet_ids" {
  type        = list(string)
  description = "Subredes privadas"
}

variable "security_group_ids" {
  type        = list(string)
  description = "Security groups permitidos"
}

variable "backup_retention_days" {
  type        = number
  description = "Días de retención de backup"
  default     = 7
}

variable "preferred_backup_window" {
  type        = string
  description = "Ventana de backup"
  default     = "05:00-07:00"
}

variable "deletion_protection" {
  type        = bool
  description = "Protege contra eliminación"
  default     = true
}

variable "min_capacity" {
  type        = number
  description = "Capacidad mínima serverless v2"
  default     = 0.5
}

variable "max_capacity" {
  type        = number
  description = "Capacidad máxima serverless v2"
  default     = 4
}

variable "tags" {
  type        = map(string)
  description = "Etiquetas"
  default     = {}
}
