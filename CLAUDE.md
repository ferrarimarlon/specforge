# CLAUDE.md — Project Memory

## Framework

This project uses **ForgeMySpec** as its default development framework. All implementation work must follow the spec-first workflow.

## Default Agent

The `forgemyspec-default` agent (`plugins/forgemyspec/agents/forgemyspec-default.md`, symlinked under `.claude/agents/`) is the entry point for all development tasks. It:
- Preloads the `forgemyspec` and `forgemyspec-implement` skills
- Enforces spec compilation before any code is written
- Routes to the correct skill based on whether a `spec.yaml` already exists

## Spec-First Rule

**Do not write code without a spec.**

| Situation | Action |
|---|---|
| No spec exists for the task | Run `/forgemyspec` first |
| Spec exists | Run `/forgemyspec-implement` |
| Spec is stale or ambiguous | Ask user to update `spec.yaml` before proceeding |

## Project Layout

```
.
├── CLAUDE.md                          ← you are here (project memory)
├── plugins/forgemyspec/                 ← canonical skills + default agent source (symlinked into .claude/)
│   ├── agents/forgemyspec-default.md
│   └── skills/{forgemyspec,forgemyspec-implement}/
├── .claude/
│   ├── settings.json                  ← `defaultAgent`: forgemyspec-default
│   ├── agents/forgemyspec-default.md    ← symlink → plugins/forgemyspec/agents/…
│   └── skills/                        ← symlinks → plugins/forgemyspec/skills/…
├── examples/                          ← example ForgeMySpec bundles
│   ├── sample-bundle/                 ← parser CLI example
│   └── mini-os/                       ← minimal x86 OS example
└── src/                               ← ForgeMySpec Python package
```

## Conventions

- Generated bundles go in `./forgemyspec-bundle/` or a task-named subdirectory — never directly in `.claude/skills/`.
- `CLAUDE.md` files (this one and those inside bundles) store only stable decisions and known pitfalls — not transient logs or scratch notes.
- Scope drift is checked against `evals/scope_drift_cases.yaml` in each bundle.

## Known Pitfalls

- Do not add external dependencies unless the spec's `must_include` explicitly calls for a library.
- Do not amend a spec mid-implementation without user approval — create a new spec version instead.
