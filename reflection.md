# PawPal+ Project Reflection

## 1. System Design

**a. Initial design** 

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

  User should be able to:
    - Track feeding
    - Get reminders for medicine
    - Book a Groomer/Grooming services

  Objects(Attributes): 
    - Owner 
        - Name
        - Address
    - Pet
        - Name
        - Age
        - Type of pet
            - Breed
    - Task
        - Name
        - Description
        - Duration
        - Priority at minimum
    - Planner 
        - Daily Plan/Schedule
        - Constraints
        - Priorities
        - Reasoning
    
    Objects(Methods):
    - Owner
        - Add owner information
        - Add pet information
    - Task
        - Create a new task
        - Edit a task
        - Delete a task
    - Planner 
        - Create a Daily Plan/Schedule
            - Consider Constraints
            - Consider Priorities
        - Provide Reasoning
        - Display

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

- I made many changes due to Claude pointing many issues in my skeleton design. My skeleton class was missing two relationships. My uml design says owner owns pets and pets have care tasks, but in my skeleton owner had no pets field and pet had no task fields. The add_pet_information method had no collection to update. The Tasks methods were missing many details, such as parameters and correct return types.


---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

- My scheduler considers whether a task is completed, its scheduled start time, and its numeric priority. Completed tasks are excluded, timed tasks are ordered earliest first, and unscheduled tasks come after them. If two tasks have the same time, the higher-priority task comes first.
- I prioritized completion status first so finished care tasks do not appear again, then scheduled time so tasks are shown when they are intended to happen. Priority is a tie-breaker because the current scheduler does not yet model time availability or resolve conflicts. Task duration and frequency are stored, but preferences and recurring schedules are not yet enforced.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

- The scheduler checks each pair of scheduled tasks for overlaps instead of using a more complex scheduling method. This is reasonable because a pet owner's daily schedule is small, so the check is easy to understand and works well. It does not account for tasks without a start time, travel time, or tasks that cross midnight.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

- I used Claude and Copilot to help with system design, code review, and documentation.  When working on the skeleton AI was very helpful. Claude was able to point out many things I missed. I was missing some relationships and some fields. It also pointed out I did not set the data types for my attribute, which I was then able to fix. It helped me refactor my classes to implement the relationships. The fix changed my methods to correctly implement the methods so that the owner had a pet field and the pet have a tasks field. Claude also helped me as a code reviewer for me and was able to help me check that all required implementations were correct.
- The uml design prompt was helpful since it helped me visualize my proposed design in a fast way. My prompts to check if my implementation were correct was helpful in mitigating issues.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

- When I first as AI to review my skeleton it gave me suggestions that were more complex than I wanted. I then had to ask AI to simplify the changes it wanted to make, because I wanted to make sure I can understand the code it was trying to add. I verified that I was able to understand all the suggestions and the reasoinings behind them

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

- I tested adding pets and tasks, preventing the same pet from being added twice, collecting an owner’s tasks, and editing and deleting tasks. These tests check that the basic data relationships and task operations work. I tested schedule sorting, including placing unscheduled tasks last and using priority to break ties. I also checked that completed and future-dated tasks are excluded while tasks due today or without a due date are included. I tested filtering tasks by completion status and pet name, detecting overlapping tasks (including tasks with the same start time), and creating the next daily or weekly task after completion.
These tests matter because they cover the main scheduling rules and common actions that the app depends on. The current test suite has 11 tests and has passed.

- I am fairly confident in the behaviors covered by the tests, but the test suite does not cover every possible schedule or edge case. If I had more time, I would test tasks that end exactly when another begins, tasks that cross midnight, overdue tasks, and attempts to complete a task that does not belong to the owner. I would also test that completing an already-completed recurring task does not create another occurrence.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

- I’m most satisfied that I turned the initial class design into a working system where owners can manage pets and their care tasks, and the scheduler can build an ordered daily plan. It has been a long time since I started a project from almost scratch to a working product. I am happy I went through all development stages from design to logic to UI to testing. 

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

- If I had another iteration, I would improve the scheduler so it could do more than warn about overlapping tasks. It could use task duration and the owner’s available time to suggest better start times. I would also add UI controls for marking tasks complete and setting due dates and recurrence, since those behaviors currently exist only in the scheduler logic. 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

- I learned how useful AI can be when it comes to designing systems. A quick request is able to make a diagrahm that it would probably take me a long time to make. Also, using AI to review my code allowed me to catch mistake and errors before they became a bigger issue.
