# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
============================================================
PawPal+ Daily Schedule for Jordan
   Pets: Mochi (dog), Whiskers (cat)
   Time budget: 120 minutes
============================================================

Time           Task                      Pet            Dur  Priority
--------------------------------------------------------------------
08:30-08:40    Breakfast feeding         Mochi         10m  [high]
07:30-07:40    Breakfast feeding         Whiskers      10m  [high]
08:00-08:30    Morning walk              Mochi         30m  [high]
08:30-08:35    Joint supplement          Mochi          5m  [medium]
08:35-08:45    Litter box cleaning       Whiskers      10m  [medium]
08:45-09:00    Play session              Whiskers      15m  [low]
09:00-09:20    Afternoon enrichment      Mochi         20m  [low]

>> Today's Plan (7 tasks, 100 min total):

  1. 08:30 -- Breakfast feeding for Mochi (10 min) [high]
     Reason: high priority -- scheduled first
  2. 07:30 -- Breakfast feeding for Whiskers (10 min) [high]
     Reason: high priority -- scheduled first
  3. 08:00 -- Morning walk for Mochi (30 min) [high]
     Reason: high priority -- scheduled first
  4. 08:30 -- Joint supplement for Mochi (5 min) [medium]
     Reason: medium priority
  5. 08:35 -- Litter box cleaning for Whiskers (10 min) [medium]
     Reason: medium priority
  6. 08:45 -- Play session for Whiskers (15 min) [low]
     Reason: low priority -- fit into remaining time
  7. 09:00 -- Afternoon enrichment for Mochi (20 min) [low]
     Reason: low priority -- fit into remaining time

>> Time remaining: 20 min out of 120 min budget

[OK] No scheduling conflicts detected.
============================================================
```

## 🧪 Testing PawPal+

Run the test suite with:

```bash
python -m pytest tests/test_pawpal.py -v
```

The test suite covers 27 tests across 7 areas:
- **Task completion** — verifies `mark_complete()` changes status
- **Task addition** — adding/removing tasks updates the pet's list
- **Task validation** — `is_valid()` catches empty titles, zero duration, bad priority
- **Sorting** — tasks sort correctly by time and by priority
- **Recurrence** — completing a daily task creates tomorrow's task, weekly creates next week's
- **Conflict detection** — overlapping times are flagged, back-to-back tasks are not
- **Edge cases** — empty schedules, no pets, filtering by nonexistent pet

Sample test output:

```
============================= test session starts =============================
collected 27 items

tests/test_pawpal.py::TestTaskCompletion::test_task_starts_incomplete PASSED
tests/test_pawpal.py::TestTaskCompletion::test_mark_complete_changes_status PASSED
tests/test_pawpal.py::TestTaskCompletion::test_mark_complete_is_idempotent PASSED
tests/test_pawpal.py::TestTaskAddition::test_pet_starts_with_no_tasks PASSED
tests/test_pawpal.py::TestTaskAddition::test_adding_one_task_increases_count PASSED
tests/test_pawpal.py::TestTaskAddition::test_adding_multiple_tasks PASSED
tests/test_pawpal.py::TestTaskAddition::test_remove_task_decreases_count PASSED
tests/test_pawpal.py::TestTaskValidation::test_valid_task PASSED
tests/test_pawpal.py::TestTaskValidation::test_empty_title_is_invalid PASSED
tests/test_pawpal.py::TestTaskValidation::test_zero_duration_is_invalid PASSED
tests/test_pawpal.py::TestTaskValidation::test_bad_priority_is_invalid PASSED
tests/test_pawpal.py::TestSorting::test_sort_by_time_returns_chronological_order PASSED
tests/test_pawpal.py::TestSorting::test_sort_by_time_puts_no_time_last PASSED
tests/test_pawpal.py::TestSorting::test_sort_by_priority_high_first PASSED
tests/test_pawpal.py::TestRecurrence::test_daily_task_creates_next_day PASSED
tests/test_pawpal.py::TestRecurrence::test_weekly_task_creates_next_week PASSED
tests/test_pawpal.py::TestRecurrence::test_non_recurring_task_returns_none PASSED
tests/test_pawpal.py::TestConflictDetection::test_overlapping_tasks_detected PASSED
tests/test_pawpal.py::TestConflictDetection::test_no_conflicts_when_tasks_dont_overlap PASSED
tests/test_pawpal.py::TestConflictDetection::test_back_to_back_tasks_no_conflict PASSED
tests/test_pawpal.py::TestEdgeCases::test_schedule_with_no_tasks PASSED
tests/test_pawpal.py::TestEdgeCases::test_schedule_with_no_pets PASSED
tests/test_pawpal.py::TestEdgeCases::test_explain_plan_with_empty_schedule PASSED
tests/test_pawpal.py::TestEdgeCases::test_filter_incomplete_skips_completed PASSED
tests/test_pawpal.py::TestEdgeCases::test_schedule_respects_time_budget PASSED
tests/test_pawpal.py::TestEdgeCases::test_filter_by_pet_returns_correct_tasks PASSED
tests/test_pawpal.py::TestEdgeCases::test_filter_by_nonexistent_pet PASSED

============================= 27 passed in 0.53s ==============================
```

**Confidence Level: 4/5** — All 27 tests pass. The scheduler handles the main use cases well. With more time I would add tests for edge cases like tasks with identical times across different pets and stress-testing with a large number of tasks.

## 📐 Smarter Scheduling



| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_priority()`, `Scheduler.sort_by_time()` | Sorts by priority (high first) or by preferred time (earliest first) |
| Filtering | `Scheduler.filter_by_time()`, `Scheduler.filter_by_pet()`, `Scheduler.filter_incomplete()` | Filters tasks by time budget, pet name, or completion status |
| Conflict handling | `Scheduler.detect_conflicts()` | Compares time slots and returns warnings for overlapping tasks |
| Recurring tasks | `Scheduler.handle_recurring()` | Creates the next occurrence (daily or weekly) when a task is completed |

## 📸 Demo Walkthrough

1. **Enter owner info** — Type your name and set how much time you have today using the slider.
2. **Add your pets** — Enter a pet's name, species, and age, then click "Add Pet." Repeat for each pet.
3. **Add tasks** — Pick a pet from the dropdown, fill in the task details (name, duration, priority, category, preferred time), and click "Add Task." Tasks show up in a table under each pet.
4. **Choose sort order** — Select whether to sort by priority (high first) or by time (earliest first).
5. **Generate the schedule** — Click "Build Today's Schedule." The app creates a daily plan that fits within your time budget.
6. **Review the plan** — The schedule shows as a table with time slots, task names, pets, and priorities. Expand "Why this schedule?" to see the reasoning behind each task's placement.
7. **Check for conflicts** — If two tasks overlap, the app shows a warning with the conflicting times and suggests adjusting preferred times.
8. **See time remaining** — A metric at the bottom shows how many minutes are left in your budget.
