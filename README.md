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

PawPal+ uses dataclasses for `Owner`, `Pet`, and `Task`. An `Owner` manages multiple pets and can collect their tasks together; each `Pet` stores its care tasks. `Scheduler` retrieves tasks through the owner's collection, leaves completed tasks out of the schedule, and orders remaining tasks by scheduled time, using priority to break ties. Tasks also store their frequency. The `main.py` script demonstrates a schedule across two pets.

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

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

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
# Paste your pytest output here
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Behavior |
|---------|-----------|----------|
| Sorting | `Scheduler.sort_by_time()` | Orders tasks by scheduled start time, puts tasks without a start time last, and uses higher priority to break ties. |
| Filtering | `Scheduler.filter_tasks()` | Filters by completion status, pet name, or both. Pet names are matched exactly without case sensitivity. |
| Conflict detection | `Scheduler.detect_conflicts()` | Checks scheduled task start times and durations for overlaps, returning warning messages instead of stopping schedule generation. Tasks without a start time are skipped. `Scheduler.create_daily_schedule()` stores these messages in `conflict_warnings`. |
| Recurring tasks | `Scheduler.mark_task_completed()` | Completing a daily or weekly task creates a new task instance due one or seven days later. `Scheduler.create_daily_schedule()` leaves future-dated instances out until they are due. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
