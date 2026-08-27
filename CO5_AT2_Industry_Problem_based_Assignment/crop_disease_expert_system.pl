% ============================================================
% SIMATS ENGINEERING - MLA01 Artificial Intelligence & Expert Systems
% CO5 Assessment Tool 2 - Industry Problem-Based Assignment
% Crop-Disease Advisory Expert System
% Compatible with SWI-Prolog
% ============================================================

:- dynamic known/1.

% -------------------------
% Knowledge Base
% -------------------------
% Crop facts
crop(tomato).
crop(rice).
crop(cotton).

% Soil facts
soil(loamy).
soil(clayey).
soil(sandy).

% Weather facts
weather(humid).
weather(warm_humid).
weather(wet).
weather(hot_dry).

% Disease facts and advisory actions
disease(late_blight).
disease(early_blight).
disease(bacterial_spot).
disease(rice_blast).
disease(brown_spot).
disease(aphid_infestation).
disease(bollworm_infestation).

% Production-style rules:
% disease(Disease, Crop, RequiredConditions, Action)
rule(late_blight,
     [crop(tomato), weather(wet), symptom(water_soaked_spots),
      symptom(leaf_browning), symptom(wilting)],
     [action(remove_affected_leaves),
      action(improve_air_circulation),
      action(avoid_overhead_irrigation),
      action(consult_local_extension_for_fungicide)]).

rule(early_blight,
     [crop(tomato), weather(warm_humid), symptom(concentric_leaf_spots),
      symptom(yellow_leaves), symptom(lower_leaf_damage)],
     [action(remove_plant_debris),
      action(crop_rotation),
      action(improve_field_airflow),
      action(consult_local_extension_for_fungicide)]).

rule(bacterial_spot,
     [crop(tomato), weather(wet), symptom(small_dark_spots),
      symptom(yellow_halo), symptom(leaf_drop)],
     [action(use_clean_seed_or_transplants),
      action(avoid_working_when_foliage_is_wet),
      action(sanitize_tools),
      action(consult_local_extension)]).

rule(rice_blast,
     [crop(rice), weather(warm_humid), symptom(spindle_shaped_spots),
      symptom(gray_centers), symptom(yellowing)],
     [action(use_resistant_variety),
      action(avoid_excess_nitrogen),
      action(field_monitoring),
      action(consult_local_extension_for_fungicide)]).

rule(brown_spot,
     [crop(rice), soil(sandy), symptom(brown_leaf_spots),
      symptom(yellowing), symptom(poor_growth)],
     [action(improve_nutrient_management),
      action(improve_water_management),
      action(use_clean_seed),
      action(consult_local_extension)]).

rule(aphid_infestation,
     [crop(cotton), weather(hot_dry), symptom(curling_leaves),
      symptom(sticky_honeydew), symptom(small_insects)],
     [action(monitor_aphid_population),
      action(conserve_natural_enemies),
      action(remove_heavily_infested_parts),
      action(use_ipm_threshold_based_control)]).

rule(bollworm_infestation,
     [crop(cotton), symptom(chewed_bolls), symptom(frass),
      symptom(caterpillar_present)],
     [action(field_scouting),
      action(remove_infested_material),
      action(use_trap_or_biological_control_where_appropriate),
      action(use_ipm_threshold_based_control)]).

% -------------------------
% Simple disease advisory
% -------------------------
diagnose(Facts, Disease, Actions) :-
    rule(Disease, Conditions, Actions),
    subset_list(Conditions, Facts).

subset_list([], _).
subset_list([H|T], Facts) :-
    memberchk(H, Facts),
    subset_list(T, Facts).

% -------------------------
% Explicit Forward Chaining
% -------------------------
forward_chain(InitialFacts, FinalFacts, Conclusions) :-
    forward_loop(InitialFacts, InitialFacts, FinalFacts, Conclusions).

forward_loop(Facts, Seen, FinalFacts, Conclusions) :-
    findall(Disease,
            (rule(Disease, Conditions, _),
             subset_list(Conditions, Facts)),
            Ds0),
    sort(Ds0, Ds),
    subtract(Ds, Seen, NewDiseases),
    ( NewDiseases == [] ->
        FinalFacts = Facts,
        Conclusions = Seen
    ;   append(Facts, NewDiseases, UpdatedFacts),
        append(Seen, NewDiseases, UpdatedSeen),
        forward_loop(UpdatedFacts, UpdatedSeen, FinalFacts, Conclusions)
    ).

% -------------------------
% Explicit Backward Chaining
% -------------------------
backward_chain(Goal, Facts, Trace) :-
    prove(Goal, Facts, [], Trace).

prove(Goal, Facts, Visited, [goal(Goal, fact)|Visited]) :-
    memberchk(Goal, Facts), !.

prove(Goal, Facts, Visited, [goal(Goal, rule(RuleId))|Rest]) :-
    rule(RuleId, Conditions, _),
    memberchk(RuleId, Visited), !, fail.

prove(Goal, Facts, Visited, [goal(Goal, rule(RuleId)), conditions(ConditionTraces)|Rest]) :-
    rule(RuleId, Conditions, _),
    prove_all(Conditions, Facts, [RuleId|Visited], ConditionTraces),
    Rest = [].

prove_all([], _, _, []).
prove_all([C|Cs], Facts, Visited, [C-Trace|Rest]) :-
    prove(C, Facts, Visited, Trace),
    prove_all(Cs, Facts, Visited, Rest).

% -------------------------
% Recommendation
% -------------------------
recommend(Facts, Disease, Actions) :-
    diagnose(Facts, Disease, Actions).

% -------------------------
% Sample Test Cases
% -------------------------
test_case(1, Facts) :-
    Facts = [crop(tomato), weather(wet),
             symptom(water_soaked_spots), symptom(leaf_browning),
             symptom(wilting)].

test_case(2, Facts) :-
    Facts = [crop(tomato), weather(warm_humid),
             symptom(concentric_leaf_spots), symptom(yellow_leaves),
             symptom(lower_leaf_damage)].

test_case(3, Facts) :-
    Facts = [crop(rice), weather(warm_humid),
             symptom(spindle_shaped_spots), symptom(gray_centers),
             symptom(yellowing)].

test_case(4, Facts) :-
    Facts = [crop(rice), soil(sandy),
             symptom(brown_leaf_spots), symptom(yellowing),
             symptom(poor_growth)].

test_case(5, Facts) :-
    Facts = [crop(cotton), weather(hot_dry),
             symptom(curling_leaves), symptom(sticky_honeydew),
             symptom(small_insects)].

run_tests :-
    forall(test_case(N, Facts),
           ( format('~nTest Case ~w~nFacts: ~w~n', [N, Facts]),
             findall(D-A, diagnose(Facts,D,A), Results),
             format('Diagnosis and actions: ~w~n', [Results]),
             forward_chain(Facts, _, Conclusions),
             format('Forward-chain conclusions: ~w~n', [Conclusions])
           )).

% Example queries:
% ?- test_case(1, F), diagnose(F, D, A).
% ?- test_case(3, F), forward_chain(F, Final, Conclusions).
% ?- backward_chain(rice_blast,
%       [crop(rice), weather(warm_humid),
%        symptom(spindle_shaped_spots), symptom(gray_centers),
%        symptom(yellowing)], Trace).
%
% Unification example:
% ?- rule(D, Conditions, Actions).
% Backtracking gives alternative matching rules.
%
% NOTE:
% The advisory is educational and should not replace diagnosis by a
% qualified agricultural extension officer or plant pathologist.
