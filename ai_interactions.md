# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked the AI agent (Claude, via Gemini IDE) to build the entire PawPal+ project from scratch following the module instructions across all 6 phases. The main task was: implement a pet care scheduling system with Python classes, a CLI demo, automated tests, and a Streamlit UI.

For the stretch feature, I asked the agent to add a knapsack-based scheduling algorithm (dynamic programming) that maximizes total priority value within the owner's time budget, instead of the greedy approach that just picks tasks in priority order.

**What did the agent do?**

The agent worked through each phase step by step:
- **Phase 1**: Created `diagrams/uml_draft.mmd` (Mermaid class diagram) and `pawpal_system.py` (class skeletons with dataclasses)
- **Phase 2**: Implemented all method logic in `pawpal_system.py`, created `main.py` (CLI demo), and `tests/test_pawpal.py` (13 initial tests)
- **Phase 3**: Rewrote `app.py` to import backend classes, use `st.session_state` for persistence, and wire up Add Pet / Add Task / Generate Schedule buttons
- **Phase 4**: Added `sort_by_time()`, `filter_by_pet()`, `filter_incomplete()`, `handle_recurring()` to the Scheduler. Updated `main.py` to demo all new features
- **Phase 5**: Expanded tests to 27 (sorting, recurrence, conflict detection, edge cases). Updated README with test output
- **Phase 6**: Polished the Streamlit UI, created `diagrams/uml_final.mmd`, completed `reflection.md`
- **Stretch**: Added `optimize_knapsack()` and `generate_optimized_schedule()` using dynamic programming. Added 4 knapsack tests (31 total). Added scheduling mode toggle in the UI

Files edited: `pawpal_system.py`, `app.py`, `main.py`, `tests/test_pawpal.py`, `README.md`, `reflection.md`, `diagrams/uml_draft.mmd`, `diagrams/uml_final.mmd`

Commands run: `git clone`, `git add`, `git commit`, `python main.py`, `python -m pytest`

**What did you have to verify or fix manually?**

- The agent initially used emoji characters in print statements that crashed on Windows (cp1252 encoding error). I let the agent fix it but had to re-run to verify.
- The agent wrote overly detailed commit messages like "Clean up comments: remove e.g. from docstrings" that I asked it to simplify to just "Phase 2 update."
- I reviewed all docstrings and comments to remove "e.g." phrasing that felt too formal and unlike how I would naturally write.
- I verified the Streamlit app worked by running `streamlit run app.py` and testing the UI manually.

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | | |
| **Prompt** | | |
| **Response summary** | | |
| **What was useful** | | |
| **Problems noticed** | | |
| **Decision** | | |

**Which approach did you use in your final implementation and why?**

<!-- Your conclusion -->
