variable "project_id" {
  description = "GCP project ID."
  type        = string
}

variable "region" {
  description = "GCP region for Cloud Run services."
  type        = string
  default     = "us-central1"
}

variable "backend_image" {
  description = "Container image URI for the governance API."
  type        = string
}

variable "frontend_image" {
  description = "Container image URI for the intake portal."
  type        = string
}

variable "environment" {
  description = "Deployment environment name."
  type        = string
  default     = "demo"
}
