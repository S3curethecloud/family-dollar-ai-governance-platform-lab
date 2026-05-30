
Hosting Options

Status: Hosting Decision Baseline

Option A — Static Frontend Demo Only
Host the frontend command center as a static public demo.
Backend API remains local/demo-only.
Lowest public-risk option.
Option B — Frontend + Demo API
Host frontend and a controlled demo backend API.
Requires stricter boundary, rate limiting, auth/abuse controls, and data controls.
Option C — Private Demo Only
Keep demo private and use screenshots, local run, or recorded walkthroughs.
Best if public claims or security posture are not ready.
Recommended A15 Path
Option A first: static frontend demo only.
Do not expose backend API publicly in A15.
Do not connect live enterprise systems.
Do not expose policy enforcement as production authority.
Future Hosting Candidates
Cloudflare Pages
GitHub Pages
Static site under SecureTheCloud portfolio
Private demo URL
Recorded demo walkthrough

