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
     - Yes
     - Yes
     - Yes (modules)
     - Yes (``tests/examples/bases_example.py``)
   * - 2 - Sistemas Lineares
     - :mod:`codigos.sistemaslineares`
     - Yes
     - Yes
     - Yes (modules)
     - Yes (``tests/examples/solve_system.py``)
   * - 3 - Interpolações
     - :mod:`codigos.interpolacoes`
     - Yes
     - Yes
     - Yes (modules)
     - Yes (``tests/examples/interpolacoes_example.py``)
   * - 4 - Ajustes de Curvas
     - :mod:`codigos.ajustecurvasv2`
     - Yes
     - Yes
     - Yes (modules)
     - Yes (``tests/examples/ajustecurvas_example.py``)
   * - 5 - Equações Diferenciais
     - :mod:`codigos.EDOs`
     - Yes
     - Yes (menu)
     - Yes (EDOs.rst)
     - Yes (``tests/examples/edo_example.py``)
   * - 6 - Integração Numérica
     - :mod:`codigos.integracoes`
     - Yes
     - Yes
     - Yes (modules)
     - Yes (``tests/examples/integracoes_example.py``)
   * - 7 - Métodos de Raízes
     - :mod:`codigos.raizes`
     - Yes
     - Yes
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
