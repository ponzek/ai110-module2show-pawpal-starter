"""
PawPal+ CLI Demo Script

Shows off the scheduling system including sorting, filtering,
recurring tasks, and conflict detection.
"""

import sys
import io

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    # --- Create Owner ---
    owner = Owner(name="Jordan", available_minutes=120)

    # --- Create Pets ---
    dog = Pet(name="Mochi", species="dog", age=3, special_needs=["joint supplement"])
    cat = Pet(name="Whiskers", species="cat", age=5)

    # --- Add Tasks for Mochi (added out of order on purpose) ---
    dog.add_task(Task(
        title="Afternoon enrichment",
        duration_minutes=20,
        priority="low",
        category="enrichment",
        preferred_time="14:00",
    ))
    dog.add_task(Task(
        title="Morning walk",
        duration_minutes=30,
        priority="high",
        category="walk",
        is_recurring=True,
        frequency="daily",
        preferred_time="08:00",
        due_date=date.today(),
    ))
    dog.add_task(Task(
        title="Breakfast feeding",
        duration_minutes=10,
        priority="high",
        category="feeding",
        is_recurring=True,
        frequency="daily",
        preferred_time="08:30",
    ))
    dog.add_task(Task(
        title="Joint supplement",
        duration_minutes=5,
        priority="medium",
        category="meds",
        is_recurring=True,
        frequency="daily",
        preferred_time="09:00",
    ))

    # --- Add Tasks for Whiskers (also out of order) ---
    cat.add_task(Task(
        title="Play session",
        duration_minutes=15,
        priority="low",
        category="enrichment",
        preferred_time="10:00",
    ))
    cat.add_task(Task(
        title="Breakfast feeding",
        duration_minutes=10,
        priority="high",
        category="feeding",
        is_recurring=True,
        frequency="daily",
        preferred_time="07:30",
    ))
    cat.add_task(Task(
        title="Litter box cleaning",
        duration_minutes=10,
        priority="medium",
        category="grooming",
        is_recurring=True,
        frequency="daily",
        preferred_time="09:30",
    ))

    # Add a task that overlaps with Mochi's morning walk to test conflict detection
    cat.add_task(Task(
        title="Vet checkup",
        duration_minutes=25,
        priority="high",
        category="meds",
        preferred_time="08:00",
    ))

    # --- Register pets with owner ---
    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(owner)

    # ============================================================
    # DEMO 1: Sort by time
    # ============================================================
    print("=" * 60)
    print("DEMO 1: Sort tasks by time")
    print("=" * 60)
    all_tasks = owner.get_all_tasks()
    sorted_by_time = scheduler.sort_by_time(all_tasks)
    for t in sorted_by_time:
        print(f"  {t.preferred_time or 'no time'} - {t.title} [{t.priority}]")

    # ============================================================
    # DEMO 2: Filter by pet
    # ============================================================
    print("\n" + "=" * 60)
    print("DEMO 2: Filter tasks for Mochi only")
    print("=" * 60)
    mochi_tasks = scheduler.filter_by_pet("Mochi")
    for t in mochi_tasks:
        print(f"  {t.title} ({t.duration_minutes} min, {t.priority})")

    # ============================================================
    # DEMO 3: Generate full schedule and check conflicts
    # ============================================================
    print("\n" + "=" * 60)
    print("DEMO 3: Full schedule with conflict detection")
    print("=" * 60)
    schedule = scheduler.generate_schedule()

    print(f"\n{'Time':<14} {'Task':<25} {'Pet':<12} {'Dur':>5}  {'Priority':<8}")
    print("-" * 68)
    for entry in schedule:
        time_str = f"{entry['start']}-{entry['end']}"
        print(f"{time_str:<14} {entry['task']:<25} {entry['pet']:<12} {entry['duration']:>3}m  [{entry['priority']}]")

    # Show conflicts
    conflicts = scheduler.detect_conflicts(schedule)
    if conflicts:
        print("\n!! Schedule Conflicts:")
        for c in conflicts:
            print(f"  - {c}")
    else:
        print("\n[OK] No scheduling conflicts detected.")

    # Print explanation
    print()
    print(scheduler.explain_plan(schedule))

    # ============================================================
    # DEMO 4: Recurring tasks
    # ============================================================
    print("\n" + "=" * 60)
    print("DEMO 4: Recurring task handling")
    print("=" * 60)

    # Mark the morning walk as complete and create next occurrence
    morning_walk = dog.get_tasks()[1]  # Morning walk (added second)
    print(f"  Completing: {morning_walk.title} (due: {morning_walk.due_date})")
    morning_walk.mark_complete()

    next_task = scheduler.handle_recurring(morning_walk, dog)
    if next_task:
        print(f"  Next occurrence created: {next_task.title} (due: {next_task.due_date})")
    print(f"  Mochi now has {len(dog.get_tasks())} tasks (original + next occurrence)")

    # ============================================================
    # DEMO 5: Filter out completed tasks
    # ============================================================
    print("\n" + "=" * 60)
    print("DEMO 5: Filter incomplete tasks only")
    print("=" * 60)
    incomplete = scheduler.filter_incomplete(dog.get_tasks())
    print(f"  Mochi total tasks: {len(dog.get_tasks())}")
    print(f"  Incomplete tasks: {len(incomplete)}")
    for t in incomplete:
        print(f"    - {t.title} (completed: {t.completed})")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
