Interpolações
==============

Funções do módulo :mod:`codigos.interpolacoes` para interpolação (Newton, Lagrange, Gregory-Newton).

Documentação da API
--------------------

.. automodule:: codigos.interpolacoes
    :members:
    :noindex:

Exemplo de Uso
--------------

.. literalinclude:: ../tests/exemplos/exemplo_interpolacoes.py
    :language: python
    :linenos:

Testes de Integração
--------------------

Coberto pelos seguintes testes:

- **Teste global**: ``pytest -q`` (roda todos os testes do projeto)
- **Teste de calcnum**: ``pytest tests/test_inputs_calcnum.py::test_calcnum_inputs_basic -q`` (valida integração via menu principal)
- **Teste individual**: ``pytest tests/test_interpolacoes.py -v`` (testes específicos do módulo)

Teste correspondente: :file:`tests/inputs/inputInterpolacoes.txt`

Testes Unitários (visíveis)
---------------------------

:doc:`tests/test_interpolacoes`

Links rápidos
-------------

- Teste de integração relacionado: :file:`tests/test_inputs_calcnum.py::test_calcnum_inputs_basic`
- Testes unitários (arquivo): :file:`tests/test_interpolacoes.py`
- Página de testes (docs): :doc:`tests/test_interpolacoes`