import streamlit as st
from datetime import time
from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if "owner" not in st.session_state:
    st.session_state["owner"] = Owner(name=owner_name, address="")

owner = st.session_state["owner"]

if "scheduler" not in st.session_state:
    st.session_state["scheduler"] = Scheduler(owner)

st.markdown("### Add a Pet")
col1, col2 = st.columns(2)
with col1:
    pet_age = st.number_input("Pet age", min_value=0, max_value=100, value=3)
with col2:
    pet_breed = st.text_input("Breed", value="Mixed")

if st.button("Add pet"):
    pet = Pet(
        name=pet_name,
        age=int(pet_age),
        pet_type=species,
        breed=pet_breed,
    )
    owner.add_pet_information(pet)
    st.session_state["schedule"] = None

if owner.pets:
    st.write("Pets:", ", ".join(pet.name for pet in owner.pets))
else:
    st.info("Add a pet before scheduling care tasks.")

st.markdown("### Schedule a Task")
if owner.pets:
    selected_pet = st.selectbox(
        "Pet",
        owner.pets,
        format_func=lambda pet: pet.name,
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input(
            "Duration (minutes)", min_value=1, max_value=240, value=20
        )
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    task_description = st.text_input("Description", value="")
    scheduled_start = st.time_input("Preferred start time", value=time(9, 0))

    if st.button("Add task"):
        task = Task.create_task(
            name=task_title,
            description=task_description,
            duration=int(duration),
            priority={"low": 1, "medium": 2, "high": 3}[priority],
            scheduled_start=scheduled_start,
        )
        selected_pet.add_task(task)
        st.session_state["schedule"] = None

    if selected_pet.tasks:
        st.write(
            "Current tasks:",
            [
                {
                    "title": task.name,
                    "duration_minutes": task.duration,
                    "priority": task.priority,
                    "start_time": task.scheduled_start,
                }
                for task in selected_pet.tasks
            ],
        )
    else:
        st.info("No tasks for this pet yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
if owner.pets:
    if st.button("Generate schedule"):
        scheduler = st.session_state["scheduler"]
        st.session_state["schedule"] = scheduler.create_daily_schedule()

    schedule = st.session_state.get("schedule")
    if schedule is not None:
        if schedule:
            st.table(
                [
                    {
                        "task": task.name,
                        "duration_minutes": task.duration,
                        "priority": task.priority,
                        "start_time": task.scheduled_start,
                    }
                    for task in schedule
                ]
            )
            scheduler = st.session_state["scheduler"]
            st.caption(scheduler.provide_reasoning())
            for warning in scheduler.conflict_warnings:
                st.warning(warning)
        else:
            st.info("No care tasks have been added yet.")
else:
    st.info("Add a pet and at least one task to generate a schedule.")
