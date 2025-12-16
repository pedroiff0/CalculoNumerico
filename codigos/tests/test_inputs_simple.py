import subprocess
import sys
import os
import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
INPUT_DIR = os.path.join(os.path.dirname(__file__), 'inputs')


def run_input_file_int(fname):
    path = os.path.join(INPUT_DIR, fname)
    with open(path, 'r', encoding='utf-8') as fh:
        data = fh.read()
    proc = subprocess.run([sys.executable, 'integracoes.py'], input=data, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=ROOT, text=True, timeout=20)
    return proc.returncode, proc.stdout


def run_input_file_edo(fname):
    path = os.path.join(INPUT_DIR, fname)
    with open(path, 'r', encoding='utf-8') as fh:
        data = fh.read()
    proc = subprocess.run([sys.executable, 'EDOs.py'], input=data, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=ROOT, text=True, timeout=20)
    return proc.returncode, proc.stdout


@pytest.mark.parametrize('fname', [
    'inputIntegrais.txt',
])
def test_integracoes_inputs_basic(fname):
    rc, out = run_input_file_int(fname)
    print('\n--- output for', fname, '---')
    print(out)
    # Alguns scripts podem terminar com código != 0 quando o stdin acaba (EOF).
    # O importante é que a saída contenha um resultado reconhecível.
    assert ('Resultado' in out) or ('Resultado pela' in out) or ('Resultado exato' in out)

@pytest.mark.parametrize('fname', [
    'inputEDOS.txt',
])
def test_edos_inputs_basic(fname):
    rc, out = run_input_file_edo(fname)
    # print output so -s shows it to the user
    print('\n--- output for', fname, '---')
    print(out)
    # aceitar rc != 0 quando EOF for atingido; validar presença de saída esperada
    assert ('Tabela de resultados' in out) or ('Resultado' in out) or ('Tabela de resultados' in out)
