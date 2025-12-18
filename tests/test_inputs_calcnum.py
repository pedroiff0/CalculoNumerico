import subprocess
import sys
import os
import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
INPUT_DIR = os.path.join(os.path.dirname(__file__), 'inputs')


def run_input_file_calc(fname):
    path = os.path.join(INPUT_DIR, fname)
    with open(path, 'r', encoding='utf-8') as fh:
        data = fh.read()
    env = dict(os.environ)
    env['MPLBACKEND'] = env.get('MPLBACKEND', 'Agg')
    # Execute the package entry to call menu_principal() so imports work
    cmd = [sys.executable, '-c', "import codigos.calcnum as m; m.menu_principal()"]
    proc = subprocess.run(cmd, input=data, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=ROOT, text=True, timeout=30, env=env)
    return proc.returncode, proc.stdout


@pytest.mark.parametrize('fname,expected', [
    ('inputBases.txt', ('Binário', '1011')),
    ('inputSistemas.txt', ('Solução',)),
    ('inputInterpolacoes.txt', ('Resultado (Newton)',)),
    ('inputAjustes.txt', ('Polinômio interpolador',)),
    ('inputEDOS_calcnum.txt', ('Tabela de resultados', 'Aproximação', 'y(1)')),
    ('inputIntegracoes_calcnum.txt', ('Resultado',)),
    ('inputRaizes.txt', ('A raiz encontrada',)),
])
def test_calcnum_inputs_basic(fname, expected):
    rc, out = run_input_file_calc(fname)
    print('\n--- output for', fname, '---')
    print(out)
    assert any(s in out for s in expected)
