# Ads and Analytics review guide

Apply these checks to changes in `Media-Platforms/ads-and-analytics`. They also cover its contracts with FRE when the diff crosses that boundary.

## Analytics and ad behavior

- Trace event and ad lifecycles for duplicate listeners, repeated initialization, double-counting, duplicate ad requests, or stacked slots.
- For ad insertion changes, verify the slot and position contract, desktop and mobile ordering, immediate versus lazy request timing, paired breaker and rail behavior, and empty-container handling. Confirm expected values from current code or tests; do not assume one template's taxonomy applies everywhere.
- Check whether template-specific behavior belongs in a narrow, named path instead of a shared landing, feed, or orchestration flow. Keep observers and selectors scoped to the owning page or component.
- Look for existing helpers, config, and contracts before accepting new globals, duplicated queries, hard-coded site/test values, or fallback selectors.
- Keep the full business rule in a clear owner. Check that guards, utilities, and test fixtures do not each encode only part of the decision.

## FRE integration

When FRE markup, events, attributes, or UI behavior interact with this code:

- Identify the producer and consumer, and verify event names, detail properties, and data attributes match.
- Confirm which repository owns rendered or reserved DOM. Keep component-specific markup with its owner when possible.
- First check whether ads-and-analytics can make the decision itself. Request a FRE change only when the producer or DOM contract must change.
- If both repositories change, check dependency links, release coordination, and integration evidence.
- Avoid multiple aliases for one contract unless a migration requires them and the transition is clear.

## QA and evidence

For runtime changes, look for concrete QA steps that cover the changed template and representative unaffected surfaces. Check that PR-bundle URLs preserve required parameters, that event/ad tests cover edge cases, and that cross-repo payloads are exercised when relevant. Do not ask for broad end-to-end coverage when the diff cannot affect runtime behavior.
