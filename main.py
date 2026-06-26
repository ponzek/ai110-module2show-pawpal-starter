"""
PawPal+ CLI Demo Script

Creates sample data (owner, pets, tasks) and prints a daily schedule
to verify that the backend logic works correctly.
"""

import sys
import io

# Fix Windows console encoding for emoji/unicode
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    # --- Create Owner ---
    owner = Owner(name="Jordan", available_minutes=120)

    # --- Create Pets ---
    dog = Pet(name="Mochi", species="dog", age=3, special_needs=["joint supplement"])
    cat = Pet(name="Whiskers", species="cat", age=5)

    # --- Add Tasks for Mochi (dog) ---
    dog.add_task(Task(
        title="Morning walk",
        duration_minutes=30,
        priority="high",
        category="walk",
        is_recurring=True,
        preferred_time="08:00",
    ))
    dog.add_task(Task(
        title="Breakfast feeding",
        duration_minutes=10,
        priority="high",
        category="feeding",
        is_recurring=True,
        preferred_time="08:30",
    ))
    dog.add_task(Task(
        title="Joint supplement",
        duration_minutes=5,
        priority="medium",
        category="meds",
        is_recurring=True,
    ))
    dog.add_task(Task(
        title="Afternoon enrichment",
        duration_minutes=20,
        priority="low",
        category="enrichment",
    ))

    # --- Add Tasks for Whiskers (cat) ---
    cat.add_task(Task(
        title="Breakfast feeding",
        duration_minutes=10,
        priority="high",
        category="feeding",
        is_recurring=True,
        preferred_time="07:30",
    ))
    cat.add_task(Task(
        title="Litter box cleaning",
        duration_minutes=10,
        priority="medium",
        category="grooming",
        is_recurring=True,
    ))
    cat.add_task(Task(
        title="Play session",
        duration_minutes=15,
        priority="low",
        category="enrichment",
    ))

    # --- Register pets with owner ---
    owner.add_pet(dog)
    owner.add_pet(cat)

    # --- Generate Schedule ---
    scheduler = Scheduler(owner)
    schedule = scheduler.generate_schedule()

    # --- Print Results ---
    print("=" * 60)
    print(f"PawPal+ Daily Schedule for {owner.name}")
    print(f"   Pets: {', '.join(p.name + ' (' + p.species + ')' for p in owner.get_pets())}")
    print(f"   Time budget: {owner.available_minutes} minutes")
    print("=" * 60)

    # Print the schedule table
    print(f"\n{'Time':<14} {'Task':<25} {'Pet':<12} {'Dur':>5}  {'Priority':<8}")
    print("-" * 68)
    for entry in schedule:
        time_str = f"{entry['start']}-{entry['end']}"
        print(f"{time_str:<14} {entry['task']:<25} {entry['pet']:<12} {entry['duration']:>3}m  [{entry['priority']}]")

    # Print the explanation
    print()
    print(scheduler.explain_plan(schedule))

    # Check for conflicts
    conflicts = scheduler.detect_conflicts(schedule)
    if conflicts:
        print("\n!! Schedule Conflicts:")
        for c in conflicts:
            print(f"  - {c}")
    else:
        print("\n[OK] No scheduling conflicts detected.")

    print("=" * 60)


if __name__ == "__main__":
    main()
