Testes: test_integracoes
------------------------

Testes para o módulo `codigos.integracoes`.

Verifica fórmula de erro de truncamento, regras Newton-Cotes (Trapézio,
Simpson 1/3, Simpson 3/8), e comportamento em modo verbose e não-interativo.

Conteúdo dos testes: 

.. literalinclude:: ../../tests/test_integracoes.py
   :language: python
   :linenos:

Resumo das funções de teste:

- **test_erro_truncamento_composta**: Verifica as fórmulas de estimativa de erro de truncamento para regras compostas.
- **test_trapezio_composta_simple**: Integra f(x)=x no intervalo [0,1] usando Trapézio composta e compara com 0.5.
- **test_erro_truncamento_composta_values**: Valida valores numéricos das fórmulas de erro para casos concretos.
- **test_newton_cotes_trapezio_linear**: Integral de f(x)=x no intervalo [0,1] com Newton-Cotes (trapézio simples).
- **test_newton_cotes_verbose_and_vectorized**: Verifica que caminho vetorizado e verbose imprimem uma linha de resultado.
- **test_trapezio_composta_verbose_estimativa**: Verifica estimativa automática de erro em modo verbose para Trapézio composta.
- **test_newton_cotes_invalid_limits**: Limites inválidos devem provocar exceções apropriadas.
- **test_newton_cotes_simpson_on_quadratic**: Simpson 1/3 deve integrar x**2 exatamente em [0,1]
- **test_trapezio_composta_monkeypatch**: Teste com m fixo via monkeypatch para Trapézio composta.
- **test_simpson_1_3_composta_monkeypatch**: Simpson 1/3 composta com m par (m=4).
- **test_simpson_3_8_composta_monkeypatch**: Simpson 3/8 composta com m múltiplo de 3 (m=3).
