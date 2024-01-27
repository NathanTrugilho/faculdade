from pysr import PySRRegressor

x0 = []
sigma1 = []
sigma2 = []
sigma3 = []
#G0 = []
WA = []
delta = [] #(dir - esq)/2

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
    #G0.append(float(valores[4]))
    WA.append(float(valores[4]))
    delta.append(float(valores[5]))

dados = [x0, sigma1, sigma2, sigma3, WA]#, G0]
dados_transpostos = list(map(list, zip(*dados)))

# Configurações ====================================================================== 
model = PySRRegressor(
    model_selection="accuracy",
    niterations=1000,  # < Increase me for better results
    binary_operators=["+", "*", "-", "/"],
    progress=False,
    populations=50,
    population_size=100,
    maxsize=16,
    delete_tempfiles=True,
    # ^ Mostra apenas as equações finais, sem mostrar o progresso
    unary_operators=[
        "sin",
        "cos",
        "exp",
        "log",
        "inv(x) = 1/x",
        # ^ Custom operator (julia syntax)
    ],
    extra_sympy_mappings={"inv": lambda x: 1 / x},
    # ^ Define operator for SymPy as well
    warm_start=True,
    turbo=True,
    batching=True,
    # ^ Faz com que o pysr rode a partir de um progresso já feito (a partir de um Hall_of_fame da vida)
    loss="loss(prediction, target) = (prediction - target)^2",
    # ^ Custom loss function (julia syntax)
)

model.fit(dados_transpostos, delta)

print(model)