from pysr import PySRRegressor

x0 = []
sigma1 = []
sigma2 = []
sigma3 = []
G0 = []
WA = []
esq = [] # Frequência que resulta no -3dB que está à direita de x0
dir = [] # Frequência que resulta no -3dB que está à esquerda de x0
media = [] #(dir + esq)/2
diferenca = [] #dir - esq

# Coleta os dados do arquivo ===============================================
with open('dados.txt', 'r') as arquivo:
    linhas = arquivo.readlines()

for linha in linhas:
    # Serve para tirar os '\n' e espaços
    valores = linha.strip().split(',')
    
    x0.append(float(valores[0]))
    sigma1.append(float(valores[1]))
    sigma2.append(float(valores[2]))
    sigma3.append(float(valores[3]))
    G0.append(float(valores[4]))
    WA.append(float(valores[5]))
    esq.append(float(valores[6]))
    dir.append(float(valores[7]))
    media.append(float(valores[8]))
    diferenca.append(float(valores[9]))
dados = [x0, sigma1, sigma2, sigma3, G0, WA, media, diferenca]
#dados = [x0, sigma1, sigma2, sigma3, G0, WA, esq, dir, media, diferenca]
dados_transpostos = list(map(list, zip(*dados)))
# ==========================================================================

# Mudar aqui pra fazer funcionar
model = PySRRegressor(
    niterations=40,  # < Increase me for better results
    binary_operators=["+", "*", "-"],
    unary_operators=[
        "cos",
        "exp",
        "sin",
        "inv(x) = 1/x",
        # ^ Custom operator (julia syntax)
    ],
    extra_sympy_mappings={"inv": lambda x: 1 / x},
    # ^ Define operator for SymPy as well
    loss="loss(prediction, target) = (prediction - target)^2",
    # ^ Custom loss function (julia syntax)
)

model.fit(dados_transpostos,esq)

#model.fit(X, y)

print(model)