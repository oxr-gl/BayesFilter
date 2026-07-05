# Actual-SV Single-Target Visible Stop Handoff

Date: 2026-06-29

## Status

`ACTIVE_STOP_HANDOFF_TEMPLATE`

## Use

Write this artifact when the program stops because of:

- a newly discovered governing-scalar contradiction;
- review nonconvergence after five rounds for the same blocker;
- a human-required boundary;
- inability to classify a route as same-target versus surrogate;
- inability to proceed without runtime/package/default actions outside the current
  reviewed phase.

## Stop Record Template

### Stop summary

- Phase reached:
- Gate status:
- Immediate blocker:
- Why continuing would risk drift or unsupported claims:

### Governing state at stop

- Current authority artifact:
- Current single-target contract status:
- Route statuses known so far:
- Last reviewed artifact:

### What was completed safely

- <artifacts written>
- <checks/reviews completed>

### What was explicitly not concluded

- <non-claims preserved at stop>

### Exact next reviewed action required

- <next subplan / reset memo / human decision>

## Standing rule

If the stop reason is that the governing scalar or comparator class is wrong or
unclear, the next action must be a reset memo or reviewed blocker artifact
before any implementation or test execution resumes.
