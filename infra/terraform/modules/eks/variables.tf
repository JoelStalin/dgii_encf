variable "name" {
  type        = string
  description = "Nombre base del clúster"
}

variable "version" {
  type        = string
  description = "Versión de Kubernetes"
  default     = "1.29"
}

variable "vpc_id" {
  type        = string
  description = "ID del VPC"
}

variable "subnet_ids" {
  type        = list(string)
  description = "Subredes para el endpoint del clúster"
}

variable "node_subnet_ids" {
  type        = list(string)
  description = "Subredes para los nodos"
}

variable "enable_public_endpoint" {
  type        = bool
  description = "Habilita endpoint público"
  default     = false
}

variable "capacity_type" {
  type        = string
  description = "Tipo de capacidad (ON_DEMAND o SPOT)"
  default     = "ON_DEMAND"
}

variable "node_min" {
  type        = number
  description = "Mínimo de nodos"
  default     = 2
}

variable "node_desired" {
  type        = number
  description = "Número deseado de nodos"
  default     = 3
}

variable "node_max" {
  type        = number
  description = "Máximo de nodos"
  default     = 5
}

variable "instance_types" {
  type        = list(string)
  description = "Tipos de instancia para los nodos"
  default     = ["m6i.large"]
}

variable "ami_type" {
  type        = string
  description = "Tipo de AMI"
  default     = "AL2023_x86_64"
}

variable "disk_size" {
  type        = number
  description = "Tamaño del disco de los nodos"
  default     = 50
}

variable "tags" {
  type        = map(string)
  description = "Etiquetas a aplicar"
  default     = {}
}
