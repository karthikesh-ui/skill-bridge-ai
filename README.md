# Skill Bridge-AI

A college minor project for students exploring career options after 10th standard. The Flask backend ranks career matches by overlap with separately stored answers, loads curated JSON pathways, and offers optional Gemini explanations. The browser stores profile, discovery answers, selected career, skill checks, and roadmap status in localStorage. No account is required.

## Architecture
Student answers → weighted subject/activity/area/work-style matching → structured career JSON → pathway routes → optional Gemini explanation → roadmap and demo readiness. Recommendation weights are subjects 3, activities 2, career areas 2, work preference 1, and competitive-exam preference 1. Scores are normalized exploration rankings, not scientifically validated probabilities or eligibility decisions. The demo readiness model weights skills 40%, completed stages 40%, project 10%, interview practice 10%; it is not a professional assessment.

## Start
See [SETUP.md](SETUP.md). With an activated environment: `pip install -r requirements.txt` then `python app.py`; open `http://127.0.0.1:5000/`.

## Data and limitations
`data/careers.json`, `data/career_extensions.json`, `data/matching.json`, `data/pathways.json`, `data/skills.json`, and `data/exams.json` provide 44 example professions and illustrative routes, not an exhaustive catalogue. Extension records are merged by stable career ID into the existing API structures. Several programs and exams have changing eligibility. Always verify admissions, subject requirements, dates, professional licensing and recruitment rules on official institution and examination websites. Routes and resources are illustrative; profile/progress remain in the same browser and are lost if site data is cleared. Gemini is optional and falls back to a deterministic explanation.

## Future scope
Phase 2: more Indian and state-specific careers, official verification and college discovery. Phase 3: resume analysis and ATS. Phase 4: login, database, cloud deployment and progress sync. Phase 5: live resources, notifications and advanced mentoring.

## Tests
`python -m unittest discover -s tests -v` checks API flow and page routes. Do not put a secret in client code or commit `.env`.
