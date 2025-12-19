Integrações Numéricas
======================

Funções do módulo :mod:`codigos.integracoes` para regras compostas e auxiliares.

Documentação
------------

.. automodule:: codigos.integracoes
    :members: newton_cotes, trapezio_composta, simpson_1_3_composta, simpson_3_8_composta, pedir_dados_integral, pedir_m_ou_h, erro_truncamento_composta
    :noindex:

Exemplo de Uso
--------------

.. literalinclude:: ../tests/exemplos/exemplo_integracoes.py
    :language: python
    :linenos:

Testes de Integração
--------------------

Coberto pelos seguintes testes:

- **Teste global**: ``pytest -q`` (roda todos os testes do projeto)
- **Teste de calcnum**: ``pytest tests/test_inputs_calcnum.py::test_calcnum_inputs_basic -q`` (valida integração via menu principal)
- **Teste individual**: ``pytest tests/test_integracoes.py -v`` (testes específicos do módulo)

Teste correspondente: :file:`tests/inputs/inputIntegracoes_calcnum.txt`

Testes Unitários (visíveis)
---------------------------

:doc:`tests/test_integracoes`

Links rápidos
-------------

- Teste de integração relacionado: :file:`tests/test_inputs_calcnum.py::test_calcnum_inputs_basic`
- Testes unitários (arquivo): :file:`tests/test_integracoes.py`
- Página de testes (docs): :doc:`tests/test_integracoes`