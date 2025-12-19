"""Gera páginas ReST dos testes unitários e um índice para Sphinx.

Localização: docs/scripts/generate_tests_docs.py (para facilitar inclusão no repositório/docs).

Este script procura arquivos em `<project_root>/tests/test_*.py`, extrai a docstring do módulo
e as docstrings das funções `test_*` e escreve `docs/tests_unitarios.rst` e páginas em
`docs/tests/` (cada arquivo `test_<mod>.rst`).
"""
import ast
from pathlib import Path

# Determina a raiz do projeto procurando a primeira pasta que contenha 'tests'
# a partir do diretório do script e subindo na árvore.
HERE = Path(__file__).resolve()
for p in [HERE, *HERE.parents]:
    if (p / 'tests').is_dir() and (p / 'docs').is_dir():
        PROJECT_ROOT = p
        break
else:
    # Fallback razoável: dois níveis acima (quando executado a partir de docs/scripts)
    PROJECT_ROOT = HERE.parents[2]

TESTS_DIR = PROJECT_ROOT / "tests"
OUT_DIR = PROJECT_ROOT / "docs"
OUT_DIR.mkdir(exist_ok=True)
RST_DIR = OUT_DIR / "tests"
RST_DIR.mkdir(exist_ok=True)

INDEX_PATH = OUT_DIR / "tests_unitarios.rst"

index_lines = ["Documentação dos Testes Unitários\n"]
index_lines.append("=" * len(index_lines[0].rstrip("\n")) + "\n\n")
index_lines.append("Este documento lista os testes por módulo com suas docstrings. \n\n")
index_lines.append(".. toctree::\n")
index_lines.append("   :maxdepth: 1\n\n")

for test_file in sorted(TESTS_DIR.glob('test_*.py')):
    name = test_file.stem
    src = test_file.read_text(encoding='utf-8')
    tree = ast.parse(src)
    module_doc = ast.get_docstring(tree) or ''

    # create per-module rst
    rst_path = RST_DIR / f"{name}.rst"
    with rst_path.open('w', encoding='utf-8') as fh:
        title = f"Testes: {name}"
        fh.write(title + "\n" + ("-" * len(title)) + "\n\n")
        if module_doc:
            fh.write(module_doc + "\n\n")
        else:
            fh.write("_Sem docstring de módulo._\n\n")

        fh.write("Conteúdo dos testes: \n\n")
        # Ajuste do caminho relativo correto: a partir de docs/tests, ir até a pasta tests do projeto
        fh.write(f".. literalinclude:: ../../tests/{test_file.name}\n   :language: python\n   :linenos:\n\n")

        # add a brief summary of test functions
        fh.write("Resumo das funções de teste:\n\n")
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                func_doc = ast.get_docstring(node) or '_Sem docstring._'
                first_line = func_doc.splitlines()[0] if func_doc else '_Sem docstring._'
                fh.write(f"- **{node.name}**: {first_line}\n")

    # add to index toctree entry (relative path)
    index_lines.append(f"   tests/{name}\n")

# write top-level index rst
INDEX_PATH.write_text(''.join(index_lines), encoding='utf-8')
print(f"Gerados {INDEX_PATH} e páginas em {RST_DIR}")