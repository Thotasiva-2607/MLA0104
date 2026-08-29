% Cybersecurity Threat Detection Expert System
% SWI-Prolog
% Defensive academic demonstration of rule-based threat reasoning.

:- dynamic observed/1.

% -------------------------
% Knowledge base: facts
% -------------------------
severity(low).
severity(medium).
severity(high).
severity(critical).

% -------------------------
% Production rules / derived predicates
% -------------------------
threat(brute_force_attempt, User) :-
    observed(failed_logins(User, N)),
    N >= 5.

threat(suspicious_login, User) :-
    observed(unusual_location(User)),
    observed(off_hours_login(User)).

threat(privilege_escalation_detected, User) :-
    observed(privilege_escalation(User)).

threat(suspicious_file_activity, User) :-
    observed(suspicious_file_access(User)).

threat(network_anomaly, User) :-
    observed(abnormal_network_traffic(User)).

threat(account_compromise, User) :-
    threat(privilege_escalation_detected, User),
    threat(suspicious_file_activity, User).

threat(high_risk_account, User) :-
    threat(brute_force_attempt, User),
    threat(suspicious_login, User).

threat(critical_incident, User) :-
    threat(account_compromise, User),
    threat(network_anomaly, User).

% -------------------------
% Recommended actions
% -------------------------
action(isolate_account(User), User) :-
    threat(high_risk_account, User).

action(review_privileges(User), User) :-
    threat(privilege_escalation_detected, User).

action(isolate_host(User), User) :-
    threat(critical_incident, User).

action(investigate_network(User), User) :-
    threat(network_anomaly, User).

% -------------------------
% Backward chaining
% Query examples:
% ?- threat(brute_force_attempt, alice).
% ?- threat(critical_incident, alice).
% -------------------------

% -------------------------
% Forward chaining
% A simple fixed-point engine over observed facts.
% -------------------------

derive_all(Facts, Conclusions) :-
    forward_step(Facts, Facts1),
    ( Facts1 == Facts ->
        Conclusions = Facts
    ;   derive_all(Facts1, Conclusions)
    ).

forward_step(Facts, NewFacts) :-
    findall(F,
            derivable(F, Facts),
            Candidates),
    append(Facts, Candidates, Combined),
    sort(Combined, NewFacts).

derivable(brute_force(User), Facts) :-
    member(failed_logins(User, N), Facts),
    N >= 5.

derivable(suspicious_login(User), Facts) :-
    member(unusual_location(User), Facts),
    member(off_hours_login(User), Facts).

derivable(privilege_escalation_detected(User), Facts) :-
    member(privilege_escalation(User), Facts).

derivable(suspicious_file_activity(User), Facts) :-
    member(suspicious_file_access(User), Facts).

derivable(network_anomaly(User), Facts) :-
    member(abnormal_network_traffic(User), Facts).

derivable(account_compromise(User), Facts) :-
    member(privilege_escalation_detected(User), Facts),
    member(suspicious_file_activity(User), Facts).

derivable(high_risk_account(User), Facts) :-
    member(brute_force(User), Facts),
    member(suspicious_login(User), Facts).

derivable(critical_incident(User), Facts) :-
    member(account_compromise(User), Facts),
    member(network_anomaly(User), Facts).

% -------------------------
% Utility for running a case
% -------------------------
clear_case :-
    retractall(observed(_)).

load_case(Facts) :-
    clear_case,
    forall(member(F, Facts), assertz(observed(F))).

run_case(Facts, Results) :-
    load_case(Facts),
    findall(T-U, threat(T,U), Results).

% -------------------------
% Sample test cases
% -------------------------
test_case(1, [
    failed_logins(alice, 8),
    unusual_location(alice),
    off_hours_login(alice)
]).

test_case(2, [
    privilege_escalation(bob),
    suspicious_file_access(bob)
]).

test_case(3, [
    failed_logins(charlie, 2),
    unusual_location(charlie)
]).

test_case(4, [
    abnormal_network_traffic(diana),
    privilege_escalation(diana),
    suspicious_file_access(diana)
]).

test_case(5, [
    failed_logins(eric, 7),
    unusual_location(eric),
    off_hours_login(eric),
    privilege_escalation(eric),
    suspicious_file_access(eric),
    abnormal_network_traffic(eric)
]).

run_demo :-
    forall(
        test_case(N, Facts),
        (
            format("~nTest Case ~w~nFacts: ~w~n", [N, Facts]),
            run_case(Facts, Results),
            format("Backward-chaining conclusions: ~w~n", [Results]),
            derive_all(Facts, FC),
            format("Forward-chaining closure: ~w~n", [FC])
        )
    ).
