Tutorial — `calcnum`
=====================

Este tutorial mostra como executar o arquivo principal `calcnum.py` de forma não
interativa usando arquivos de entrada em `tests/inputs/` e como reproduzir
os exemplos usados nos testes de integração.

Executando um exemplo (linha de comando)
----------------------------------------

.. code-block:: console

   python calcnum.py < tests/inputs/inputSistemas.txt

O arquivo acima contém as entradas simuladas para a opção "Sistemas Lineares".
Abaixo mostramos um exemplo do conteúdo do arquivo de entrada.

.. literalinclude:: ../tests/inputs/inputSistemas.txt
    :language: text

Outros arquivos de input (exemplos)
-----------------------------------------

- :file:`tests/inputs/inputAjustes.txt`
- :file:`tests/inputs/inputBases.txt`
- :file:`tests/inputs/inputEDOS_calcnum.txt`
- :file:`tests/inputs/inputIntegracoes_calcnum.txt`
- :file:`tests/inputs/inputInterpolacoes.txt`
- :file:`tests/inputs/inputRaizes.txt`

Dica: execute com `python calcnum.py < tests/inputs/<arquivo>` para validar
comportamento de menu de forma repetível e adequada para CI.
