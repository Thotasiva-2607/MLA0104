# Cybersecurity Threat Detection Expert System

## Topic
Rule-based expert system for a Security Operations Center (SOC).

## Tool
SWI-Prolog.

## Files
- `cybersecurity_expert.pl` - Prolog knowledge base, rules, forward and backward reasoning.
- `test_cases.txt` - Five industry-based test cases and expected results.
- `Cybersecurity_Threat_Detection_Expert_System_Report.docx` - Complete academic report.

## Run
1. Install SWI-Prolog.
2. Open SWI-Prolog.
3. Consult the file:
   `['cybersecurity_expert.pl'].`
4. Run:
   `?- run_demo.`
5. Try backward-chaining queries:
   `?- threat(brute_force_attempt, alice).`
   `?- threat(account_compromise, bob).`
   `?- threat(critical_incident, diana).`

## Note
The rules are an educational prototype. Real SOC systems should combine rule-based reasoning with calibrated thresholds, event correlation, authentication telemetry, endpoint/network logs, and human analyst validation.
