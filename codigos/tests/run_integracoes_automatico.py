import subprocess
import sys
import os

def run_test(inputs, desc):
    print(f"\n=== {desc} ===")
    proc = subprocess.Popen(
        [sys.executable, "integracoes.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=os.path.dirname(__file__),
        text=True
    )
    try:
        out, err = proc.communicate(inputs, timeout=30)
    except subprocess.TimeoutExpired:
        proc.kill()
        print("Timeout!")
        return
    print(out)
    if err:
        print("[stderr]", err)

def main():
    # Teste Trapézio simples
    run_test(
        "1\n"  # Trapézio
        "x**2\n0\n1\nn\nn\n\n"  # função, a, b, composta=n, tabela=n
        , "Trapézio simples, f(x)=x^2, [0,1]"
    )
    # Teste Trapézio composta
    run_test(
        "1\n"  # Trapézio
        "x**2\n0\n1\ns\nn\n10\n\n"  # função, a, b, composta=s, tabela=n, n=10
        , "Trapézio composta, f(x)=x^2, [0,1], n=10"
    )
    # Teste Simpson 1/3 simples
    run_test(
        "2\n"  # Simpson 1/3
        "x**2\n0\n1\nn\nn\n\n"  # função, a, b, composta=n, tabela=n
        , "Simpson 1/3 simples, f(x)=x^2, [0,1]"
    )
    # Teste Simpson 1/3 composta
    run_test(
        "2\n"  # Simpson 1/3
        "x**2\n0\n1\ns\nn\n10\n\n"  # função, a, b, composta=s, tabela=n, n=10
        , "Simpson 1/3 composta, f(x)=x^2, [0,1], n=10"
    )
    # Teste Simpson 3/8 simples
    run_test(
        "3\n"  # Simpson 3/8
        "x**3\n0\n1\nn\nn\n\n"  # função, a, b, composta=n, tabela=n
        , "Simpson 3/8 simples, f(x)=x^3, [0,1]"
    )
    # Teste Simpson 3/8 composta
    run_test(
        "3\n"  # Simpson 3/8
        "x**3\n0\n1\ns\nn\n6\n\n"  # função, a, b, composta=s, tabela=n, n=6
        , "Simpson 3/8 composta, f(x)=x^3, [0,1], n=6"
    )
    # Teste com tabela (Trapézio)
    run_test(
        "1\n"  # Trapézio
        "x**2\n0\n1\nn\ns\n3\n0\n0.5\n1\n0\n0.25\n1\n\n"  # função, a, b, composta=n, tabela=s, n=3, x/y
        , "Trapézio com tabela, f(x)=x^2, x=[0,0.5,1], y=[0,0.25,1]"
    )
    # PDF 1: Simpson 3/8, x**2 + x, [1,2], integral exata e erro
    run_test(
        "3\n"  # Simpson 3/8
        "x**2 + x\n1\n2\nn\nn\n\n"  # função, a, b, composta=n, tabela=n
        "s\n"  # calcular erro
        "2.3333333333333335\n"  # valor exato (analítico)
        , "PDF: Simpson 3/8 simples, f(x)=x**2 + x, [1,2], erro"
    )
    # PDF 2: Simpson 1/3 composta, h=0.1, cos(x), [0,0.8]
    run_test(
        "2\n"  # Simpson 1/3
        "math.cos(x)\n0\n0.8\ns\nn\n8\n\n"  # função, a, b, composta=s, tabela=n, n=8 (h=0.1)
        , "PDF: Simpson 1/3 composta, f(x)=cos(x), [0,0.8], h=0.1"
    )
    # PDF 3: Trapézio com tabela, x=0,2,...,20; y=1.8,2,4,4,6,4,3.6,3.4,2.8
    run_test(
        "1\n"  # Trapézio
        "x\n0\n20\nn\ns\n11\n0\n2\n4\n6\n8\n10\n12\n14\n16\n18\n20\n1.8\n2\n4\n4\n6\n4\n3.6\n3.4\n2.8\n\n"  # função, a, b, composta=n, tabela=s, n=11, x/y
        , "PDF: Trapézio com tabela, x=0,2,...,20; y=1.8,2,4,4,6,4,3.6,3.4,2.8"
    )

if __name__ == "__main__":
    main()
