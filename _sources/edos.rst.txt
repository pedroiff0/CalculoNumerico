Equações Diferenciais Ordinárias (EDOs)
========================================

Documentação das funções do módulo :mod:`codigos.edos` relacionadas à resolução de equações diferenciais ordinárias usando métodos numéricos como Runge-Kutta e Euler.

Documentação
-------------

As funções listadas abaixo implementam métodos numéricos para resolver EDOs de primeira e segunda ordem, sistemas de EDOs, com opções para diferentes ordens de Runge-Kutta e visualização de resultados.

.. automodule:: codigos.edos
    :members: runge_kutta, executar_runge_kutta, runge_kutta_sistema, executar_sistema_edos, executar_edo_2ordem, resolver_edo_2ordem
    :noindex:

Exemplo de Uso
--------------

.. literalinclude:: ../tests/exemplos/exemplo_edos.py
    :language: python
    :linenos:

Testes de Integração
--------------------

Coberto pelos seguintes testes:

- **Teste global**: ``pytest -q`` (roda todos os testes do projeto)
- **Teste de calcnum**: ``pytest tests/test_inputs_calcnum.py::test_calcnum_inputs_basic -q`` (valida integração via menu principal)
- **Teste individual**: ``pytest tests/test_edos.py -v`` (testes específicos do módulo)

Teste correspondente: :file:`tests/inputs/inputEDOS.txt`

Testes Unitários (visíveis)
---------------------------

:doc:`tests/test_edos`

Links rápidos
-------------

- Teste de integração relacionado: :file:`tests/test_inputs_calcnum.py::test_calcnum_inputs_basic`
- Testes unitários (arquivo): :file:`tests/test_edos.py`
- Página de testes (docs): :doc:`tests/test_edos`
