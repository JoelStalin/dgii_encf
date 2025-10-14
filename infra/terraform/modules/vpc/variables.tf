variable "name" {
  description = "Nombre lógico del VPC"
  type        = string
}

variable "cidr_block" {
  description = "CIDR principal"
  type        = string
}

variable "availability_zones" {
  description = "Lista de zonas de disponibilidad a usar"
  type        = list(string)
}

variable "public_subnets" {
  description = "Lista de subredes públicas"
  type        = list(string)
  default     = []
}

variable "private_subnets" {
  description = "Lista de subredes privadas"
  type        = list(string)
  default     = []
}

variable "create_nat_gateway" {
  description = "Indica si se debe crear un NAT gateway"
  type        = bool
  default     = true
}

variable "tags" {
  description = "Etiquetas adicionales"
  type        = map(string)
  default     = {}
}
