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
Yes, the design changed during implementation.
I simplified the system to better match the assignment requirements.

Main changes:

Removed TaskManager and stored tasks directly inside Pet
Replaced CareTask with a simpler Task class
Made Owner → Pets → Tasks the main structure (single source of truth)
Simplified Scheduler to directly pull tasks from Owner
Added completed field and time-based scheduling (HH:MM)
Added recurrence logic and conflict detection

Reason:

The original design was over-engineered for the assignment
Simplifying improved clarity and made testing + UI integration easier
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
a. Constraints and priorities

The scheduler considers:

Task scheduled time
Task completion status
Task frequency (daily / weekly)
Tasks due today

Priority decision:

Time-based ordering was treated as the most important constraint
Simpler than balancing multiple weights and fits the use case
- Why is that tradeoff reasonable for this scenario?
b. Tradeoffs
The scheduler uses exact time matching for conflict detection (e.g., both at 09:00)
It does not handle overlapping durations (e.g., 09:00–09:30 vs 09:15–09:45)

Why this is reasonable:

Keeps logic simple and easy to implement
Matches assignment scope without overcomplicating scheduling

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

Used AI for:
Structuring the system design
Refactoring code to simplify architecture
Debugging test failures
Generating test cases and improving coverage
Helpful prompts were:
“Align this with assignment requirements”
“Simplify this design”
“Fix this test to match new architecture”

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
I did not blindly accept AI suggestions.
Example:
Initially AI supported a complex TaskManager design
I later rejected it after checking assignment requirements
Verified changes by:
Running tests (pytest)
Checking if design matches assignment wording
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?
a. What I tested
Task completion updates status correctly
Adding a task increases a pet’s task count
Tasks are sorted correctly by time
Recurring tasks are generated after completion
Conflict detection works for same-time tasks

Why important:

These cover the core scheduling behavior
Ensures both correctness and assignment requirements
**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?
I am fairly confident the scheduler works correctly for expected cases
Core flows (add → schedule → display) work end-to-end

Edge cases to test next:

Invalid time formats (e.g., “9am” instead of “09:00”)
Multiple recurring chains over many days
Overlapping time ranges (not just exact match)
Large number of tasks
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
Simplifying the architecture was the biggest win
The final model (Owner → Pet → Task → Scheduler) is clean and easy to reason about
Tests and Streamlit integration worked smoothly after refactor
**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
Add better time handling (actual datetime instead of strings)
Improve scheduling logic to handle overlaps and priorities together
Add edit/delete features in the UI
Persist data (instead of only session state)

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
A simpler design that matches requirements is better than an over-engineered one
AI is most useful when used iteratively and critically, not blindly