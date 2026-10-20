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

- One tradeoff is that scheduled time takes precedence over priority: an earlier task appears first even if a later task has a higher priority.
- This is reasonable because some care activities, such as medication, may need to happen at intended times. Priority still helps order tasks scheduled for the same time. 

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

- When working on the skeleton AI was very helpful. Claude was able to point out many things I missed. I was missing some relationships and some fields. It also pointed out I did not set the data types for my attribute, which I was then able to fix. It helped me refactor my classes to implement the relationships. The fix changed my methods to correctly implement the methods so that the owner had a pet field and the pet have a tasks field. Claude also helped me as a code reviewer for me and was able to help me check that all required implementations were correct.
- The uml design prompt was helpful since it helped me visualize my proposed design in a fast way. My prompts to check if my implementation were correct was helpful in mitigating issues.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

- When I first as AI to review my skeleton it gave me suggestions that were more complex than I wanted. I then had to ask AI to simplify the changes it wanted to make, because I wanted to make sure I can understand the code it was trying to add. I verified that I was able to understand all the suggestions and the reasoinings behind them.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
