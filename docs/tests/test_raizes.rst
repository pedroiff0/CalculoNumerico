Testes: test_raizes
-------------------

Testes para o módulo `codigos.raizes`.

- Bisseção: validade do intervalo, comportamento em intervalos inválidos e saída em verbose
- Newton: convergência básica e comportamento quando a derivada é nula
- Secante: convergência básica
- `pedir_dados_raizes`: valida leitura de parâmetros no modo de menu

Conteúdo dos testes: 

.. literalinclude:: ../../tests/test_raizes.py
   :language: python
   :linenos:

Resumo das funções de teste:

- **test_bissecao_basic**: Verifica a convergência básica do método da bisseção.
- **test_bissecao_invalid_interval**: Confirma que bisseção detecta intervalo inválido (mesmo sinal em extremidades).
- **test_newton_basic**: Verifica convergência do método de Newton-Raphson para raiz sqrt(2).
- **test_newton_derivative_zero**: Testa o comportamento de Newton quando a derivada é zero no ponto inicial.
- **test_secante_basic**: Verifica que o método da secante convergente para uma raiz em (0,1).
- **test_pedir_dados_raizes_for_menu**: Simula a leitura de parâmetros no modo de menu para a bisseção.
- **test_plotar_funcao_grafico_false**: _Sem docstring._
- **test_plotar_funcao_grafico_true**: _Sem docstring._
- **test_bissecao_with_verbose**: _Sem docstring._
- **test_plotar_funcao_grafico_false**: Garante que `plotar_funcao(..., grafico=False)` não chama `plt.show()`.
- **test_plotar_funcao_grafico_true**: Garante que `plotar_funcao(..., grafico=True)` chama `plt.show()`.
- **test_bissecao_with_verbose**: Verifica que `bissecao` funciona corretamente em modo `verbose`.
