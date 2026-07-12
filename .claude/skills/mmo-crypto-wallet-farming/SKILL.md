---
name: mmo-crypto-wallet-farming
description: Use when MMO crypto operations need multi-wallet isolation, airdrop task automation, on-chain interaction scripting, and Sybil-avoidance strategy for DeFi and airdrop farming.
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash"]
---

# Mission
Operate a multi-wallet crypto farming program with strict identity isolation and human-mimicking on-chain behavior.

## Mandatory scope checks
- define wallet isolation: one wallet = one browser profile = one proxy = one funded identity
- define on-chain behavioral variance: randomize swap amounts, transaction timing, gas price variation
- define activity consistency schedule: regular low-frequency weekly interactions preferred over burst sessions
- define security perimeter: farming wallets isolated from primary asset wallets
- define Sybil-risk assessment per project before committing wallet resources
- define capital budget: gas costs, minimum funding per wallet, maximum capital at risk

## Evidence contract
- include wallet-to-profile-to-proxy binding registry with zero sharing verified
- include behavioral variance config showing non-repetitive transaction patterns
- include dry-run trace: wallet completes tasks with varied timing and amounts

## Role
- mmo-crypto-farming

## Layer
- layer-4-specialists-and-standalones

## Inputs
- wallet inventory (address, funded status, chain, proxy assignment, age, on-chain history)
- target protocol task list (swap, LP provision, governance vote, quest, bridge)
- Sybil detection signals published or known for the target project

## Outputs
- crypto farming operations plan: wallet registry, behavioral variance config, security controls, Sybil-avoidance rules, and capital risk summary

## Reference skills and rules
- Sybil detection in 2026 uses AI behavioral analysis — identical timing or amounts across wallets causes mass disqualification.
- Weekly consistent activity beats daily heavy activity for most airdrop eligibility criteria.
- Never use unaudited or unverified automation scripts with wallet access — seed phrase compromise causes total asset loss.
- Gas cost and capital risk must be explicitly budgeted before any farming campaign starts.
- Open `references/mmo-crypto-wallet-farming-operator-contract.md` when scope, evidence, or operator safety is unclear.
- Use `examples/mmo-crypto-wallet-farming-good-output.md` and `examples/mmo-crypto-wallet-farming-bad-output.md` to calibrate output quality.
- Use `evals/mmo-crypto-wallet-farming-cases.json` as the minimum scenario set for behavior regression checks.
- Use `competencies/mmo-crypto-wallet-farming-competencies.json` to check covered competencies, failure traps, and unknown-domain policy.

## Likely next step
- mmo-identity-infrastructure
- mmo-proxy-network-ops
- mmo-http-api-automation
- policy-guard
- qa-governor
