# Starting Business Brief — Field Repair Tracker

> We need a system where field technicians can log repair jobs from their phones. A manager should be able to see all the jobs and assign them to technicians. We also want some kind of notification when a job gets assigned. It should be fast and work offline sometimes.

## Stakeholder Answers (reveal only after asking clarification questions)

- A field technician may view and update only their own jobs and cannot assign other technicians.
- A service manager may view all jobs, assign any job to any technician, and generate a daily summary report.
- A job includes site address, fault description, priority (low/medium/high/critical), and optional photo.
- Offline means viewing currently assigned jobs without connectivity; creating jobs requires connectivity.
- Performance target: 95% of API requests within 300 ms at 200 concurrent users.

Reference: https://book.agentic-swe.dev/tutorial_6.html
