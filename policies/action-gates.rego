package family_dollar.ai.action_gate

default allow := false

deny[msg] {
  input.action_type == "autonomous_execution"
  msg := "Autonomous execution is blocked."
}

deny[msg] {
  input.touches_payment_data == true
  msg := "Payment-data action is restricted."
}

deny[msg] {
  input.mutates_retail_system == true
  input.human_approval_status != "approved"
  msg := "Retail-system mutation requires human approval."
}

deny[msg] {
  input.customer_impacting == true
  input.human_approval_status != "approved"
  msg := "Customer-impacting action requires human approval."
}

allow {
  count(deny) == 0
}
