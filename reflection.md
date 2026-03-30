# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**
core tasks:
1. Add / Manage Pet & Owner Info
2. Create / Edit Care Tasks
3. Generate & View Daily Plan
- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

- Owner
    - Stores owner details (name, available time, preferences)
    - Provides constraints that influence scheduling
- Pet
    - Stores pet information (name, species, age, needs)
    - Helps tailor tasks based on pet requirements
- CareTask
    - Represents a single care activity (walk, feed, meds, etc.)
    - Stores duration, priority, and other task details
    - Core unit used in scheduling
- TaskManager
    - Manages all tasks (add, edit, delete, retrieve)
    - Keeps task-related logic separate from scheduling
- Scheduler
    - Main decision-making component (“brain” of the system)
    - Uses tasks + constraints to generate a daily plan
    - Prioritizes tasks and ensures time limits are respected
- DailyPlan
    - Stores the final schedule for the day
    - Contains selected tasks and total duration
    - May include explanation of decisions
**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
- Add completed: bool = False to CareTask
- Decide one source of truth for available time
- Avoid storing tasks separately in both TaskManager and Scheduler
- Add a pet-task link like pet_id
- Change special_needs from str to a list if you want add/remove methods
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
