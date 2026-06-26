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

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

The scheduler detects time conflicts (two tasks at the same time) but only warns the user instead of automatically resolving them. This is a reasonable tradeoff because the owner might want to decide which task to move — for example, they might reschedule a vet checkup but not skip a feeding. Automatically resolving conflicts could lead to important tasks being silently dropped.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
