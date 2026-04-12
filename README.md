# SpecForge

SpecForge is a CLI for turning a human request into a set of Claude execution artifacts with clear scope, explicit constraints, and measurable delivery criteria.

The project comes from a practical problem teams hit with coding agents every day: the code may be impressive, yet the result still misses the requirement. A request starts simple, then the run accumulates logs, diffs, prior decisions, repo rules, tool outputs, and half-remembered assumptions. By the end, the agent may produce useful code, but the team still has to ask the same questions:

- Did it stay inside the requested scope?
- Did it preserve the real constraints?
- Did it prove completion with evidence?
- Can another run follow the same contract?

SpecForge gives that request a stronger form before implementation begins.

It also supports a `spec-driven development` workflow. In practice, that workflow often struggles at the hardest point: defining the full set of requirements, constraints, evidence, and guardrails needed before execution starts. SpecForge helps turn that fuzzy upfront phase into a concrete operational spec that can actually drive implementation.

## Two flavors: external CLI and in-Claude skills

| Flavor | Role |
| --- | --- |
| **Python CLI** (`specforge`) | Runs locally with API keys: LLM draft → normalized spec → lint → writes the artifact bundle under your chosen output directory (default: `specforge-bundle`). |
| **Claude Code skills** (this repo) | Project skills under `.claude/skills/` teach Claude the same pipeline **inside** the session. MCP-connected tools can supply repo, docs, and ticket context while authoring or implementing from a spec—no terminal required for the drafting workflow. |

Bundled skills:

- **`specforge`** — Compile a requirement into `spec.yaml` and the usual Claude artifacts; emphasizes MCP context gathering first.
- **`specforge-implement`** — Execute implementation when a bundle already exists.

Sample CLI output (parser CLI example) lives at `examples/sample-bundle/`. Repository skills and generated bundles are intentionally separate: skills live under `.claude/skills/`, generated work typically under `./specforge-bundle` or a path you choose.

## Demo

Interactive CLI: compile a requirement, then choose an output folder. The status panel shows provider, workspace, pipeline (`task -> spec -> lint -> package`), and slash commands.

![Spec Forge v0.1.0 interactive CLI](docs/cli-demo.png)

## What Problem It Solves

Coding agents operate inside a context harness, not inside a vacuum. The current user request is only one layer among many:

1. system and platform instructions
2. repository and project guidance
3. current user request
4. conversation history
5. tool outputs such as logs, patches, errors, and file content

That stack is powerful, and it is also where drift begins. The core requirement can become proportionally small compared to the rest of the context. Missing details are silently completed by pattern matching. “Helpful” additions can slip in because no hard execution contract exists. Completion can be reported in broad language even when acceptance remains fuzzy.

SpecForge addresses that by compiling the request into artifacts that are easier for a coding agent to follow and easier for a human to audit.

## What It Produces

For each request, SpecForge generates a bundle designed for Claude-driven execution:

- `spec.yaml` with objective, assumptions, constraints, success criteria, evidence, actions, and decision rules
- `CLAUDE.md` with persistent project memory and execution guardrails
- `.claude/commands/implement-from-spec.md` as the implementation entrypoint
- `acceptance-checklist.md` as a final delivery gate
- `evals/scope_drift_cases.yaml` for scope-oriented evaluation seeds

These files give the run a stable anchor. Instead of asking the coding agent to remember everything from a loose prompt, the workflow gives it a compact contract it can revisit throughout implementation.

## Structure of the Generated Spec

The operational contract lives primarily in `spec.yaml`. The other generated files are views or workflows built from that same content.

### Top-level fields in `spec.yaml`

| Area | Fields | Role |
| --- | --- | --- |
| Identity | `version`, `title`, `objective` | What is being built and why. |
| Execution | `execution_mode` | How the run should proceed (for example step-by-step vs other modes the CLI supports). |
| Context | `context` | Nested object: `system` (environment or repo framing) and `assumptions` (explicit premises the implementation may rely on). |
| Boundaries | `constraints` | Hard limits: what must stay true or out of scope. |
| Outcomes | `success_criteria`, `required_evidence` | What “done” means and what proof is required. |
| Reasoning | `hypotheses` | List of objects with `id`, `description`, and `confidence` (0–1). These are the working beliefs the plan is based on. |
| Work plan | `actions` | List of objects: `id`, `description`, `type`, optional `requires_confirmation`, and `supports` (hypothesis ids this action advances or depends on). |
| Governance | `decision_rules` | When to stop, escalate, or choose between options during implementation. |
| Provenance | `metadata` | Compiler-filled and model fields such as `source_prompt`, `generator`, `model`, optional `profile`, and optionally `scope_contract` (see below). |

Strings in list fields are deduplicated when normalized; hypothesis and action `id` values are normalized to stable identifiers.

### Traceability: actions and hypotheses

Each action can list hypothesis ids in `supports`. That links planned work to the hypotheses it validates or depends on. The linter can require every hypothesis to be referenced by at least one action and every action to declare `supports` when policy demands it, so the spec stays auditable as a graph rather than a flat checklist.

### Scope contract in metadata

When present, `metadata.scope_contract` (or the field name set by `scope_contract_field` in policy) holds structured in/out scope:

- `must_include`: items that must remain in scope.
- `must_not_include`: items explicitly out of scope.

That shape feeds scope evaluation and helps catch drift against the original intent.

### How the other artifacts relate

- **`CLAUDE.md`** summarizes constraints, decision rules, success criteria, and assumptions from the spec into persistent project memory plus an implementation protocol that points back to `spec.yaml`.
- **`.claude/commands/implement-from-spec.md`** is the command entrypoint for running implementation against the bundled spec.
- **`acceptance-checklist.md`** turns success criteria and related spec content into a human- and agent-checkable delivery gate.
- **`evals/scope_drift_cases.yaml`** provides evaluation seeds derived from the spec for scope-oriented checks.

Reading `spec.yaml` first is the source of truth; the other files are aligned views for Claude and for review.

## How The Flow Works

The runtime path is straightforward:

```text
Human request
    |
    v
LLM draft JSON
    |
    v
Normalization into Spec
    |
    v
Programmatic lint + policy checks
    |
    v
Score / pass gate
    |
    v
Claude artifact bundle
```

The LLM produces a structured draft. The generator normalizes that draft into the internal `Spec` model. The lint step then applies deterministic checks over structure and traceability. Policy controls thresholds, required fields, minimum section counts, and scoring penalties. If the spec clears the gate, SpecForge packages the Claude artifacts for execution.

This architecture is intentionally split:

- generation handles synthesis
- normalization handles shape and consistency
- lint handles deterministic enforcement
- packaging handles downstream Claude usability

## What The Lint Actually Validates

The lint layer evaluates the generated spec programmatically. It checks:

- required fields and expected types
- minimum content counts per section
- hypothesis identity and confidence format
- action identity, type, and confirmation flags
- traceability links from actions to hypotheses through `supports`
- required metadata fields
- duplicate or near-duplicate list entries

This gives the project a machine-checkable quality gate before the artifacts are handed to a coding agent.

Semantic truth still depends on the original request and on the draft quality produced by the model. Structural integrity, traceability discipline, and packaging readiness are enforced by code.

## Why This Matters For Claude

Claude performs best when the execution surface is compact, explicit, and revisitable. A long-running implementation session is easier to control when the important constraints are already materialized into files the agent can read repeatedly:

- one file for the operational spec
- one file for persistent memory
- one checklist for acceptance
- one command entrypoint for execution

That structure reduces accidental scope expansion and raises the chance of reproducible delivery across runs.

## Using The CLI

From the repository root:

```bash
.venv/bin/specforge
```

This opens the interactive client. You write the task, choose the output folder, and SpecForge generates the bundle.

Direct execution also works:

```bash
.venv/bin/specforge "build a deterministic SQL expression analyzer CLI"
.venv/bin/specforge --prompt "build a deterministic SQL expression analyzer CLI"
.venv/bin/specforge --from-file prompt.txt
```

## API Key Configuration

The CLI resolves the provider from the environment.

Recommended setup: create `./.venv/.env`

```env
OPENAI_API_KEY="sk-..."
OPENAI_MODEL="gpt-codex"

# or
ANTHROPIC_API_KEY="sk-ant-..."
ANTHROPIC_MODEL="claude-3-5-sonnet-latest"
```

Alternative shell configuration:

```bash
export OPENAI_API_KEY="sk-..."
# or
export ANTHROPIC_API_KEY="sk-ant-..."
```

## Compiler Policy

SpecForge supports an optional policy file for controlling how strict the compilation and gate should be.

Default path:

```text
./.specforge-policy.yaml
```

Override path:

```bash
export SPECFORGE_POLICY=/path/to/policy.yaml
```

Example policy:

```yaml
min_items:
  assumptions: 1
  constraints: 2
  success_criteria: 2
  hypotheses: 1
  required_evidence: 2
  actions: 2
  decision_rules: 2
allowed_action_types: [analyze, design, implement, validate, review]
require_action_support_links: true
required_metadata_fields: [source_prompt]
scope_contract_field: scope_contract
lint_base_score: 100
lint_error_penalty: 18
lint_warning_penalty: 5
lint_min_passing_score: 70
scope_eval_base_score: 100
scope_violation_penalty: 25
```

## Architecture At A Glance

Core files:

- `src/opsspec/cli.py` handles the user flow
- `src/opsspec/generator.py` compiles draft JSON into the internal spec
- `src/opsspec/linting.py` applies deterministic quality checks
- `src/opsspec/scope_eval.py` evaluates scope contract adherence
- `src/opsspec/claude_skill.py` writes the Claude artifact bundle
- `src/opsspec/nlp_policy.py` loads policy and scoring configuration

In-Claude authoring and handoff:

- `.claude/skills/specforge/` — Skill instructions and references for MCP-aware spec compilation
- `.claude/skills/specforge-implement/` — Skill for implementation-only runs from an existing bundle

Example generated bundle (for reference): `examples/sample-bundle/`

## Case Study: Mini OS

The `examples/mini-os/` directory is a complete SpecForge-driven implementation of a minimal x86 bare-metal operating system. It shows the full workflow from a single prompt to a bootable disk image.

![MiniOS v0.1 running in QEMU — boot summary, memory map, and GDT](docs/minios-qemu.png)

### The original prompt

```
build a simple operating system
```

### What the skill compiled

Running `/specforge` against that prompt produced the full artifact bundle in one step:

| Artifact | Role |
| --- | --- |
| `spec.yaml` | Operational contract: objective, assumptions, constraints, success criteria, hypotheses, actions, decision rules |
| `CLAUDE.md` | Persistent project memory: guardrails, known pitfalls, decision log |
| `.claude/commands/implement-from-spec.md` | Implementation entrypoint — step-by-step execution recipe |
| `acceptance-checklist.md` | Delivery gate: every criterion checked with evidence |
| `evals/scope_drift_cases.yaml` | Scope evaluation seeds — patterns that must match or not match |

### The generated spec at a glance

**Objective** — 512-byte BIOS bootloader + freestanding C kernel → VGA text output → boots in QEMU from a raw disk image, no external libraries.

**Constraints (hard limits from `spec.yaml`)**
- Bootloader must be exactly 512 bytes and end with the `0xAA55` BIOS signature.
- Kernel is freestanding C only — no libc, no crt0, no runtime.
- Zero external libraries; toolchain is nasm + gcc -m32 + ld.
- All files inside `examples/mini-os/`.
- `make run` is the single command to boot in QEMU.

**Hypotheses the spec reasoned about**

| ID | Claim | Confidence |
| --- | --- | --- |
| h1 | A 512-byte NASM bootloader can load, switch to protected mode, and hand off to a C kernel at 0x1000 | 0.95 |
| h2 | A freestanding C kernel can write directly to VGA framebuffer 0xB8000, producing readable coloured output | 0.97 |
| h3 | A Makefile using only nasm + gcc -m32 + ld can produce a bootable raw image runnable in qemu-system-x86_64 | 0.92 |

**Actions the spec decomposed the work into**

| ID | Type | Description |
| --- | --- | --- |
| a1 | design | Create directory layout: `boot/`, `kernel/`, `linker.ld`, `Makefile` |
| a2 | implement | Write `boot/boot.asm` — 16-bit startup, INT 13h disk read, A20, GDT, protected-mode switch, jump to 0x1000 |
| a3 | implement | Write `kernel/kernel.c` — VGA helpers and `kernel_main` banner |
| a4 | implement | Write `linker.ld` — sections at 0x1000, flat binary output |
| a5 | implement | Write `Makefile` — `all`, `run`, `clean` targets; produce `build/os.img` |
| a6 | validate | Run `make`, check boot.bin size, boot in QEMU, verify VGA output |

Each action declares `supports` links to the hypotheses it validates, so the spec is auditable as a graph.

**Scope contract — what the spec explicitly fenced out**

```yaml
must_include:
  - 512-byte bootloader (NASM)
  - protected-mode switch
  - freestanding C kernel
  - VGA text output
  - Makefile
  - QEMU run target

must_not_include:
  - libc or any runtime library
  - filesystem driver
  - keyboard/interrupt handling
  - multitasking or scheduling
  - anything outside examples/mini-os/
```

### Scope drift evaluation

`evals/scope_drift_cases.yaml` holds 11 machine-checkable seeds derived from the spec. Six are negative checks (patterns that must never appear — no `#include <stdio.h>`, no `-lpthread`, no IDT, no scheduler keywords) and five are positive checks (files that must exist and contain specific keywords like `0xAA55`, `0xB8000`, `-ffreestanding`).

### Implementation and evidence

Running `/implement-from-spec` executed the six actions in order. The acceptance checklist was filled with evidence, not approximations:

```
$ make
  [OK] boot.bin     512 bytes
  [OK] kernel.bin   2445 bytes
  [OK] os.img       65536 bytes
  [OK] magic        55aa

$ xxd -s 510 -l 2 build/os.img
000001fe: 55aa

$ qemu debug port output:
MiniOS v0.1 — kernel_main reached
[BOOT] Bootloader: 0x7C00  Kernel: 0x1000  Stack: 0x90000
[MEM]  VGA: 0xB8000  Conv: 0x00000-0x9FFFF
[GDT]  Code: 0x08  Data: 0x10
Kernel halted. All systems nominal.
```

All acceptance criteria passed: `make` exits 0, `boot.bin` is exactly 512 bytes, bytes 510–511 are `55 AA`, the kernel banner appears in QEMU with coloured VGA sections, and `make clean` removes all artefacts.

### What the spec prevented

The decision rules in the spec handled the real hardware-level failure modes before they became dead ends:

- Boot.bin > 512 bytes → trim GDT or strings, never remove the magic bytes.
- Black screen → check `0xAA55` at offset 510 and kernel load address `0x1000`.
- Garbled VGA → verify `(attr << 8) | char` cell encoding.
- Linker emits ELF → add `--oformat binary` to ld invocation.

The `CLAUDE.md` pitfall log captured the Apple Silicon cross-compiler issue (`i686-elf-gcc`) and the entry-point ordering problem (linking `entry.o` first so `call 0x1000` lands on `kernel_main`, not a helper function) — decisions that would otherwise disappear into conversation history.

## Next TODOs

- Add a conflict-mediation structure for cases with conflicting requirements
