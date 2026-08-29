% medical_expert.pl
% Rule-Based Medical Diagnosis Expert System
% Tool: SWI-Prolog
% Demonstrates facts, production rules, forward chaining,
% backward chaining, unification and backtracking.
%
% NOTE: Educational demonstration only. It is NOT a medical diagnostic tool.

:- dynamic fact/1.

% -------------------------
% Knowledge Base
% -------------------------

disease(common_cold).
disease(flu).
disease(migraine).
disease(food_poisoning).
disease(allergy).
disease(pneumonia).

% IF-THEN production rules
rule(flu, [
    symptom(fever),
    symptom(cough),
    symptom(body_ache),
    symptom(fatigue)
]).

rule(common_cold, [
    symptom(sneezing),
    symptom(runny_nose),
    symptom(sore_throat)
]).

rule(migraine, [
    symptom(severe_headache),
    symptom(nausea),
    symptom(light_sensitivity)
]).

rule(food_poisoning, [
    symptom(vomiting),
    symptom(diarrhea),
    symptom(abdominal_pain)
]).

rule(allergy, [
    symptom(sneezing),
    symptom(itchy_eyes),
    symptom(runny_nose)
]).

rule(pneumonia, [
    symptom(fever),
    symptom(cough),
    symptom(shortness_of_breath),
    symptom(chest_pain)
]).

action(flu, consult_doctor_if_severe).
action(flu, rest_and_hydrate).
action(common_cold, rest_and_hydrate).
action(common_cold, monitor_symptoms).
action(migraine, rest_in_dark_quiet_room).
action(migraine, consult_healthcare_professional).
action(food_poisoning, maintain_hydration).
action(food_poisoning, seek_medical_help_if_severe).
action(allergy, avoid_known_allergens).
action(allergy, consult_healthcare_professional_if_persistent).
action(pneumonia, seek_prompt_medical_evaluation).

% -------------------------
% Backward Chaining
% -------------------------

backward_chain(Goal, Facts, Trace) :-
    prove(Goal, Facts, Trace).

prove(Goal, Facts, goal(Goal, fact)) :-
    memberchk(Goal, Facts), !.

prove(Goal, Facts, goal(Goal, rule(Goal, Traces))) :-
    rule(Goal, Conditions),
    prove_conditions(Conditions, Facts, Traces).

prove_conditions([], _, []).
prove_conditions([C|Cs], Facts, [goal(C, fact)|Traces]) :-
    memberchk(C, Facts),
    prove_conditions(Cs, Facts, Traces).

% -------------------------
% Forward Chaining
% -------------------------

forward_chain(Facts, Conclusions) :-
    forward_step(Facts, Facts, Conclusions).

forward_step(Known, Original, Conclusions) :-
    findall(D,
        (rule(D, Conditions),
         disease(D),
         all_present(Conditions, Known),
         \+ memberchk(D, Known)),
        NewDiseases),
    ( NewDiseases = [] ->
        Conclusions = Known
    ;   append(Known, NewDiseases, Next),
        forward_step(Next, Original, Conclusions)
    ).

all_present([], _).
all_present([X|Xs], Facts) :-
    memberchk(X, Facts),
    all_present(Xs, Facts).

% -------------------------
% Diagnosis Interface
% -------------------------

diagnose(Facts, Diagnoses) :-
    findall(D,
        (disease(D), rule(D, Conditions), all_present(Conditions, Facts)),
        Diagnoses).

recommendations(Diagnoses, Actions) :-
    findall(A,
        (member(D, Diagnoses), action(D, A)),
        Raw),
    sort(Raw, Actions).

% -------------------------
% Demonstration Test Cases
% -------------------------

test_case(1,
    [symptom(fever), symptom(cough), symptom(body_ache), symptom(fatigue)],
    [flu]).

test_case(2,
    [symptom(sneezing), symptom(runny_nose), symptom(sore_throat)],
    [common_cold]).

test_case(3,
    [symptom(severe_headache), symptom(nausea), symptom(light_sensitivity)],
    [migraine]).

test_case(4,
    [symptom(vomiting), symptom(diarrhea), symptom(abdominal_pain)],
    [food_poisoning]).

test_case(5,
    [symptom(fever), symptom(cough), symptom(shortness_of_breath), symptom(chest_pain)],
    [pneumonia]).

run_test_case(N) :-
    test_case(N, Facts, Expected),
    diagnose(Facts, Diagnoses),
    forward_chain(Facts, Forward),
    recommendations(Diagnoses, Actions),
    format('~nTest Case ~w~n', [N]),
    format('Facts: ~w~n', [Facts]),
    format('Expected diagnosis: ~w~n', [Expected]),
    format('Diagnosis: ~w~n', [Diagnoses]),
    format('Forward-chain conclusions: ~w~n', [Forward]),
    format('Recommended actions: ~w~n', [Actions]),
    (Diagnoses == Expected -> writeln('Result: PASS') ; writeln('Result: CHECK')).

run_all_tests :-
    forall(between(1,5,N), run_test_case(N)).
