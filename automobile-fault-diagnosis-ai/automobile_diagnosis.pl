% Automobile Fault Diagnosis System
% CO5 AT3 - Modelling Comparative Analysis
% Course: Artificial Intelligence and Expert Systems
% Course Code: MLA01

% --------------------------------------------------
% FACTS
% --------------------------------------------------

% Vehicle
vehicle(car1).

% Observed symptoms
overheating(car1).
starting_failure(car1).
abnormal_noise(car1).
low_mileage(car1).
warning_on(car1).

% --------------------------------------------------
% BASIC DIAGNOSTIC RULES
% --------------------------------------------------

% Overheating indicates a possible cooling-system fault.
cooling_fault(X) :-
    overheating(X).

% Starting failure indicates a possible battery fault.
battery_fault(X) :-
    starting_failure(X).

% Abnormal engine noise indicates a possible engine fault.
engine_fault(X) :-
    abnormal_noise(X).

% Low mileage indicates a possible fuel-system fault.
fuel_fault(X) :-
    low_mileage(X).

% Warning indicator indicates a possible sensor/system fault.
sensor_fault(X) :-
    warning_on(X).

% --------------------------------------------------
% COMBINED DIAGNOSTIC RULES
% --------------------------------------------------

% Overheating together with warning indicator
% strongly indicates a cooling-system fault.
cooling_fault_high(X) :-
    overheating(X),
    warning_on(X).

% Starting failure together with warning indicator
% indicates a possible electrical fault.
electrical_fault(X) :-
    starting_failure(X),
    warning_on(X).

% Abnormal noise together with low mileage
% indicates a possible engine-performance fault.
engine_performance_fault(X) :-
    abnormal_noise(X),
    low_mileage(X).

% --------------------------------------------------
% GENERAL DIAGNOSIS
% --------------------------------------------------

% A vehicle has a possible fault if any of the
% diagnostic conditions are satisfied.
possible_fault(X, cooling_system_fault) :-
    cooling_fault(X).

possible_fault(X, battery_fault) :-
    battery_fault(X).

possible_fault(X, engine_fault) :-
    engine_fault(X).

possible_fault(X, fuel_system_fault) :-
    fuel_fault(X).

possible_fault(X, sensor_system_fault) :-
    sensor_fault(X).

possible_fault(X, electrical_fault) :-
    electrical_fault(X).

% --------------------------------------------------
% END OF PROGRAM
% --------------------------------------------------