package family_dollar.ai.environment_promotion

default allow := false

deny[msg] {
  input.tests_passed == false
  msg := "Tests must pass before promotion."
}

deny[msg] {
  input.change_ticket_present == false
  msg := "Change ticket is required before promotion."
}

deny[msg] {
  input.rollback_plan_present == false
  msg := "Rollback plan is required before promotion."
}

deny[msg] {
  input.owner_approval_present == false
  msg := "Owner approval is required before promotion."
}

review[msg] {
  input.to_environment == "prod"
  msg := "Production promotion requires governance review."
}

allow {
  count(deny) == 0
  count(review) == 0
}
