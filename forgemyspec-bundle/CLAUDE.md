# CLAUDE.md

## Role
You are implementing from spec-first constraints. Prioritize determinism, traceability, and quality.

## Persistent Memory Policy
- This file is project memory and should persist across sessions.
- Update only stable project knowledge (decisions, conventions, pitfalls).
- Do not store ephemeral logs or temporary debugging notes here.

## Current Spec Snapshot
- Title: Local Console Tic-Tac-Toe for Two Human Players
- Objective: Create a simple Tic-Tac-Toe game that runs in the console for two human players on the same machine, with no networking and no points or scoring system.

## Non-Negotiable Guardrails
- Must run locally in the console.
- Must support exactly two human players taking turns.
- Must not use networking or any online/multiplayer connectivity.
- Must not include a points, score, or ranking system.
- Should remain simple in structure and interaction.
- Must not require graphical UI components.

## Decision Rules
- If implementation language is unspecified, choose the simplest language supported by the working environment for a console program.
- If input format is unspecified, use a simple and clearly prompted format such as row/column or cell number.
- If a move is invalid, do not switch turns and prompt the same player again.
- If a winning line is detected, end the game immediately and announce the winner.
- If the board is full and no winning line exists, end the game as a draw.
- Do not add AI opponents, networking, persistence, or score tracking unless explicitly requested.

## Success Criteria
- The program starts in a console and allows two human players to play Tic-Tac-Toe on the same machine.
- The board state is displayed in a readable text format after game start and after each valid move.
- Players alternate turns between X and O.
- The program accepts player move input and updates the correct board position when the move is valid.
- The program rejects invalid input or occupied-cell moves and prompts for another move without corrupting game state.
- The program detects and announces a win for X or O when three matching marks align horizontally, vertically, or diagonally.
- The program detects and announces a draw when all cells are filled without a winner.
- The implementation contains no networking features and no scoring or points tracking.

## Assumptions
- The game uses a standard 3x3 Tic-Tac-Toe board.
- Players are represented by X and O.
- Both players use the same console session on one local machine.
- Input is entered via keyboard in the console.
- A single game session is sufficient; persistent score tracking is not required.
- The implementation language is not specified and may be chosen by the coding agent unless constrained by the environment.

## Implementation Protocol
1. Read `spec.yaml` first and implement only traceable scope.
2. If details are missing, document explicit assumptions before coding.
3. Do not add features, frameworks, or layers outside the spec objective.
4. Verify all success criteria with concrete evidence (tests, commands, outputs).
5. Report residual risks and unresolved assumptions in the final summary.

## Decision Log
- (record stable architecture or policy decisions here)

## Known Pitfalls
- (record recurring implementation failure modes here)
