# Acceptance Checklist

## Scope
- [ ] Objective implemented exactly: Especificar e implementar um jogo da velha funcional.
- [ ] No unrequested features were introduced
- [ ] All assumptions are explicit and justified

## Success Criteria
- [ ] O jogo permite iniciar uma partida de jogo da velha 3x3.
- [ ] Dois jogadores podem alternar jogadas válidas.
- [ ] O sistema impede jogadas em posições ocupadas ou fora do tabuleiro.
- [ ] O jogo detecta corretamente vitória por linha, coluna ou diagonal.
- [ ] O jogo detecta corretamente empate quando o tabuleiro é preenchido sem vencedor.
- [ ] Há evidência executável ou demonstrável do funcionamento básico do jogo.

## Required Evidence
- [ ] Código-fonte do jogo da velha.
- [ ] Demonstração de alternância de turnos entre dois jogadores.
- [ ] Evidência de validação de jogadas inválidas.
- [ ] Evidência de detecção de vitória e empate.
- [ ] Registro explícito das suposições adotadas sobre interface e modo de jogo.

## Decision Rules Compliance
- [ ] Se o usuário não informar linguagem, manter a escolha de tecnologia como suposição explícita e não como requisito confirmado.
- [ ] Se houver conflito entre simplicidade e recursos extras, priorizar a versão básica funcional.
- [ ] Se a interface não for especificada, usar interface textual simples como padrão.
- [ ] Não executar ações destrutivas ou que alterem sistemas externos, pois não são necessárias para este objetivo.
