Matriz de Cobertura — `calcnum`
================================

Esta página apresenta o estado atual de testes, documentação e exemplos para as
funcionalidades principais expostas pelo `menu_principal` em :mod:`codigos.calcnum`.

.. list-table:: Matriz de Cobertura — `calcnum`
   :header-rows: 1

   * - Item do Menu
     - Módulo(s)
     - Testes (mód.)
     - Testes (calcnum)
     - Sphinx/Tutorial
     - Exemplos (tests/examples/)
   * - 1 - Conversão de Bases
     - :mod:`codigos.bases`
     - Yes (partial)
     - Partial
     - Yes (modules)
     - No
   * - 2 - Sistemas Lineares
     - :mod:`codigos.calcnum`
     - Partial
     - Partial
     - Yes (calcnum)
     - Yes (``tests/examples/solve_system.py``)
   * - 3 - Interpolações
     - :mod:`codigos.interpolacoes`
     - Yes
     - Partial
     - Yes (modules)
     - No
   * - 4 - Ajustes de Curvas
     - :mod:`codigos.ajustecurvas`
     - Partial
     - Partial
     - Yes (modules)
     - No
   * - 5 - Equações Diferenciais
     - :mod:`codigos.EDOs` / calc
     - Yes
     - Partial (menu)
     - Yes (EDOs.rst)
     - Yes (``tests/examples/edo_example.py``)
   * - 6 - Integração Numérica
     - :mod:`codigos.integracoes`
     - Yes
     - Partial
     - Yes (modules)
     - No
   * - 7 - Métodos de Raízes
     - :mod:`codigos.raizes`
     - Partial
     - Partial
     - Yes (modules)
     - Yes (``tests/examples/simple_root_find.py``)


Legenda: "Partial" indica que há testes/documentação mas nem todas as funções
públicas foram cobertas ainda.

Próximas ações recomendadas
---------------------------

- Completar testes unitários para todas as funções públicas em `codigos/calcnum.py`.
- Adicionar testes de integração que executem `calcnum.py` e escolham cada opção do
  `menu_principal` via arquivos de input (um por menu item) para garantir comportamento
  não interativo (adequado ao CI).
- Criar tutoriais Sphinx por item de menu com snippets completos e exemplos vinculados
  aos scripts em `examples/`.
