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

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

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
