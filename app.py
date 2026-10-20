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
    selected_pet_index = st.selectbox(
        "Pet",
        range(len(owner.pets)),
        format_func=lambda index: owner.pets[index].name,
    )
    selected_pet = owner.pets[selected_pet_index]
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
        st.success(f"Added '{task.name}' to {selected_pet.name}'s care tasks.")

    scheduler = st.session_state["scheduler"]
    completion_filter = st.selectbox(
        "Show tasks",
        ["All", "To do", "Completed"],
        key="task_completion_filter",
    )
    completed_filter = {
        "All": None,
        "To do": False,
        "Completed": True,
    }[completion_filter]
    visible_tasks = scheduler.filter_tasks(
        completed=completed_filter,
        pet_name=selected_pet.name,
    )
    visible_tasks = scheduler.sort_by_time(visible_tasks)

    if visible_tasks:
        st.table(
            [
                {
                    "Care task": task.name,
                    "Description": task.description or "-",
                    "Duration (min)": task.duration,
                    "Priority": task.priority,
                    "Start time": (
                        task.scheduled_start.strftime("%I:%M %p").lstrip("0")
                        if task.scheduled_start
                        else "Not scheduled"
                    ),
                    "Status": "Completed" if task.completed else "To do",
                }
                for task in visible_tasks
            ]
        )
    else:
        st.info(f"No {completion_filter.lower()} tasks for {selected_pet.name}.")

st.divider()

st.subheader("Build Schedule")
if owner.pets:
    if st.button("Generate schedule"):
        scheduler = st.session_state["scheduler"]
        st.session_state["schedule"] = scheduler.create_daily_schedule()

    schedule = st.session_state.get("schedule")
    if schedule is not None:
        if schedule:
            scheduler = st.session_state["scheduler"]
            if scheduler.conflict_warnings:
                for warning in scheduler.conflict_warnings:
                    st.warning(
                        f"{warning} Adjust one task's start time or duration "
                        "so both care tasks fit into the day."
                    )
            else:
                st.success("Your schedule is ready with no timing conflicts.")

            st.table(
                [
                    {
                        "Pet": next(
                            (
                                pet.name
                                for pet in owner.pets
                                if any(pet_task is task for pet_task in pet.tasks)
                            ),
                            "Unknown pet",
                        ),
                        "Care task": task.name,
                        "Duration (min)": task.duration,
                        "Priority": task.priority,
                        "Start time": (
                            task.scheduled_start.strftime("%I:%M %p").lstrip("0")
                            if task.scheduled_start
                            else "Not scheduled"
                        ),
                    }
                    for task in schedule
                ]
            )
            st.caption(scheduler.provide_reasoning())
        else:
            st.info("No care tasks have been added yet.")
else:
    st.info("Add a pet and at least one task to generate a schedule.")
