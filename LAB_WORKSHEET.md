# Lab Worksheet — Submit These Deliverables

## Activity 1: Requirements Engineering (~30–40 minutes)

1. Give your AI the starting brief from `specs/business_brief.md` (without showing stakeholder answers first).
2. Ask it to list ambiguities and stakeholder questions.
3. Reveal the stakeholder answers and ask for at least **five** functional and **three measurable** non-functional requirements.
4. Audit requirements using: correct, unambiguous, complete, consistent, verifiable, traceable, prioritised (Pass/Partial/Fail).
5. Produce 3–4 epics, four job lifecycle user stories, and three Gherkin scenarios for job assignment.
6. Save outputs in `deliverables/requirements.md` and `deliverables/assign_job.feature`.

## Activity 2: Software Design (~30–40 minutes)

1. Use your refined requirements to ask AI for a use-case diagram in Mermaid.
2. Ask for a class diagram, at least one design pattern, and a SOLID critique.
3. Ask for a sequence diagram of Assign Job including JWT check, repository persistence, asynchronous notification and response.
4. Independently check actor boundaries, traceability, SOLID, and whether notification blocks the response.
5. Save Mermaid source in `deliverables/use_case.mmd`, `class_diagram.mmd`, `sequence_diagram.mmd`.

## Activity 3: Specification-Driven Coding (~40–50 minutes)

1. Read `spec_assign_job.md` and inspect the starter code.
2. Ask your AI agent to implement exactly the four requested layers plus an adapter to the supplied `SeedStore`.
3. Run `uv run pytest tests/test_assign_contract.py -q`; fix failures.
4. Write at least one new test that verifies a notification is scheduled after success, not after failure.
5. Review: correctness, type hints, dependency injection, non-blocking notification, HTTP codes, no global mutable state.
6. Save a brief AI-review log to `deliverables/review_notes.md`.

## Submission Checklist

- [ ] `requirements.md` and `assign_job.feature`
- [ ] Three diagrams as `.mmd` files
- [ ] Assign Job API implementation
- [ ] All contract tests passing
- [ ] Notification test and a short review log
- [ ] A short paragraph naming two remaining design risks

## Suggested Prompt for Activity 3

> Read `spec_assign_job.md`, the requirements and diagrams created, and the starter code. Implement only the Assign Job use case in the specified layered architecture. Reuse the signed-JWT dependency and SeedStore provided by the starter. Do not modify the provided contract tests. Explain any assumptions and run the tests.
