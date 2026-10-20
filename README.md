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

## Implementation Summary

PawPal+ uses dataclasses for `Owner`, `Pet`, and `Task`. An `Owner` manages multiple pets and can collect their tasks together; each `Pet` stores its care tasks. `Scheduler` retrieves tasks through the owner's collection, leaves completed tasks out of the schedule, and orders remaining tasks by priority first, then scheduled time. `Task.priority` uses 1 for Low, 2 for Medium, and 3 for High; `Task.priority_level` provides the display label. Tasks also store their frequency. The `main.py` script demonstrates a schedule across two pets.

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

```
Today's Schedule
----------------
07:30 AM | Mochi | Breakfast: Serve Mochi's morning meal (10 min, priority 2)
08:00 AM | Biscuit | Morning walk: Walk around the neighborhood (25 min, priority 3)
06:00 PM | Mochi | Medication: Give Mochi the prescribed medicine (5 min, priority 1)
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
===================================== test session starts ======================================
platform win32 -- Python 3.14.7, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\ari14\Desktop\codepath\ai110-module2show-pawpal-starter
plugins: anyio-4.15.1
collected 15 items

tests\test_pawpal.py ...............                                                      [100%]

====================================== 15 passed in 0.07s ======================================

```

Confidence Level: 4/5 stars. All 15 tests pass, covering core task and owner behavior, JSON persistence, priority-based schedule ordering, recurrence, filtering, and conflict detection. This is solid confidence in the tested logic, though it is not a substitute for broader integration testing or a coverage report.

## 📐 Smarter Scheduling

| Feature | Method(s) | Behavior |
|---------|-----------|----------|
| Sorting | `Scheduler.sort_by_time()` | Orders tasks by descending priority, then scheduled start time; within each priority, tasks without a start time go last. |
| Filtering | `Scheduler.filter_tasks()` | Filters by completion status, pet name, or both. Pet names are matched exactly without case sensitivity. |
| Conflict detection | `Scheduler.detect_conflicts()` | Checks scheduled task start times and durations for overlaps, returning warning messages instead of stopping schedule generation. Tasks without a start time are skipped. `Scheduler.create_daily_schedule()` stores these messages in `conflict_warnings`. |
| Recurring tasks | `Scheduler.mark_task_completed()` | Completing a daily or weekly task creates a new task instance due one or seven days later. `Scheduler.create_daily_schedule()` leaves future-dated instances out until they are due. |

## 📸 Demo Walkthrough

### Main UI Features

The Streamlit app lets an owner add pets with a name, species, age, and breed. After adding a pet, the owner can create care tasks for that pet by entering a title, description, duration, priority, and preferred start time. The task list can be filtered to show all tasks, tasks to do, or completed tasks. Selecting **Generate schedule** builds today's plan and displays each task with its pet, duration, priority, and start time. The page also shows overlap warnings and the scheduler's explanation when a plan is generated.

### Example Workflow

1. Add Mochi as a cat and enter Mochi's age and breed.
2. Select Mochi and add a breakfast task with its duration, priority, and preferred start time.
3. Add another pet, such as Biscuit, and create a morning walk task. If tasks overlap, the scheduler will report a warning.
4. Select **Generate schedule** to see today's tasks ordered by priority, then time, along with any warnings and the scheduling rationale.

### Scheduler Behaviors

- **Daily schedule:** Includes incomplete tasks that have no due date or are due today or earlier; future-dated and completed tasks are excluded.
- **Priority-based scheduling:** High priority tasks come before Medium and Low tasks, even when their scheduled time is later. Within a priority level, earlier start times come first and unscheduled tasks go last.
- **Filtering:** Tasks can be filtered by completion status and pet name. Pet-name matching is exact and case-insensitive.
- **Conflict warnings:** Scheduled tasks are checked for overlap using their start times and durations. Tasks without a start time are skipped, and overlaps produce warnings rather than stopping schedule generation.
- **Recurrence:** The scheduler logic can create a new task due one or seven days later when a daily or weekly task is marked complete. The current UI does not expose task-completion or recurrence controls.

Running `python main.py` prints this sample CLI schedule:

**Original output:**
```
Today's Schedule
----------------
07:30 AM | Biscuit | Morning walk: Walk around the neighborhood (25 min, priority 3)
07:30 AM | Mochi | Breakfast: Serve Mochi's morning meal (10 min, priority 2)
06:00 PM | Mochi | Medication: Give Mochi the prescribed medicine (5 min, priority 1)

Warnings
Warning: 'Morning walk' overlaps with 'Breakfast'.
```

**Priority based enhanced:**
```
Today's Schedule
----------------
08:30 AM | Biscuit | Morning walk: Walk around the neighborhood (25 min, priority High)
07:30 AM | Mochi | Breakfast: Serve Mochi's morning meal (10 min, priority Medium)
06:00 PM | Mochi | Medication: Give Mochi the prescribed medicine (5 min, priority Low)

The morning walk appears first despite starting later than breakfast because it has High priority.
```

### Data Persistence

PawPal+ stores owner, pet, and task data in `data.json` in the project directory. The Streamlit app loads this file when a session starts and saves it whenever a pet or task is added, so the data is available again after restarting the app.

`Owner.save_to_json()` converts the dataclasses into dictionaries and writes JSON using Python's built-in `json` module. Scheduled times and due dates are stored as ISO-formatted strings and converted back to `time` and `date` objects by `Owner.load_from_json()`. No additional serialization library is required. The generated `data.json` is listed in `.gitignore` to keep local pet data out of version control.

Files modified: `pawpal_system.py` adds the save/load methods, `app.py` loads and saves data during the Streamlit workflow, `tests/test_pawpal.py` verifies the JSON round trip, `.gitignore` excludes the generated data file, and `README.md` documents the workflow.


### Professional UI and Output Formatting
The task list and daily schedule use Streamlit’s st.table to present care tasks in organized columns. Task names include an emoji based on their type, such as a walking icon for walks or a pill for medication. Priorities use colored indicators: red for High, yellow for Medium, and green for Low. Task statuses use a check mark for Completed and an orange marker for To do.

The shared formatting functions format_task_name, format_priority, and format_status are defined in pawpal_formatting.py. The Streamlit UI and CLI reuse these helpers, so their labels stay consistent.

```
Today's Schedule
----------------
08:30 AM | Biscuit | 🚶 Morning walk: Walk around the neighborhood (25 min, 🔴 High)
07:30 AM | Mochi | 🍽️ Breakfast: Serve Mochi's morning meal (10 min, 🟡 Medium)
06:00 PM | Mochi | 💊 Medication: Give Mochi the prescribed medicine (5 min, 🟢 Low)

Reasoning
Completed tasks are excluded; remaining tasks are ordered by descending priority, then scheduledtime.
```