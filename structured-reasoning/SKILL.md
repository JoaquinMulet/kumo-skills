---
name: structured-reasoning
description: Structured reasoning templates for complex code tasks — debugging multi-file bugs, understanding unfamiliar codebases, and comparing implementations. Use when facing hard debugging (bug spans multiple files, root cause unclear), when needing to understand how unfamiliar code works before modifying it, or when comparing two approaches/patches/implementations. Also triggers on "no entiendo este código", "qué hace esto", "por qué falla", "compara estas dos opciones", "investiga este bug". Do NOT use for straightforward tasks where the fix or approach is obvious.
---

# Structured Reasoning

When facing complex code tasks — the kind where jumping straight to a fix leads to wrong conclusions — use these structured templates to reason systematically. The core idea: write down what you expect before you look, then reconcile with what you find. This catches assumption errors that free-form reasoning misses.

Based on research showing that structured reasoning templates improve agentic code accuracy by 10-15 percentage points over standard reasoning (arxiv:2603.01896).

## When to use this

Activate structured reasoning when:
- The bug or question spans **3+ files** and the root cause isn't obvious
- You've already tried one fix and it didn't work (time to slow down)
- The codebase is unfamiliar and you need to build a mental model before changing anything
- You need to compare two implementations and determine if they're equivalent

Do NOT use for: simple typos, one-file fixes, tasks with clear specs, writing new code from scratch.

## Template 1: Debug (Fault Localization)

Use when: a bug exists but the root cause is unclear, especially across multiple files.

### Phase 1: Test/Error Semantics

Before touching code, analyze what the failure actually tells you:
- What does the error message or failing test assert?
- What is the expected behavior vs actual behavior?
- What components are involved? (list them as PREMISES)

### Phase 2: Code Path Tracing

Trace the execution path from the entry point to the failure:
- For each significant call in the path: note the METHOD, FILE:LINE, BEHAVIOR, and WHY it matters
- Build a call sequence showing the flow from input → failure point

### Phase 3: Hypothesis-Driven Exploration

Before reading each new file, write:
```
HYPOTHESIS: [What I expect to find and why]
EVIDENCE SO FAR: [What supports this hypothesis]
CONFIDENCE: [high/medium/low]
```

After reading, update:
```
RESULT: [confirmed/refuted/refined] — [what I actually found]
REMAINING QUESTIONS: [what's still unclear]
NEXT FILE: [what to read next and why]
```

This prevents "fishing" — aimlessly reading files hoping to stumble on the answer.

### Phase 4: Ranked Predictions

Based on the divergence analysis, produce ranked predictions:
- Each prediction must cite a specific PREMISE and specific code location
- Rank by confidence, explain why each candidate could be the root cause
- The top prediction should be actionable (you can write a fix for it)

## Template 2: Code Understanding

Use when: you need to understand how unfamiliar code works before modifying it.

### Step 1: Function Trace Table

Build a table of the relevant functions:

| Function | File:Line | Parameters | Return Type | Behavior (VERIFIED) |
|----------|-----------|------------|-------------|---------------------|

Mark behavior as VERIFIED only after reading the actual implementation, not from names or comments.

### Step 2: Data Flow Analysis

For each key variable:
- Where is it created?
- Where is it modified? (or "NEVER MODIFIED")
- Where is it used?
- Evidence: [specific file:line]

### Step 3: Semantic Properties

Identify properties that matter for your task:
- "Property X is mutable" — Evidence: [where it's mutated]
- "Function Y is pure" — Evidence: [no side effects found in implementation]
- Invariants the code assumes but doesn't explicitly check

### Step 4: Alternative Hypothesis Check

Before committing to your understanding, ask:
- If the opposite conclusion were true, what evidence would exist?
- What did you look for but NOT find? (absence of evidence is data)
- Confidence level: HIGH (multiple confirming sources) / MEDIUM / LOW

## Template 3: Implementation Comparison

Use when: comparing two patches, approaches, or implementations to determine if they're equivalent or which is better.

### Definitions

- D1: State what the first approach does (precise, no assumptions)
- D2: State what the second approach does
- D3: Define "equivalent" for this context (same output? same behavior? same performance?)

### Analysis of Behavior

For each relevant input/scenario:
- What does Approach 1 produce?
- What does Approach 2 produce?
- Are they identical? If not, describe the difference.

Focus especially on **edge cases**: empty inputs, null values, boundary conditions, error paths.

### Divergence Points

If the approaches differ:
- Identify the specific code paths where they diverge
- For each divergence: is it a meaningful behavioral difference or just a stylistic one?
- CLAIM: [specific claim about the difference, citing code locations]

### Conclusion

- EQUIVALENT / NOT EQUIVALENT / CONDITIONALLY EQUIVALENT
- If not equivalent: which approach is correct/better and why?
- If conditionally equivalent: under what conditions do they differ?

## General Rules

- **Hypothesize before you read.** The single most impactful habit. Writing down what you expect forces you to notice when reality differs from your mental model.
- **Track confidence explicitly.** "I think" is vague. "CONFIDENCE: low because I haven't verified the return type" is actionable.
- **Name your evidence.** Every claim should point to a file:line. If you can't cite evidence, mark the claim as UNVERIFIED.
- **Know when to stop.** These templates add overhead. If after Phase 1 the answer is obvious, skip the rest and fix it. The structure is a tool, not a ritual.
- **Adapt freely.** These templates are starting points. Drop sections that don't apply, add sections that do. The goal is structured thinking, not form-filling.
