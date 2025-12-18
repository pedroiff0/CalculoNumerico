Aviso — Passos futuros
=======================

Esta seção descreve os passos futuros recomendados para completar a cobertura de
testes e documentação:

- Escrever testes unitários para **todas** as funções públicas em `codigos/calcnum.py`.
- Garantir exemplos em `tests/examples/` para todos os tópicos e usá-los via
  `.. literalinclude::` nas páginas dos tutoriais.
- Adicionar cobertura de testes automatizada e análise estática (ex.: `pytest` + `coverage`).
- Atualizar o CI para executar a suíte de testes e build da documentação em PRs.
- Refatorar funções grandes em `calcnum.py` em módulos menores para teste e manutenção mais fáceis.

Contribuições são bem-vindas: abra issue ou PR com propostas concretas.
