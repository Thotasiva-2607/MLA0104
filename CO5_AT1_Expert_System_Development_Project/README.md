# Medical Diagnosis Expert System

## Project
A rule-based medical diagnosis expert system developed in SWI-Prolog for the SIMATS Engineering CO5 Expert System Development Project.

> Educational project only. The system does not replace a qualified medical professional.

## Features
- Prolog facts and production rules
- Backward chaining
- Forward chaining
- Unification through Prolog's logical matching
- Backtracking
- Diagnosis and recommendation generation
- Five industry-based test cases

## Requirements
- SWI-Prolog
- Windows/Linux/macOS

## How to Run

1. Install SWI-Prolog.
2. Open SWI-Prolog.
3. Load the program:

```prolog
?- consult('medical_expert.pl').
```

4. Run individual tests:

```prolog
?- run_test_case(1).
?- run_test_case(2).
?- run_test_case(3).
?- run_test_case(4).
?- run_test_case(5).
```

5. Run all tests:

```prolog
?- run_all_tests.
```

6. Direct diagnosis example:

```prolog
?- diagnose([symptom(fever), symptom(cough), symptom(body_ache), symptom(fatigue)], D).
```

Expected:
```text
D = [flu].
```

7. Backward-chaining demonstration:

```prolog
?- backward_chain(
       flu,
       [symptom(fever), symptom(cough), symptom(body_ache), symptom(fatigue)],
       Trace).
```

8. Forward-chaining demonstration:

```prolog
?- forward_chain(
       [symptom(fever), symptom(cough), symptom(body_ache), symptom(fatigue)],
       Conclusions).
```

## Repository Structure

```text
Medical_Expert_System/
├── medical_expert.pl
├── README.md
├── test_cases.txt
├── screenshots/
│   └── README.txt
├── report/
│   └── Medical_Diagnosis_Expert_System_Report.docx
└── presentation/
    └── Medical_Diagnosis_Expert_System_Presentation.pptx
```

## Production Rule Example

IF fever AND cough AND body_ache AND fatigue
THEN flu.

In Prolog:
```prolog
rule(flu, [
    symptom(fever),
    symptom(cough),
    symptom(body_ache),
    symptom(fatigue)
]).
```

## Procedural vs Non-Procedural
The system is primarily declarative/non-procedural because the knowledge is represented as facts and rules. The programmer specifies what relationships hold rather than writing a fixed sequence of diagnostic steps. Prolog's inference engine determines how rules are matched and explored.

## GitHub
Create a repository and upload all files from this folder. Suggested repository name:

`medical-diagnosis-expert-system-prolog`

After creating it, paste your GitHub repository URL into the final report.
