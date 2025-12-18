Aviso — Passos futuros
=======================

Esta seção descreve passos recomendados e diretrizes para manter a qualidade da base de código e da documentação:

- Escrever testes unitários para **todas** as funções públicas em `codigos/calcnum.py`.
- Garantir que todos os *exemplos* estejam em `tests/exemplos/` e sejam incluídos nas páginas de tutorial via `.. literalinclude::`.
- Alterações estruturais (renomeações ou remoção de arquivos) devem ser realizadas somente com autorização prévia do mantenedor principal.
- Adotar execução contínua de testes e build de documentação no CI (ex.: `pytest` + `sphinx-build -W`).

Contribuições são bem-vindas: abra issue ou PR com propostas concretas e um rascunho das mudanças planejadas.