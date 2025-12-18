# Pacote para permitir importações de `codigos.*`
__all__ = ['bases', 'sistemaslineares', 'interpolacoes', 'ajustecurvas', 'integracoes', 'edos', 'raizes', 'calcnum']

# Import modules lazily to make `from codigos import <module>` succeed in CI environments
from . import bases, sistemaslineares, interpolacoes, ajustecurvas, integracoes, edos, raizes, calcnum

# O pacote é composto por módulos individuais; mantenha este arquivo simples para tornar a pasta importável.