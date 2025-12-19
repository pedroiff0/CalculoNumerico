Métodos de Raízes
=================

Funções do módulo :mod:`codigos.raizes` para cálculo de raízes (Bisseção, Newton, Secante).

Documentação
------------

.. automodule:: codigos.raizes
    :members: bissecao, newton, secante, pedir_dados_raizes
    :noindex:

Exemplo de Uso
--------------

.. literalinclude:: ../tests/exemplos/exemplo_busca_raiz.py
    :language: python
    :linenos:

Testes de Integração
--------------------

Coberto pelos seguintes testes:

- **Teste global**: ``pytest -q`` (roda todos os testes do projeto)
- **Teste de calcnum**: ``pytest tests/test_inputs_calcnum.py::test_calcnum_inputs_basic -q`` (valida integração via menu principal)
- **Teste individual**: ``pytest tests/test_raizes.py -v`` (testes específicos do módulo)

Teste correspondente: :file:`tests/inputs/inputRaizes.txt`

Testes Unitários (visíveis)
---------------------------

:doc:`tests/test_raizes`

Links rápidos
-------------

- Testes unitários (arquivo): :file:`tests/test_raizes.py`
- Página de testes (docs): :doc:`tests/test_raizes`