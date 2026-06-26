import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.caption("A smart pet care planning assistant")

# --- Session State Setup ---
# Store the Owner object in session_state so it persists between page refreshes
if "owner" not in st.session_state:
    st.session_state.owner = None

# --- Owner Setup ---
st.subheader("Owner Info")
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
st.subheader("Add a Pet")
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
        st.write(f"- {pet.name} ({pet.species}, age {pet.age})")
else:
    st.info("No pets added yet.")

st.divider()

# --- Add Tasks to a Pet ---
st.subheader("Add a Task")

if owner.get_pets():
    # Let the user pick which pet gets the task
    pet_names = [p.name for p in owner.get_pets()]
    selected_pet_name = st.selectbox("Choose a pet", pet_names)

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task name", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["high", "medium", "low"])

    category = st.selectbox("Category", ["walk", "feeding", "meds", "grooming", "enrichment", "general"])

    if st.button("Add Task"):
        new_task = Task(
            title=task_title,
            duration_minutes=int(duration),
            priority=priority,
            category=category,
        )
        # Find the selected pet and add the task
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
            st.write(f"_{pet.name}:_")
            for t in tasks:
                st.write(f"  - {t.title} ({t.duration_minutes} min, {t.priority})")
else:
    st.info("Add a pet first, then you can add tasks.")

st.divider()

# --- Generate Schedule ---
st.subheader("Generate Schedule")

if st.button("Build Today's Schedule"):
    all_tasks = owner.get_all_tasks()

    if not all_tasks:
        st.warning("No tasks to schedule. Add some tasks first!")
    else:
        scheduler = Scheduler(owner)
        schedule = scheduler.generate_schedule()

        # Show the schedule as a table
        st.write("**Daily Plan:**")
        st.table(schedule)

        # Show the explanation
        explanation = scheduler.explain_plan(schedule)
        st.text(explanation)

        # Check for conflicts
        conflicts = scheduler.detect_conflicts(schedule)
        if conflicts:
            st.warning("Schedule Conflicts Found:")
            for c in conflicts:
                st.write(f"- {c}")
        else:
            st.success("No scheduling conflicts!")
