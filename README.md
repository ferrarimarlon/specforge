# SpecForge

**Turn a human request into a machine-executable contract — before the first line of code is written.**

SpecForge compiles natural-language requirements into a structured artifact bundle that gives a coding agent a stable, auditable contract to work from. The output is not documentation. It is a runtime-ready execution harness for Claude.

![Spec Forge v0.1.0 interactive CLI](docs/cli-demo.png)

---

## The Problem

Coding agents operate inside a context harness, not a vacuum. Every session layers request on top of guidance on top of history on top of tool output. That stack is powerful — and it is exactly where drift begins.

```
1. system and platform instructions
2. repository and project guidance
3. current user request          ← gets proportionally smaller over time
4. conversation history
5. tool outputs: logs, patches, errors, file content
```

By mid-session, the original requirement is a small fraction of what the agent is tracking. Missing details get silently filled by pattern-matching. "Helpful" additions slip in because no hard execution contract exists. Completion gets reported in broad language even when acceptance criteria remain fuzzy.

**SpecForge addresses this by compiling the request into a compact contract before implementation starts.**

---

## What SpecForge Produces

Each compilation run outputs a bundle of five artifacts:

| Artifact | What It Does |
|---|---|
| `spec.yaml` | The operational contract: objective, assumptions, constraints, success criteria, hypotheses, actions, decision rules |
| `CLAUDE.md` | Persistent project memory: guardrails, known pitfalls, decision log — Claude reads this on every turn |
| `.claude/commands/implement-from-spec.md` | The implementation entrypoint — a step-by-step execution recipe |
| `acceptance-checklist.md` | The delivery gate: every criterion stated as a checkable assertion with required evidence |
| `evals/scope_drift_cases.yaml` | Machine-checkable scope seeds — patterns that must or must not appear in the implementation |

These files give the agent a stable anchor it can revisit throughout a long session. Instead of holding everything in context, the agent has a compact contract it can re-read at any step.

---

## Two Ways To Use It

| Flavor | What It Does |
|---|---|
| **Python CLI** (`specforge`) | Runs locally with your API key. Interactive or direct-prompt mode. Writes the artifact bundle to your chosen output directory (default: `specforge-bundle`). |
| **Claude Code skills** | Project skills under `.claude/skills/` teach Claude the same pipeline inside the session. No terminal required. MCP-connected tools can supply repo, docs, and ticket context during spec authoring. |

**Bundled skills:**

- **`/specforge`** — Compile a requirement into `spec.yaml` and the full artifact bundle. Gathers MCP context first.
- **`/specforge-implement`** — Execute implementation when a bundle already exists. No re-compilation.

---

## Interactive CLI

Write the task. Choose an output folder. SpecForge generates the bundle. The status panel shows provider, workspace, pipeline stage, and available slash commands.

```bash
# Interactive mode
.venv/bin/specforge

# Direct prompt
.venv/bin/specforge "build a deterministic SQL expression analyzer CLI"

# From file
.venv/bin/specforge --from-file prompt.txt
```

---

## The Compilation Pipeline

```
Human request
    │
    ▼
LLM draft JSON
    │
    ▼
Normalization → internal Spec model
    │
    ▼
Programmatic lint + policy checks
    │
    ▼
Score / pass gate
    │
    ▼
Claude artifact bundle
```

The pipeline is deliberately split:

- **Generation** handles synthesis — the LLM turns a prompt into structured JSON
- **Normalization** handles shape — deduplication, stable IDs, consistent types
- **Lint** handles enforcement — deterministic checks over structure and traceability
- **Packaging** handles Claude usability — writing files the agent can re-read mid-session

Semantic truth still depends on the original request. Structural integrity, traceability, and packaging readiness are enforced by code.

---

## The Spec Structure

The operational contract lives in `spec.yaml`. Every other artifact is a view of the same content.

| Area | Fields | Role |
|---|---|---|
| Identity | `version`, `title`, `objective` | What is being built and why |
| Execution | `execution_mode` | How the run should proceed |
| Context | `context.system`, `context.assumptions` | Environment framing and explicit premises |
| Boundaries | `constraints` | Hard limits — what must stay true or stay out |
| Outcomes | `success_criteria`, `required_evidence` | What "done" means and what proof is required |
| Reasoning | `hypotheses` | Working beliefs with `id`, `description`, `confidence` (0–1) |
| Work plan | `actions` | Discrete steps with `id`, `type`, `supports` (hypothesis links) |
| Governance | `decision_rules` | When to stop, escalate, or choose between options |
| Provenance | `metadata` | Source prompt, generator, model, scope contract |

### Traceability graph

Each action can list hypothesis IDs in `supports`. This links planned work to the hypotheses it validates, so the spec is auditable as a directed graph — not a flat checklist. The linter enforces that every hypothesis is referenced by at least one action when policy requires it.

### Scope contract

`metadata.scope_contract` holds two explicit fences:

```yaml
must_include:   # items that must remain in scope
must_not_include: # items explicitly fenced out
```

This feeds scope evaluation and makes drift detectable against the original intent.

---

## What Lint Checks

The lint layer applies deterministic checks over the generated spec:

- Required fields and expected types
- Minimum content counts per section
- Hypothesis ID format and confidence range
- Action ID, type, and confirmation flags
- Traceability links from actions to hypotheses via `supports`
- Required metadata fields
- Duplicate or near-duplicate list entries

This gives every compilation a machine-checkable quality gate before the artifacts reach a coding agent.

---

## Why This Works For Claude

Claude performs best when the execution surface is compact, explicit, and revisitable. A long implementation session is easier to control when constraints are already materialized in files the agent can re-read at any step:

- **one file** for the operational spec
- **one file** for persistent memory
- **one checklist** for acceptance
- **one command** as the implementation entrypoint

That structure reduces accidental scope expansion and raises the chance of reproducible delivery across runs.

---

## API Key Setup

Create `./.venv/.env`:

```env
# Anthropic
ANTHROPIC_API_KEY="sk-ant-..."
ANTHROPIC_MODEL="claude-sonnet-4-6"

# or OpenAI
OPENAI_API_KEY="sk-..."
OPENAI_MODEL="gpt-4o"
```

Or export directly:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

---

## Compiler Policy

An optional policy file controls how strict compilation and the pass gate should be.

**Default path:** `./.specforge-policy.yaml`  
**Override:** `export SPECFORGE_POLICY=/path/to/policy.yaml`

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

---

## Architecture

```
src/opsspec/
├── cli.py           ← user flow and interactive session
├── generator.py     ← compiles draft JSON into internal Spec model
├── linting.py       ← deterministic quality checks
├── scope_eval.py    ← evaluates scope contract adherence
├── claude_skill.py  ← writes the Claude artifact bundle
└── nlp_policy.py    ← loads policy and scoring configuration

.claude/skills/
├── specforge/           ← MCP-aware spec compilation skill
└── specforge-implement/ ← implementation-only skill for existing bundles

examples/
├── sample-bundle/   ← reference output: parser CLI
└── mini-os/         ← reference output: bare-metal x86 OS
```

---

## Case Study: Building a Bare-Metal OS

The `examples/mini-os/` directory is a complete end-to-end demonstration. Starting from a three-word prompt, SpecForge compiled a full spec, and `/implement-from-spec` built a bootable x86 disk image.

![MiniOS v0.1 running in QEMU — boot summary, memory map, and GDT](docs/minios-qemu.png)

### The original prompt

```
build a simple operating system
```

### What the spec compiled

Running `/specforge` against that prompt produced the full bundle in one pass:

**Objective** — 512-byte BIOS bootloader + freestanding C kernel → VGA text output → boots in QEMU from a raw disk image. No external libraries. No runtime.

**Hard constraints from `spec.yaml`:**
- Bootloader must be exactly 512 bytes, ending with `0xAA55` BIOS signature
- Kernel is freestanding C only — no libc, no crt0, no runtime
- Zero external libraries; toolchain is `nasm` + `gcc -m32` + `ld`
- All files inside `examples/mini-os/`
- `make run` is the single command to boot in QEMU

**Hypotheses the spec reasoned over:**

| ID | Claim | Confidence |
|---|---|---|
| h1 | A 512-byte NASM bootloader can load, switch to protected mode, and hand off to a C kernel at `0x1000` | 0.95 |
| h2 | A freestanding C kernel can write directly to VGA framebuffer `0xB8000`, producing readable coloured output | 0.97 |
| h3 | A Makefile using only nasm + gcc -m32 + ld can produce a bootable raw image runnable in `qemu-system-x86_64` | 0.92 |

**Actions the spec decomposed the work into:**

| ID | Type | Description |
|---|---|---|
| a1 | design | Create directory layout: `boot/`, `kernel/`, `linker.ld`, `Makefile` |
| a2 | implement | Write `boot/boot.asm` — 16-bit startup, INT 13h disk read, A20, GDT, protected-mode switch, jump to `0x1000` |
| a3 | implement | Write `kernel/kernel.c` — VGA helpers and `kernel_main` banner |
| a4 | implement | Write `linker.ld` — sections at `0x1000`, flat binary output |
| a5 | implement | Write `Makefile` — `all`, `run`, `clean` targets; produce `build/os.img` |
| a6 | validate | Run `make`, check `boot.bin` size, boot in QEMU, verify VGA output |

Each action declares `supports` links to the hypotheses it validates — the spec is auditable as a graph.

**Scope contract — what the spec explicitly fenced out:**

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
  - keyboard or interrupt handling
  - multitasking or scheduling
  - anything outside examples/mini-os/
```

### Scope drift evaluation

`evals/scope_drift_cases.yaml` holds 11 machine-checkable seeds derived from the spec:

- **6 negative checks** — patterns that must never appear: `#include <stdio.h>`, `-lpthread`, IDT setup, scheduler keywords
- **5 positive checks** — files that must exist and contain specific values: `0xAA55`, `0xB8000`, `-ffreestanding`

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

The key shift is *when* the error was caught: **not at runtime, but while writing.**

Without a spec, the loop is: write → run → fail → diagnose → fix. With a spec, known failure modes are written down before the first file exists. The agent reads them during implementation and writes code that already satisfies the constraint. The failure never materializes.

#### Errors caught while writing

**Wrong linker output format.** The linker defaults to ELF format even when you need a raw binary. QEMU loads the image, the boot check passes, and execution jumps into header bytes instead of code. The screen goes black — identical in appearance to a wrong load address or a missing boot signature. Three different root causes, one symptom. Without foreknowledge, diagnosis is a guessing game. The spec had the fix written down before the Makefile existed: always pass `--oformat binary`. The agent applied it during authoring. The black screen never happened.

**Bootloader overflow.** The bootloader must fit in exactly 512 bytes, and the last two bytes are a fixed boot signature the BIOS requires to recognize the disk as bootable. If the binary grows too large and you trim the wrong thing — including the signature — the machine simply refuses to boot with no error output. The spec made the priority explicit before the assembler file was written: trim strings or data, never the signature. The agent never had to make that call under pressure.

**Garbled screen output.** Each character cell on the screen is encoded as two bytes: color first, character second. Swap the order and every cell renders as a random glyph — the screen fills with output that looks alive but is completely unreadable. The correct encoding was in the spec before the display code was written. The agent applied it directly. There was no garbled screen to debug.

#### Errors caught while writing — but only after being discovered first

Some failures were not anticipated. They hit at runtime. But once discovered, they were logged into a persistent memory file the agent reads at the start of every session — so the next run starts with that knowledge already in place.

**Wrong function at the kernel entry point.** The bootloader jumps to a fixed memory address expecting to land on the kernel's main function. But the C compiler places functions in whatever order it chooses — and helper functions like screen clear or string print often end up before the main function in the final binary. The bootloader lands in the middle of a helper, the kernel crashes silently, and nothing appears on screen. Once discovered, the fix — forcing the entry point to always be first — was logged permanently. Every subsequent run inherits it and writes the correct code from the start.

**Compiler incompatibility on Apple Silicon.** The standard 32-bit compile flag does not work on Apple Silicon Macs. The error looks like a missing installation rather than an architecture mismatch, making it easy to spend time reinstalling tools that are already correct. Once the real cause was identified and the right cross-compiler documented, that knowledge carried forward to every future run on that platform.

#### Scope creep — the failure that would never have shown up on its own

An agent asked to "build a simple OS" has a natural instinct to keep adding things: keyboard input, a basic scheduler, interrupt handling. Each addition feels helpful. None of them announce themselves as out of scope — they just accumulate quietly.

The spec's explicit list of what must *not* be included made the boundary visible before implementation began. Without it, scope drift would only become apparent when the user reviewed the final output and found an OS that did more than they asked for.

---

## What's Next

- Conflict-mediation structure for specs with contradictory requirements
