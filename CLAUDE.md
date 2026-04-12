# CLAUDE.md — Project Memory

## Framework

This project uses **SpecForge** as its default development framework. All implementation work must follow the spec-first workflow.

## Default Agent

The `specforge-default` agent (`.claude/agents/specforge-default.md`) is the entry point for all development tasks. It:
- Preloads the `specforge` and `specforge-implement` skills
- Enforces spec compilation before any code is written
- Routes to the correct skill based on whether a `spec.yaml` already exists

## Spec-First Rule

**Do not write code without a spec.**

| Situation | Action |
|---|---|
| No spec exists for the task | Run `/specforge` first |
| Spec exists | Run `/specforge-implement` |
| Spec is stale or ambiguous | Ask user to update `spec.yaml` before proceeding |

## Project Layout

```
.
├── CLAUDE.md                          ← you are here (project memory)
├── .claude/
│   ├── settings.json                  ← hooks + default agent config
│   ├── agents/
│   │   └── specforge-default.md       ← default agent definition
│   └── skills/
│       ├── specforge/                 ← spec compilation skill
│       └── specforge-implement/       ← implementation skill
├── examples/                          ← example SpecForge bundles
│   ├── sample-bundle/                 ← parser CLI example
│   └── mini-os/                       ← minimal x86 OS example
└── src/                               ← SpecForge Python package
```

## Conventions

- Generated bundles go in `./specforge-bundle/` or a task-named subdirectory — never directly in `.claude/skills/`.
- `CLAUDE.md` files (this one and those inside bundles) store only stable decisions and known pitfalls — not transient logs or scratch notes.
- Scope drift is checked against `evals/scope_drift_cases.yaml` in each bundle.

## Known Pitfalls

- Do not add external dependencies unless the spec's `must_include` explicitly calls for a library.
- Do not amend a spec mid-implementation without user approval — create a new spec version instead.
