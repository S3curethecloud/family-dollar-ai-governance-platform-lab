package family_dollar.ai.deployment_gate

default allow := false

deny[msg] {
  input.tests_passed == false
  msg := "Tests must pass before deployment."
}

deny[msg] {
  input.environment == "prod"
  input.rollback_plan_present == false
  msg := "Production deployment requires rollback plan."
}

deny[msg] {
  input.environment == "prod"
  input.observability_enabled == false
  msg := "Production deployment requires observability."
}

review[msg] {
  input.risk_tier == "Tier 3"
  msg := "Tier 3 deployment requires governance review."
}

review[msg] {
  input.risk_tier == "Tier 4"
  msg := "Tier 4 deployment requires executive review."
}

allow {
  count(deny) == 0
  count(review) == 0
}
