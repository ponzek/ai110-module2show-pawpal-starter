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

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_priority()`, `Scheduler.sort_by_time()` | Sorts by priority (high first) or by preferred time (earliest first) |
| Filtering | `Scheduler.filter_by_time()`, `Scheduler.filter_by_pet()`, `Scheduler.filter_incomplete()` | Filters tasks by time budget, pet name, or completion status |
| Conflict handling | `Scheduler.detect_conflicts()` | Compares time slots and returns warnings for overlapping tasks |
| Recurring tasks | `Scheduler.handle_recurring()` | Creates the next occurrence (daily or weekly) when a task is completed |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
