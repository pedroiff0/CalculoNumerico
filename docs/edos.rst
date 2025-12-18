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

O teste de integração que valida a opção de resolução de EDOs está em::

    pytest tests/test_inputs_calcnum.py::test_calcnum_inputs_basic -q

Teste correspondente: :file:`tests/inputs/inputEDOS.txt`

Testes Unitários (visíveis)
---------------------------

Abaixo está o arquivo de testes unitários para a funcionalidade de EDOs. Ele é incluído para fácil visualização e referência.

.. literalinclude:: ../tests/test_edos.py
    :language: python
    :linenos:

Links rápidos
-------------

- Teste de integração relacionado: :file:`tests/test_inputs_calcnum.py::test_calcnum_inputs_basic`
- Testes unitários: :file:`tests/test_edos.py`
