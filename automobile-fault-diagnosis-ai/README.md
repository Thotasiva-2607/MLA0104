# Automobile Fault Diagnosis Using AI

## CO5 AT3 - Modelling Comparative Analysis

### Course

**Artificial Intelligence and Expert Systems**

**Course Code:** MLA01

---

## 1. Project Overview

This project presents an intelligent knowledge-based model
for automobile fault diagnosis.

The system identifies possible vehicle faults from observed
symptoms such as:

- Engine overheating
- Starting failure
- Abnormal engine noise
- Low mileage
- Warning indicator being ON

The same automobile diagnostic problem is represented using
four different knowledge modelling approaches:

1. Production Rules
2. Propositional Logic
3. First-Order Logic
4. Prolog

Forward chaining and backward chaining are also demonstrated
to explain the reasoning process.

---

## 2. Objectives

The main objectives of this project are:

- To identify important automobile symptoms and faults.
- To represent automobile knowledge using production rules.
- To model diagnostic conditions using propositional logic.
- To represent entities, properties and relationships using
  First-Order Logic.
- To implement the knowledge base using Prolog.
- To demonstrate forward and backward chaining.
- To compare the four modelling approaches.
- To identify the most suitable approach for automobile
  fault diagnosis.

---

## 3. Domain

The automobile fault-diagnosis domain contains:

- Vehicles
- Engines
- Batteries
- Cooling systems
- Fuel systems
- Sensors
- Warning indicators
- Vehicle symptoms
- Possible diagnostic faults

---

## 4. Symptoms Considered

The current knowledge base considers the following symptoms:

| Symptom | Possible Diagnostic Conclusion |
|---|---|
| Engine overheating | Cooling-system fault |
| Starting failure | Battery fault |
| Abnormal engine noise | Engine/mechanical fault |
| Low mileage | Fuel-system fault |
| Warning indicator ON | Sensor/system fault |

---

## 5. Knowledge Representation Models

### Production Rules

Production rules represent knowledge using IF-THEN
statements.

Example:

```text
IF engine is overheating
THEN cooling-system fault is suspected.