# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

The initial UML design uses four classes that map directly to the real-world domain:

- **Owner** — Represents the pet owner. Holds the owner's name, daily time budget (`available_minutes`), care preferences, and a list of their pets. Responsible for managing pet registration and setting availability.
- **Pet** — Represents an individual pet. Stores name, species, age, special needs, and a list of care tasks. Responsible for adding/removing tasks.
- **Task** — A single care activity (walk, feeding, meds, grooming, enrichment). Uses a Python dataclass with fields for title, duration, priority level (low/medium/high), category, recurrence flag, and preferred time. Supports comparison for priority-based sorting.
- **Scheduler** — The brain of the system. Takes an Owner (with their pets and tasks) and produces a daily schedule. Responsible for sorting by priority, filtering tasks to fit the time budget, detecting conflicts, and generating a human-readable explanation of the plan.

Relationships: Owner *owns* one or more Pets; each Pet *has* zero or more Tasks; the Scheduler *plans for* an Owner and *processes* their Tasks.

**b. Design changes**

Yes, the design changed in a few ways during implementation:

- Added a `frequency` field (`"once"`, `"daily"`, `"weekly"`) and a `due_date` field to Task. The original design only had an `is_recurring` boolean, but that wasn't enough to calculate the next occurrence date.
- Added `get_all_tasks()` to Owner so the Scheduler could pull every task across all pets in one call instead of looping through pets itself. This kept the Scheduler cleaner.
- Added `sort_by_time()`, `filter_by_pet()`, and `filter_incomplete()` to Scheduler during Phase 4. The initial design only had priority sorting and time-budget filtering.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers three main constraints:
1. **Priority** — High-priority tasks get scheduled first (meds and feeding before enrichment).
2. **Time budget** — Tasks are added in priority order until the owner's available minutes run out. Lower-priority tasks get dropped if there's no room.
3. **Preferred time** — If a task has a preferred time, the scheduler uses it. Otherwise, it fills in the next available slot starting at 08:00.

Priority felt like the most important constraint because missing medication or a feeding is worse than skipping a play session. Time budget came second because the owner has a real limit on their day.

**b. Tradeoffs**

The scheduler detects time conflicts (two tasks at the same time) but only warns the user instead of automatically resolving them. This is a reasonable tradeoff because the owner might want to decide which task to move — for example, they might reschedule a vet checkup but not skip a feeding. Automatically resolving conflicts could lead to important tasks being silently dropped.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI throughout the project for several tasks:
- **Design brainstorming** — Asked for help identifying the four main classes and their relationships, which became the UML diagram.
- **Code generation** — Used AI to generate the class skeletons from the UML, then to implement the scheduling logic and sorting algorithms.
- **Test writing** — Asked AI to draft test cases covering happy paths and edge cases like empty schedules and back-to-back tasks.
- **Debugging** — When the CLI demo crashed on Windows due to emoji encoding, AI helped diagnose the `cp1252` codec error and add a fix.

The most helpful prompts were specific ones like "sort tasks by their HH:MM time string using a lambda key" rather than vague ones like "make the scheduler better."

**b. Judgment and verification**

One moment where I didn't accept an AI suggestion as-is was the commit messages. The AI generated overly detailed messages like "Clean up comments: remove e.g. from docstrings" which drew unnecessary attention to minor changes. I had it amend the message to something simpler. I also reviewed the generated code to make sure comments and docstrings didn't use language that felt too polished or unlike how I'd naturally write.

---

## 4. Testing and Verification

**a. What you tested**

The test suite covers 27 tests across these behaviors:
- Task completion — `mark_complete()` actually changes the status
- Task addition/removal — adding and removing tasks updates the pet's list correctly
- Input validation — `is_valid()` rejects empty titles, zero durations, and invalid priority levels
- Sorting — tasks sort correctly by time (chronological) and by priority (high first)
- Recurring tasks — completing a daily task creates a new one for tomorrow, weekly creates one for next week, non-recurring returns nothing
- Conflict detection — overlapping time slots get flagged, non-overlapping and back-to-back tasks don't
- Edge cases — empty schedules, no pets, filtering by a pet that doesn't exist

These tests matter because the scheduler is the core of the app. If sorting or filtering breaks, the daily plan would be wrong and the owner could miss important tasks.

**b. Confidence**

I'm fairly confident the scheduler works correctly — **4 out of 5**. All 27 tests pass and they cover the main paths. If I had more time, I'd test: tasks with identical preferred times across different pets, what happens when available_minutes is 0, and stress-testing with 50+ tasks to see if performance holds up.

---

## 5. Reflection

**a. What went well**

I'm most satisfied with how the four classes work together. The Scheduler talks to the Owner to get pets and tasks, sorts them, filters by time, and builds a clean schedule. The separation between data (Task, Pet, Owner) and logic (Scheduler) made it easy to add new features like recurring tasks without breaking existing code.

**b. What you would improve**

If I had another iteration, I would make the conflict detection smarter — instead of just warning about overlaps, it could suggest moving one of the tasks to the next available slot. I'd also add a way to edit or delete tasks from the Streamlit UI instead of only adding them.

**c. Key takeaway**

The biggest thing I learned is that designing the system first (UML and class skeletons) before writing any logic made everything smoother. When I got to implementation, I already knew what each class was responsible for and how they connected. AI was most useful as a collaborator for generating boilerplate and catching edge cases, but I still needed to make judgment calls about what to keep, what to change, and how to organize the code.
