
Deployment Readiness Checklist

Status: Public Demo Readiness Baseline

Required Before Public Demo
Frontend build passes: true
Backend tests pass: true
Product boundaries documented: true
Claims boundary documented: true
Case study boundary documented: true
No production enforcement claims: true
No live enterprise integrations: true
No customer data: true
No secrets in repo: required check
No public backend exposure in A15: true
Technical Checks Before Deployment Execution
Run npm build
Run backend pytest
Check git status clean
Check no .env secrets committed
Check no credentials committed
Check static build artifact path
Check hosting target
Check public disclaimer visible or linked
A15 Decision
Deployment execution is not performed in A15.
A15 records readiness and deployment boundary only.

