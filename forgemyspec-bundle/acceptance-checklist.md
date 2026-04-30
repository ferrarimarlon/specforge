# Acceptance Checklist

## Scope
- [ ] Objective implemented exactly: Create a simple Tic-Tac-Toe game that runs in the console for two human players on the same machine, with no networking and no points or scoring system.
- [ ] No unrequested features were introduced
- [ ] All assumptions are explicit and justified

## Success Criteria
- [ ] The program starts in a console and allows two human players to play Tic-Tac-Toe on the same machine.
- [ ] The board state is displayed in a readable text format after game start and after each valid move.
- [ ] Players alternate turns between X and O.
- [ ] The program accepts player move input and updates the correct board position when the move is valid.
- [ ] The program rejects invalid input or occupied-cell moves and prompts for another move without corrupting game state.
- [ ] The program detects and announces a win for X or O when three matching marks align horizontally, vertically, or diagonally.
- [ ] The program detects and announces a draw when all cells are filled without a winner.
- [ ] The implementation contains no networking features and no scoring or points tracking.

## Required Evidence
- [ ] Source code for the console-based Tic-Tac-Toe game.
- [ ] Evidence that the game runs locally from the console.
- [ ] Example output showing board rendering and alternating turns.
- [ ] Example output showing handling of invalid input or occupied-cell selection.
- [ ] Example output showing a win condition being detected.
- [ ] Example output showing a draw condition being detected.
- [ ] Evidence that no networking code or scoring system is present.

## Decision Rules Compliance
- [ ] If implementation language is unspecified, choose the simplest language supported by the working environment for a console program.
- [ ] If input format is unspecified, use a simple and clearly prompted format such as row/column or cell number.
- [ ] If a move is invalid, do not switch turns and prompt the same player again.
- [ ] If a winning line is detected, end the game immediately and announce the winner.
- [ ] If the board is full and no winning line exists, end the game as a draw.
- [ ] Do not add AI opponents, networking, persistence, or score tracking unless explicitly requested.
