# Direction: Military Barracks Lawyer

A humorous Gradio app. Given a situation, the "Petty Officer" argues that it breaks military
regulations or etiquette, and a defensive persona argues that it doesn't. It is for fun, not
legal advice.

Status: dormant (last change 2025-03-15). Built in two days (54 commits), none since.

## Where it is heading
- Short one-paragraph answers from direct Chat API calls, which replaced Assistants
  run-polling (bd89d6c, f91a8e3, 7872a3f).
- A user option for a long or a short, sharp reply (807de18).
- Deployed to Hugging Face Spaces from GitHub Actions, with optional Matomo analytics
  (4cc1b0f, be6156a, 9e92ffd).

## Priorities
1. Replace the retired model names (`gpt-4o-mini`, a `gpt-4` default in
   utilities/openai_tools.py) with a current model (inferred).
2. Fix the README: it promises regulation search, a `config.py` and a `/docs` folder, none of
   which exist (inferred).

## Non-goals and constraints
- Python and Gradio in Docker, with config from environment variables (Dockerfile, .env-template).
- Keep the disclaimer: entertainment and information only (README.md).

## Decisions
- 2025-03-15: Added a long/short answer option (807de18).
- 2025-03-14: Dropped Assistants tool-calling for direct chat completions (bd89d6c, 7872a3f).

## Open questions for the owner
1. Is the Hugging Face Space still live and worth maintaining?

## Related documents
- README.md. There is no roadmap. To resume: update the model and README, then confirm the
  Space deploy still works.
