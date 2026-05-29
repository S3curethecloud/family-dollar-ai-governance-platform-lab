output "governance_api_uri" {
  description = "Cloud Run URI for the governance API."
  value       = google_cloud_run_v2_service.governance_api.uri
}

output "intake_portal_uri" {
  description = "Cloud Run URI for the intake portal."
  value       = google_cloud_run_v2_service.intake_portal.uri
}
