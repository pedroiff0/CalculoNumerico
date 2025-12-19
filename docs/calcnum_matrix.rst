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
     - Exemplos (tests/exemplos/)
     - Documentação Individual
     - Testes Individuais
   * - 1 - Conversão de Bases
     - :mod:`codigos.bases`
     - Yes
     - Yes
     - Yes
     - :file:`tests/exemplos/exemplo_bases.py`
     - :doc:`bases`
     - :doc:`tests/test_bases`
   * - 2 - Sistemas Lineares
     - :mod:`codigos.sistemaslineares`
     - Yes
     - Yes
     - Yes
     - :file:`tests/exemplos/exemplo_resolver_sistema.py`
     - :doc:`sistemas`
     - :doc:`tests/test_sistemaslineares`
   * - 3 - Interpolações
     - :mod:`codigos.interpolacoes`
     - Yes
     - Yes
     - Yes
     - :file:`tests/exemplos/exemplo_interpolacoes.py`
     - :doc:`interpolacoes`
     - :doc:`tests/test_interpolacoes`
   * - 4 - Ajustes de Curvas
     - :mod:`codigos.ajustecurvas`
     - Yes
     - Yes
     - Yes
     - :file:`tests/exemplos/exemplo_ajuste_curvas.py`
     - :doc:`ajustes`
     - :doc:`tests/test_ajustecurvas`
   * - 5 - Equações Diferenciais
     - :mod:`codigos.edos`
     - Yes
     - Yes
     - Yes
     - :file:`tests/exemplos/exemplo_edos.py`
     - :doc:`edos`
     - :doc:`tests/test_edos`
   * - 6 - Integração Numérica
     - :mod:`codigos.integracoes`
     - Yes
     - Yes
     - Yes
     - :file:`tests/exemplos/exemplo_integracoes.py`
     - :doc:`integracoes`
     - :doc:`tests/test_integracoes`
   * - 7 - Métodos de Raízes
     - :mod:`codigos.raizes`
     - Yes
     - Yes
     - Yes
     - :file:`tests/exemplos/exemplo_busca_raiz.py`
     - :doc:`raizes`
     - :doc:`tests/test_raizes`


Legenda: "Partial" indica que há testes/documentação mas nem todas as funções
públicas foram cobertas ainda.
