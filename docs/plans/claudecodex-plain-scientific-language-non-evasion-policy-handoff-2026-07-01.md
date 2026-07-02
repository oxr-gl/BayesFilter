# Claudecodex Plain Scientific Language Policy Handoff Memo

Date: 2026-07-01

Status: handoff memo for the next agent working in
`/home/chakwong/python/claudecodex`.

## Objective

Add a shared agent policy that prevents evasive or imprecise scientific
language. The goal is a generic behavior change for Claude/Codex agents, not a
BayesFilter-specific fix and not a score-specific fix.

The policy should make this principle explicit:

> Politeness is allowed in tone, but not in epistemic content. If a claim is
> false relative to its stated target, unsupported, unproved, or only true after
> qualification, say that directly.

## Permission And Workspace Guidance

This memo was drafted from `/home/chakwong/BayesFilter`, whose sandbox may not
have write access to `/home/chakwong/python/claudecodex`.

To avoid write-permission problems:

1. Start the next Codex/Claude task with working directory
   `/home/chakwong/python/claudecodex`, or request escalated permissions before
   writing there.
2. Use `apply_patch` for manual edits inside the claudecodex repository.
3. Do not use shell redirection, `cat > file`, or ad hoc write commands for
   policy edits.
4. If running the installer modifies files under `~/.claude`, `~/.codex`, or
   `~/AGENTS.md`, run it in an approved/trusted context and record the exact
   command.

## Files To Inspect First

Read these before editing:

- `/home/chakwong/python/claudecodex/AGENTS.md`
- `/home/chakwong/python/claudecodex/policies/global-scientific-coding-agent-policy.md`
- `/home/chakwong/python/claudecodex/install_global_agent_policy.py`
- `/home/chakwong/python/claudecodex/README.md`
- `/home/chakwong/python/claudecodex/claude/prompts/scholarly_literature_audit_review.md`
- `/home/chakwong/python/claudecodex/claude/prompts/scholarly_literature_audit_execution.md`
- `/home/chakwong/python/claudecodex/docs/templates/visible-gated-execution-runbook-template.md`

## Required Policy Change

Add a new section to
`/home/chakwong/python/claudecodex/policies/global-scientific-coding-agent-policy.md`.
A good location is after `## Mathematical And Literature Discipline`.

Use this content as the starting point, editing only for clarity:

```md
## Plain Scientific Language And Non-Evasion

- Politeness is allowed in tone, but not in epistemic content. Do not soften,
  hide, or blur a scientific verdict when the target, computed quantity, and
  evidence are clear.
- Use direct classifications:
  - `correct`: follows from checked derivation, source, code, or evidence.
  - `wrong relative to the stated target`: the computed object differs from the
    claimed object, or the claim omits a required term, condition, dependence,
    or diagnostic.
  - `unsupported`: no inspected derivation, citation, or artifact supports the
    claim.
  - `not checked`: the agent has not inspected enough evidence to decide.
  - `heuristic only`: may be useful, but no correctness claim is established.
- Do not use words such as "surrogate", "stabilized", "proxy",
  "reasonable", "practical", "contract", or "approximately correct" to hide a
  mathematical, statistical, or implementation mismatch. These words are allowed
  only when the modified target is explicitly defined and its relation to the
  original target is stated.
- If a method changes the objective, omits known terms, takes a partial
  derivative where a total derivative is claimed, changes the probability
  measure, changes the conditioning event, changes the baseline, or changes the
  diagnostic target, say so plainly.
- Do not say "not necessarily wrong" when the implementation fails to compute
  the claimed mathematical quantity. Say "wrong relative to that claim" and
  then state whether a different, explicitly defined claim may still be viable.
- For serious scientific or numerical conclusions, state:
  - the claimed target;
  - the quantity actually computed;
  - whether they are equal, approximately related, different, or not checked;
  - the derivation, source anchor, or artifact supporting that verdict;
  - what remains unproved or unevaluated.
- If support has not been checked, prefer "unsupported" or "not checked" over
  softening language. Direct qualification is required; evasive qualification is
  forbidden.
```

## Required Review-Prompt Changes

Update Claude review prompts so a read-only reviewer must flag evasive
scientific language.

At minimum, add a review item to:

- `claude/prompts/scholarly_literature_audit_review.md`
- `claude/prompts/scholarly_literature_audit_execution.md`, if it includes
  claim-writing or report-writing instructions.

Reviewer instruction should require:

- identify unsupported euphemisms;
- verify target quantity versus computed quantity;
- reject "surrogate", "proxy", "stabilized", or "contract" language unless the
  modified target and support are explicit;
- require a direct verdict when an implementation or derivation differs from the
  stated claim.

## Required Template Change

Update
`/home/chakwong/python/claudecodex/docs/templates/visible-gated-execution-runbook-template.md`
with a small non-evasion or plain-language review gate.

The gate should ask whether the result note:

- states target and computed quantity separately;
- uses direct classifications;
- avoids unsupported soft language;
- labels unsupported claims as unsupported;
- labels mismatches as wrong relative to the stated target.

## Installer Guidance

The installer already reads only:

`policies/global-scientific-coding-agent-policy.md`

through `_read_policy()` in `install_global_agent_policy.py`. Therefore, if the
only global behavior change is new policy text, do not modify the installer.

Modify `install_global_agent_policy.py` only if installation targets or marked
block behavior change. That is not expected for this task.

## Required Checks

Run these from `/home/chakwong/python/claudecodex`:

```bash
python install_global_agent_policy.py --dry-run
python -m py_compile install_global_agent_policy.py
```

If no installer code is changed, the compile check is still a cheap safety
check. If README or prompt templates are changed, inspect the diff manually.

After review and human approval if required, install with:

```bash
python install_global_agent_policy.py
```

Record which targets were updated.

## Evidence Contract

Question:
Does the shared claudecodex policy now require agents to use direct scientific
language and prevent evasive wording that hides unsupported or wrong claims?

Pass criteria:

- The global policy contains an explicit plain-language and non-evasion section.
- Review prompts require detection of evasive or unsupported scientific
  language.
- The gated runbook template includes a non-evasion/plain-language review gate.
- Dry-run installer succeeds.
- No installer behavior is changed unless explicitly justified.

Veto conditions:

- The policy weakens existing evidence discipline.
- The policy is BayesFilter-specific rather than project-independent.
- The policy uses vague language that repeats the problem it is meant to fix.
- The installer is modified unnecessarily.
- The agent claims installation happened without running the installer or
  recording its output.

What must not be concluded:

- This does not prove future agents will never be evasive.
- This does not resolve any BayesFilter mathematical issue by itself.
- This does not make unsupported claims correct; it only requires them to be
  labeled plainly.

## Motivation From The Incident

The immediate trigger was a debugging failure where agents described a simple
mathematical mismatch using indirect language. The core issue was total
derivative versus partial derivative:

```text
score = d/dtheta F(theta, z(theta))
stopped route = partial_theta F(theta, z) at z = z(theta)
```

If the stated target is the score, the stopped route is wrong relative to that
target unless a different target is explicitly defined and justified. Calling it
"stabilized" or "surrogate" without a defined target and support hides the
scientific status. This memo generalizes that lesson to all scientific and
numerical claims.

## Expected Close Record

When done, write a short close record under
`/home/chakwong/python/claudecodex/docs/plans/` with:

- files changed;
- exact checks run;
- installer dry-run output summary;
- installer output summary, if installed;
- whether Claude/Codex review found evasive language;
- remaining limitations.
