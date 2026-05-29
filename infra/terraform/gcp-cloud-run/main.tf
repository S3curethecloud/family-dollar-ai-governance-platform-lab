provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_cloud_run_v2_service" "governance_api" {
  name     = "family-dollar-governance-api-${var.environment}"
  location = var.region

  template {
    containers {
      image = var.backend_image

      ports {
        container_port = 8000
      }

      env {
        name  = "APP_ENV"
        value = var.environment
      }

      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
      }
    }
  }
}

resource "google_cloud_run_v2_service" "intake_portal" {
  name     = "family-dollar-intake-portal-${var.environment}"
  location = var.region

  template {
    containers {
      image = var.frontend_image

      ports {
        container_port = 8080
      }

      env {
        name  = "APP_ENV"
        value = var.environment
      }

      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
      }
    }
  }
}
