package family_dollar.ai.prompt_approval

default allow := false
default review := false

deny[msg] {
  input.asks_for_autonomous_action == true
  msg := "Prompt requests autonomous operational action."
}

deny[msg] {
  input.includes_payment_data == true
  msg := "Prompt includes payment data."
}

review[msg] {
  input.includes_pii == true
  msg := "Prompt includes PII and requires privacy review."
}

review[msg] {
  input.customer_facing_output == true
  msg := "Customer-facing output requires human review."
}

allow {
  count(deny) == 0
  count(review) == 0
}
