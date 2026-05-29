package family_dollar.ai.human_approval

default allow := false

deny[msg] {
  input.autonomous_execution_requested == true
  msg := "Autonomous execution remains blocked even after approval."
}

deny[msg] {
  input.approval_status != "approved"
  msg := "Human approval is required before handoff."
}

allow {
  count(deny) == 0
}
