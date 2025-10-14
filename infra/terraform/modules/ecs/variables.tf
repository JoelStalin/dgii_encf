variable "name" {
  type        = string
  description = "Nombre del servicio"
}

variable "cpu" {
  type        = string
  description = "CPU para la tarea Fargate"
  default     = "1024"
}

variable "memory" {
  type        = string
  description = "Memoria para la tarea Fargate"
  default     = "2048"
}

variable "desired_count" {
  type        = number
  description = "Cantidad deseada de tareas"
  default     = 2
}

variable "assign_public_ip" {
  type        = bool
  description = "Si las tareas obtienen IP pública"
  default     = false
}

variable "enable_execute_command" {
  type        = bool
  description = "Habilita ECS Exec"
  default     = true
}

variable "subnet_ids" {
  type        = list(string)
  description = "Subredes donde desplegar"
}

variable "security_group_ids" {
  type        = list(string)
  description = "Security groups de la tarea"
}

variable "container_definitions" {
  type        = any
  description = "Definición de contenedor en formato objeto"
}

variable "load_balancer" {
  description = "Configuración opcional de load balancer"
  type = object({
    target_group_arn = string
    container_name   = string
    container_port   = number
  })
  default = null
}

variable "tags" {
  type        = map(string)
  description = "Etiquetas a aplicar"
  default     = {}
}
