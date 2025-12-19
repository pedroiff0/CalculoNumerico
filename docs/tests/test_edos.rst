Testes: test_edos
-----------------

Testes para o módulo `codigos.edos`.

Cobre solver Runge-Kutta (ordens 1-4) para EDOs escalares e sistemas, bem
como validações de entradas e tratamento de passos/resíduos.

Conteúdo dos testes: 

.. literalinclude:: ../../tests/test_edos.py
   :language: python
   :linenos:

Resumo das funções de teste:

- **test_runge_kutta_scalar_exp**: Verifica RK (4ª ordem) para dy/dx = y com y(0)=1; y(1) ≈ e.
- **test_runge_kutta_system_exp**: Sistema simples: u0' = u0, u1' = 2*u1; verifica solução analítica em t=1.
- **test_passos_edo_with_m**: Verifica cálculo de h e xn dado número de subintervalos m.
- **test_runge_kutta_orders_accuracy**: Valida precisão aproximada por ordem do método Runge-Kutta.
- **test_runge_kutta_h_nonpositive_raises**: h <= 0 deve levantar ValueError.
- **test_runge_kutta_sistema_last_step**: Garante que o tempo final coincide exatamente com tf quando o último passo é menor que h.
- **test_runge_kutta_sistema_predator_prey**: Teste qualitativo da simulação de Lotka-Volterra (predador-presa).
- **test_runge_kutta_negative_h_raises**: _Sem docstring._
- **test_runge_kutta_invalid_order_raises**: _Sem docstring._
