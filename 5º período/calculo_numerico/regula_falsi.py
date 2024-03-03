ERRO = 10e-16
a = 0.5
b = 1.0

def eq(x):
    return x**3 - 9*x + 5

while True:
    c = b - eq(b)*((b-a))/(eq(b)-eq(a))
    if abs(eq(c)) <= ERRO:
        print(f"\nA raiz aproximada aparece em {c} e tem valor aproximado de {eq(c)}\n")
        break

    if(eq(a) * eq(c)) > 0:
        a = c
    
    elif(eq(b) * eq(c)) > 0:
        b = c