from pysr import PySRRegressor
import matplotlib.pyplot as plt 
import numpy as np

def pausa_tela():
    input("Pressione 'Enter' para continuar...")

def funcao_filtro(x, x0, G0, WA, sigma1, sigma2, sigma3):
    return G0 * ( ( 2 * ( x - x0 ) / ( sigma1 * WA ) ) ** sigma2 + 1 ) ** ( -2 * sigma3 )

# Usa o cálculo numérico para calcular a frequência do -3dB
def valor_x_direita(x0, G0, WA, sigma1, sigma2, sigma3):
    # Variáveis de inicialização
    RESULTADO = G0 / 2 ** 0.5
    x_esquerda = x0
    x_direita = 100 * x0

    while True:
        # A variável 'media' representa o resultado (f0) que queremos
        # encontrar e será atualizada durante a execução do código
        media = (x_esquerda + x_direita) / 2

        # Verificação da resposta final com a margem de erro de 10^-7
        if abs(RESULTADO - funcao_filtro(media, x0, G0, WA, sigma1, sigma2, sigma3)) < (10**(-7)):
            break

        # Verifica se o valor de H(f) é maior ao -3dB e altera o valor de x
        # que está abaixo do resultado
        elif funcao_filtro(media, x0, G0, WA, sigma1, sigma2, sigma3) <= RESULTADO:
            x_direita = media

        # Verifica se o valor de H(f) é menor ao -3dB e altera o valor de x
        # que está acima do resultado
        elif funcao_filtro(media, x0, G0, WA, sigma1, sigma2, sigma3) > RESULTADO:
            x_esquerda = media

    return media

# Usa o cálculo numérico para calcular a frequência do -3dB
def valor_x_esquerda(x0, G0, WA, sigma1, sigma2, sigma3):
    # Variáveis de inicialização
    RESULTADO = G0 / 2 ** 0.5
    x_esquerda = x0 / 100
    x_direita = x0

    while True:
        # A variável 'media' representa o resultado (f0) que queremos
        # encontrar e será atualizada durante a execução do código
        media = (x_esquerda + x_direita) / 2

        # Verificação da resposta final com a margem de erro de 10^-7
        if abs(RESULTADO - funcao_filtro(media, x0, G0, WA, sigma1, sigma2, sigma3)) < (10 ** (-7)):
            break

        # Verifica se o valor de H(f) é maior ao -3dB e altera o valor de x
        # que está abaixo do resultado
        elif funcao_filtro(media, x0, G0, WA, sigma1, sigma2, sigma3) > RESULTADO:
            x_direita = media

        # Verifica se o valor de H(f) é menor ao -3dB e altera o valor de x
        # que está acima do resultado
        elif funcao_filtro(media, x0, G0, WA, sigma1, sigma2, sigma3) <= RESULTADO:
            x_esquerda = media

    return media

def calcula_delta(x0Vector, sigma1Vector, sigma2Vector, sigma3Vector, G0Vector, WAVector, deltaVector):
    
    for x0Ind in range(len(x0Vector)):
        for sigma1Ind in range(len(sigma1Vector)):
            for sigma2Ind in range(len(sigma2Vector)):
                for sigma3Ind in range(len(sigma3Vector)):
                    for g0Ind in range(len(G0Vector)):
                        for WAInd in range(len(WAVector)):
                            x0 = x0Vector[x0Ind]
                            sigma1 = sigma1Vector[sigma1Ind]
                            sigma2 = sigma2Vector[sigma2Ind]
                            sigma3 = sigma3Vector[sigma3Ind]
                            G0 = G0Vector[g0Ind]
                            WA = WAVector[WAInd]
                        
                            esq = valor_x_esquerda(x0, G0, WA, sigma1, sigma2, sigma3)
                            dir = valor_x_direita(x0, G0, WA, sigma1, sigma2, sigma3)
                            deltaVector.append(float(dir - esq)/2)

def Pysr(dados_transpostos, deltaVector):

    # Configurações do Pysr ====================================================================== 
    model = PySRRegressor(
        model_selection="score",
        niterations=500,  # < Increase me for better results
        binary_operators=["+", "*", "-", "/"],
        progress=True,
        populations=50,
        population_size=100,
        maxsize=16,
        # ^ Mostra apenas as equações finais, sem mostrar o progresso
        unary_operators=[
            "sin",
            "cos",
            "exp",
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

    model.fit(dados_transpostos, deltaVector)
    print(model)

def funcao_predicao(x0, sigma1, sigma2, sigma3, G0, WA):
    return ((sigma2/(17.229462/sigma1)) * WA)

def plota_grafico(x0Vector, sigma1Vector, sigma2Vector, sigma3Vector, G0Vector, WAVector, deltaVector):

    valores_reais_delta = []
    valores_predicao = []

    if len(deltaVector) == 0:
        with open('deltaVector.txt', 'r') as arquivo:
            linha = arquivo.readline().strip()  # Lê a linha e remove espaços em branco
            valores_reais_delta = list(map(float, linha.split(',')))
            
    else:
        valores_reais_delta = deltaVector

    for x0Ind in range(len(x0Vector)):
        for sigma1Ind in range(len(sigma1Vector)):
            for sigma2Ind in range(len(sigma2Vector)):
                for sigma3Ind in range(len(sigma3Vector)):
                    for g0Ind in range(len(G0Vector)):
                        for WAInd in range(len(WAVector)):
                            x0 = x0Vector[x0Ind]
                            sigma1 = sigma1Vector[sigma1Ind]
                            sigma2 = sigma2Vector[sigma2Ind]
                            sigma3 = sigma3Vector[sigma3Ind]
                            G0 = G0Vector[g0Ind]
                            WA = WAVector[WAInd]

                            valores_predicao.append(funcao_predicao(x0, sigma1, sigma2, sigma3, G0, WA))

    indices = np.arange(len(valores_reais_delta))

    valores_ordenados = sorted(zip(valores_reais_delta, valores_predicao))
    valores_reais_ordenados = [v[0] for v in valores_ordenados]
    valores_predicao_ordenados = [v[1] for v in valores_ordenados]

    plt.scatter(np.arange(len(valores_reais_delta)), valores_reais_ordenados, color='blue', label='Valor Real do Delta')
    plt.scatter(np.arange(len(valores_predicao)), valores_predicao_ordenados, color='red', label='Predição pelo Pysr')

    plt.title('Comparação entre Valor Real do Delta e Predição pelo Pysr')
    plt.xlabel('Índice dos Pontos')
    plt.ylabel('Valor do Delta')

    plt.legend()
    plt.show()
    
    