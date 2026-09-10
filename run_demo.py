"""
Smoke test for the TrustDrift harness.

Runs two scripted episodes offline (no API key, no network) to verify that the
episode runner, the no-payload gate and the policy oracle work end to end.

This is plumbing validation, NOT an experiment. No research claim is made from
these numbers.

    python run_demo.py
"""
from trustdrift.harness import (NoPayloadGate, run_episode, save_episodes,
                                MOCK_ATTACK_SCRIPT, MOCK_BENIGN_SCRIPT)

def main():
    gate = NoPayloadGate()
    print("=" * 72)
    print("TrustDrift harness — smoke test (mock backend, offline)")
    print("=" * 72)

    eps = []
    cases = [
        ("D0  unguarded agent   vs. payload-free attacker", MOCK_ATTACK_SCRIPT, False, "malicious"),
        ("D1  policy-enforcing  vs. payload-free attacker", MOCK_ATTACK_SCRIPT, True,  "malicious"),
        ("D1  policy-enforcing  vs. genuine urgent user   ", MOCK_BENIGN_SCRIPT, True,  "benign"),
    ]
    for title, script, strict, label in cases:
        print(f"\n--- {title} ---")
        ep = run_episode(script, gate, strict, label)
        eps.append(ep)
        print(ep.transcript())
        print(f"\n  tool calls : {ep.env.tool_calls}")
        print(f"  ORACLE     : {ep.verdict}")

    print("\n" + "=" * 72)
    print(f"no-payload gate: screened {gate.screened}, rejected {gate.rejected} "
          f"({gate.rejection_rate:.1%})")
    save_episodes(eps, "episodes.jsonl")
    print("episodes written to episodes.jsonl")
    print("=" * 72)

if __name__ == "__main__":
    main()
