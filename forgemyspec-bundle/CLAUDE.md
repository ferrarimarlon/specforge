# CLAUDE.md

## Role
You are implementing from spec-first constraints. Prioritize determinism, traceability, and quality.

## Persistent Memory Policy
- This file is project memory and should persist across sessions.
- Update only stable project knowledge (decisions, conventions, pitfalls).
- Do not store ephemeral logs or temporary debugging notes here.

## Current Spec Snapshot
- Title: Criar um jogo da velha
- Objective: Especificar e implementar um jogo da velha funcional.

## Non-Negotiable Guardrails
- Não adicionar funcionalidades não solicitadas, como modo online, ranking ou animações.
- Manter as regras tradicionais do jogo da velha 3x3.
- Usar uma implementação simples e executável.
- Se linguagem ou plataforma não forem informadas, tratar como decisão em aberto e registrar a suposição adotada.

## Decision Rules
- Se o usuário não informar linguagem, manter a escolha de tecnologia como suposição explícita e não como requisito confirmado.
- Se houver conflito entre simplicidade e recursos extras, priorizar a versão básica funcional.
- Se a interface não for especificada, usar interface textual simples como padrão.
- Não executar ações destrutivas ou que alterem sistemas externos, pois não são necessárias para este objetivo.

## Success Criteria
- O jogo permite iniciar uma partida de jogo da velha 3x3.
- Dois jogadores podem alternar jogadas válidas.
- O sistema impede jogadas em posições ocupadas ou fora do tabuleiro.
- O jogo detecta corretamente vitória por linha, coluna ou diagonal.
- O jogo detecta corretamente empate quando o tabuleiro é preenchido sem vencedor.
- Há evidência executável ou demonstrável do funcionamento básico do jogo.

## Assumptions
- Assumir implementação básica e completa do jogo da velha tradicional 3x3.
- Assumir interface textual simples como padrão, por ausência de requisito de interface gráfica.
- Assumir modo para dois jogadores locais, por ausência de pedido de IA ou modo online.

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
