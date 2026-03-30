import streamlit as st
from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+.

This app helps a pet owner:
- manage pets
- add care tasks
- generate a daily schedule based on time and completion status
"""
)

# -------------------------------------------------------------------
# Session state setup
# -------------------------------------------------------------------
if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_id=1, name="Jordan")

if "next_pet_id" not in st.session_state:
    st.session_state.next_pet_id = 1

if "next_task_id" not in st.session_state:
    st.session_state.next_task_id = 1

st.divider()

# -------------------------------------------------------------------
# Owner info
# -------------------------------------------------------------------
st.subheader("Owner Information")

owner_name = st.text_input("Owner name", value=st.session_state.owner.name)

if st.button("Update owner info"):
    st.session_state.owner.name = owner_name.strip() if owner_name.strip() else st.session_state.owner.name
    st.success("Owner info updated.")

st.divider()

# -------------------------------------------------------------------
# Add a pet
# -------------------------------------------------------------------
st.subheader("Add a Pet")

with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    breed = st.text_input("Breed", value="")
    age = st.number_input("Age", min_value=0, max_value=50, value=1)
    weight = st.number_input("Weight", min_value=0.1, max_value=300.0, value=5.0)
    add_pet_submitted = st.form_submit_button("Add pet")

if add_pet_submitted:
    if pet_name.strip():
        pet = Pet(
            pet_id=st.session_state.next_pet_id,
            name=pet_name.strip(),
            species=species,
            breed=breed.strip(),
            age=int(age),
            weight=float(weight),
        )
        st.session_state.owner.add_pet(pet)
        st.session_state.next_pet_id += 1
        st.success(f"Added pet: {pet.name}")
    else:
        st.error("Please enter a pet name.")

if st.session_state.owner.pets:
    st.markdown("### Current Pets")
    pet_table = [
        {
            "Pet ID": pet.pet_id,
            "Name": pet.name,
            "Species": pet.species,
            "Breed": pet.breed,
            "Age": pet.age,
            "Weight": pet.weight,
            "Task Count": len(pet.tasks),
        }
        for pet in st.session_state.owner.pets
    ]
    st.table(pet_table)
else:
    st.info("No pets added yet.")

st.divider()

# -------------------------------------------------------------------
# Add tasks
# -------------------------------------------------------------------
st.subheader("Add Care Tasks")

if st.session_state.owner.pets:
    pet_options = {
        f"{pet.name} ({pet.species})": pet.pet_id
        for pet in st.session_state.owner.pets
    }

    with st.form("add_task_form"):
        selected_pet_label = st.selectbox("Choose pet", list(pet_options.keys()))
        task_title = st.text_input("Task title", value="Morning walk")
        description = st.text_input("Description", value="Daily exercise")
        scheduled_time = st.text_input("Scheduled time (HH:MM)", value="09:00")
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        frequency = st.selectbox("Frequency", ["one-time", "daily", "weekly"], index=1)
        add_task_submitted = st.form_submit_button("Add task")

    if add_task_submitted:
        selected_pet_id = pet_options[selected_pet_label]
        selected_pet = st.session_state.owner.get_pet_by_id(selected_pet_id)

        if selected_pet is not None and task_title.strip():
            task = Task(
                task_id=st.session_state.next_task_id,
                title=task_title.strip(),
                description=description.strip(),
                scheduled_time=scheduled_time.strip(),
                duration=int(duration),
                frequency=frequency,
                due_date=date.today(),
                completed=False,
            )
            selected_pet.add_task(task)
            st.session_state.next_task_id += 1
            st.success(f"Added task '{task.title}' to {selected_pet.name}")
        else:
            st.error("Please enter a valid task title.")
else:
    st.info("Add a pet before adding tasks.")

all_tasks = st.session_state.owner.get_all_tasks()
if all_tasks:
    st.markdown("### Current Tasks")
    task_table = []
    for pet in st.session_state.owner.pets:
        for task in pet.tasks:
            task_table.append(
                {
                    "Task ID": task.task_id,
                    "Task": task.title,
                    "Pet": pet.name,
                    "Description": task.description,
                    "Time": task.scheduled_time,
                    "Duration": task.duration,
                    "Frequency": task.frequency,
                    "Due Date": str(task.due_date),
                    "Completed": task.completed,
                }
            )
    st.table(task_table)
else:
    st.info("No tasks yet.")

st.divider()

# -------------------------------------------------------------------
# Generate schedule
# -------------------------------------------------------------------
st.subheader("Build Schedule")

if st.session_state.owner.pets:
    scheduler = Scheduler(st.session_state.owner)

    if st.button("Generate schedule"):
        schedule = scheduler.generate_schedule()
        conflicts = scheduler.detect_conflicts(schedule)

        st.success("Schedule generated.")
        st.markdown("### Today's Schedule")

        if schedule:
            schedule_table = []
            for pet_name, task in schedule:
                schedule_table.append(
                    {
                        "Time": task.scheduled_time,
                        "Pet": pet_name,
                        "Task": task.title,
                        "Duration": f"{task.duration} min",
                        "Frequency": task.frequency,
                        "Status": "Done" if task.completed else "Pending",
                    }
                )
            st.table(schedule_table)
        else:
            st.info("No tasks scheduled for today.")

        if conflicts:
            st.markdown("### Conflict Warnings")
            for warning in conflicts:
                st.warning(warning)

        st.markdown("### Terminal-Style View")
        st.text(scheduler.format_schedule_for_terminal())
else:
    st.info("Add at least one pet to build a schedule.")

st.divider()

# -------------------------------------------------------------------
# Filter tasks
# -------------------------------------------------------------------
st.subheader("Filter Tasks")

if st.session_state.owner.pets:
    scheduler = Scheduler(st.session_state.owner)
    all_tasks_with_pets = scheduler.sort_by_time(scheduler.get_todays_tasks())

    filter_option = st.selectbox(
        "Filter today's tasks by status",
        ["all", "pending", "completed"]
    )

    filtered_tasks = all_tasks_with_pets
    if filter_option == "pending":
        filtered_tasks = scheduler.filter_by_status(all_tasks_with_pets, completed=False)
    elif filter_option == "completed":
        filtered_tasks = scheduler.filter_by_status(all_tasks_with_pets, completed=True)

    if filtered_tasks:
        filtered_table = [
            {
                "Time": task.scheduled_time,
                "Pet": pet_name,
                "Task": task.title,
                "Status": "Done" if task.completed else "Pending",
            }
            for pet_name, task in filtered_tasks
        ]
        st.table(filtered_table)
    else:
        st.info("No tasks match that filter.")