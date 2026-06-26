import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.caption("A smart pet care planning assistant")

# --- Session State Setup ---
if "owner" not in st.session_state:
    st.session_state.owner = None

# --- Owner Setup ---
st.subheader("👤 Owner Info")
owner_name = st.text_input("Your name", value="Jordan")
available_time = st.slider("Available time today (minutes)", 30, 300, 120)

if st.session_state.owner is None:
    st.session_state.owner = Owner(name=owner_name, available_minutes=available_time)
else:
    st.session_state.owner.name = owner_name
    st.session_state.owner.set_availability(available_time)

owner = st.session_state.owner

st.divider()

# --- Add a Pet ---
st.subheader("🐾 Add a Pet")
col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col3:
    pet_age = st.number_input("Age", min_value=0, max_value=30, value=3)

if st.button("Add Pet"):
    new_pet = Pet(name=pet_name, species=species, age=pet_age)
    owner.add_pet(new_pet)
    st.success(f"Added {pet_name} the {species}!")

# Show current pets
if owner.get_pets():
    st.write("**Your pets:**")
    for pet in owner.get_pets():
        task_count = len(pet.get_tasks())
        st.write(f"- {pet.name} ({pet.species}, age {pet.age}) — {task_count} tasks")
else:
    st.info("No pets added yet.")

st.divider()

# --- Add Tasks to a Pet ---
st.subheader("📋 Add a Task")

if owner.get_pets():
    pet_names = [p.name for p in owner.get_pets()]
    selected_pet_name = st.selectbox("Choose a pet", pet_names)

    col1, col2 = st.columns(2)
    with col1:
        task_title = st.text_input("Task name", value="Morning walk")
        category = st.selectbox("Category", ["walk", "feeding", "meds", "grooming", "enrichment", "general"])
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        priority = st.selectbox("Priority", ["high", "medium", "low"])

    preferred_time = st.text_input("Preferred time (optional, format HH:MM)", value="", placeholder="08:00")
    is_recurring = st.checkbox("Recurring task?")
    frequency = "once"
    if is_recurring:
        frequency = st.selectbox("Frequency", ["daily", "weekly"])

    if st.button("Add Task"):
        new_task = Task(
            title=task_title,
            duration_minutes=int(duration),
            priority=priority,
            category=category,
            preferred_time=preferred_time if preferred_time else None,
            is_recurring=is_recurring,
            frequency=frequency,
        )
        for pet in owner.get_pets():
            if pet.name == selected_pet_name:
                pet.add_task(new_task)
                st.success(f"Added '{task_title}' to {pet.name}!")
                break

    # Show tasks for each pet
    st.write("**Current tasks:**")
    for pet in owner.get_pets():
        tasks = pet.get_tasks()
        if tasks:
            st.write(f"**{pet.name}:**")
            task_data = []
            for t in tasks:
                task_data.append({
                    "Task": t.title,
                    "Duration": f"{t.duration_minutes} min",
                    "Priority": t.priority,
                    "Category": t.category,
                    "Time": t.preferred_time or "—",
                    "Recurring": t.frequency if t.is_recurring else "no",
                })
            st.table(task_data)
else:
    st.info("Add a pet first, then you can add tasks.")

st.divider()

# --- Generate Schedule ---
st.subheader("📅 Generate Schedule")

sort_option = st.radio("Sort tasks by:", ["Priority (high first)", "Time (earliest first)"], horizontal=True)

if st.button("Build Today's Schedule"):
    all_tasks = owner.get_all_tasks()

    if not all_tasks:
        st.warning("No tasks to schedule. Add some tasks first!")
    else:
        scheduler = Scheduler(owner)
        schedule = scheduler.generate_schedule()

        # Sort the display based on user choice
        if sort_option == "Time (earliest first)":
            schedule = sorted(schedule, key=lambda x: x["start"])

        # Show the schedule as a clean table
        st.write("**Today's Schedule:**")
        display_data = []
        for entry in schedule:
            display_data.append({
                "Time": f"{entry['start']} - {entry['end']}",
                "Task": entry["task"],
                "Pet": entry["pet"],
                "Duration": f"{entry['duration']} min",
                "Priority": entry["priority"],
            })
        st.table(display_data)

        # Show the reasoning
        with st.expander("Why this schedule?", expanded=False):
            explanation = scheduler.explain_plan(schedule)
            st.text(explanation)

        # Check for conflicts and show warnings
        conflicts = scheduler.detect_conflicts(schedule)
        if conflicts:
            st.error("⚠️ Schedule Conflicts Detected!")
            for c in conflicts:
                st.warning(c)
            st.info("Tip: Try adjusting preferred times to avoid overlaps.")
        else:
            st.success("✅ No scheduling conflicts — you're all set!")

        # Show time budget summary
        total_scheduled = sum(e["duration"] for e in schedule)
        remaining = owner.available_minutes - total_scheduled
        st.metric("Time Remaining", f"{remaining} min", delta=f"-{total_scheduled} min used")
