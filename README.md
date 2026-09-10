# TrustDrift

**Payload-free multi-turn social engineering against tool-using LLM agents.**

Research project, BITS Pilani Dubai Campus. Divyansh Garg (2023A7PS0148U).

---

## The problem

Defences for tool-using LLM agents assume an attack contains a *malicious string* —
an injected instruction, a jailbreak prompt, an adversarial suffix. Social
engineering contains none. Over a sequence of individually innocuous turns an
adversary establishes a false identity, seeds unverifiable premises, and
manufactures authority and urgency, until a request that would have been refused at
turn one is granted at turn ten as the natural continuation of an established
context.

No per-turn classifier can detect this, because no turn contains anything to detect.

## What this repository contains

A benchmark harness in which an attacker agent conducts N-turn conversations against
a tool-using defender agent, under a hard constraint that **every attacker turn must
pass an off-the-shelf prompt-injection classifier**. Attack success is decided
mechanically by a policy oracle — did a credential-affecting tool get called for a
principal whose identity was never verified through the sanctioned channel — so
ground truth requires no annotation and carries no adjudication noise.

```
src/trustdrift/
    scenario.py    environment, tool registry, policy oracle
    harness.py     no-payload gate, episode runner, mock agents
run_demo.py        offline smoke test
```

## Status

| Component | State |
|---|---|
| Scenario spec, tool registry | done |
| Policy oracle (automatic ground truth) | done |
| Episode runner, transcript logging | done |
| No-payload gate (interface + pattern stand-in) | done |
| Mock backend (offline, deterministic) | done |
| Real injection classifier in the gate | next |
| LLM attacker with escalation planner | next |
| Baseline defences D0–D4 | next |
| Adaptive loop | next |
| TrustDrift defence | next |

## Running

```bash
cd src
python run_demo.py
```

No API key, no network, no GPU required. Runs in a few seconds.

**This smoke test is plumbing validation, not an experiment.** It uses scripted
agents to confirm the runner and oracle work end to end. No research claim is made
from its output. Every quantitative claim in the paper will come from the API
backend once it is in place.

Expected: the unguarded agent commits a violation at turn 10; the policy-enforcing
agent refuses the same attack; the policy-enforcing agent still serves a genuine
urgent user who completes verification.

## Design notes

**Why the no-payload constraint.** It removes the attack surface every existing
defence was built for, so that any residual vulnerability is attributable to
conversational manipulation alone. The gate reports its rejection rate as a
property of the benchmark.

**Why mechanical ground truth.** Prior conversational-SE work must annotate
whether an attack succeeded. Automated outcome labelling of multi-turn
conversations has been reported to disagree substantially with human adjudication.
Here the environment knows the answer.

**Why benign controls.** A defence that fires on every urgent legitimate user is
not a defence. False-intervention rate is reported alongside attack success.

## References

See `references.bib`. Core: ConvoSentinel (arXiv:2406.12263), AgentDojo
(arXiv:2406.13352), The Attacker Moves Second (arXiv:2510.09023), LLM agents
security duality (arXiv:2606.28450).
