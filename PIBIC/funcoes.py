import os
from pysr import PySRRegressor
import matplotlib.pyplot as plt 
import numpy as np
import sympy as sp
import glob
HORA = 3600
INF = 1000000

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
        model_selection="best",
        niterations=INF,  #Botei um número bem alto para a condição de parada ser dada apenas pelo tempo
        binary_operators=["+", "*", "-", "/"],
        progress=True,
        # A condição de parada ====
        timeout_in_seconds=HORA/2,
        populations=50,
        population_size=100,
        unary_operators=[
            "sin",
            "cos",
            "exp",
            "log",
        ],
        warm_start=True,
        # ^ Faz com que o pysr rode a partir de um progresso já feito (a partir de um Hall_of_fame da vida)
        turbo=True,
        batching=True,
        loss="loss(prediction, target) = (prediction - target)^2",
        early_stop_condition="f(loss, complexity) = (loss < 0.00001) && (complexity < 10)",
        equation_file="equacoes.csv",
        # ^ Custom loss function (julia syntax)
    )

    model.fit(dados_transpostos, deltaVector)
    print(model)

def plota_grafico(x0Vector, sigma1Vector, sigma2Vector, sigma3Vector, G0Vector, WAVector, deltaVector):

    valores_reais_delta = []
    # Se por algum acaso o nome do arquivo de saída das equações não for definido
    '''diretorio_atual = "./"
    
    for entrada in os.scandir(diretorio_atual):
        if entrada.is_file() and entrada.name.endswith('.pkl'):
            break'''
    
    entrada = "equacoes.pkl"
    # Nome que eu defini nas configurações do pysr ^

    model = PySRRegressor.from_file(entrada)
    x0,x1,x2,x3,x4,x5 = sp.symbols('x0 x1 x2 x3 x4 x5')

    while True:
        valores_predicao = []
        while True:
            os.system('clear')
            print("+--------------------------------------------------------+")
            print("|                      Programinha                       |")
            print("+--------------------------------------------------------+")
            print("|-> Escolha a equação de predição gerada pelo PySR       |")
            print("|-> Deixe em branco para usar a equação escolhida automa-|")
            print("| ticamente pelo PySR com base na sua seleção de modelo! |")
            print("+--------------------------------------------------------+")
            print("| 0. Voltar                                              |")
            print("+--------------------------------------------------------+\n")

            string_numero_equacao = (input("Selecione a opção e pressione Enter(0 para voltar, 1, ..., quantidade de equações): "))

            if string_numero_equacao == "":
                equacao = PySRRegressor.sympy(model, None)
                break
            
            numero_equacao = int(string_numero_equacao)
            numero_equacao -= 1
            
            if numero_equacao == -1:
                return
            
            elif numero_equacao >= 0:
                equacao = PySRRegressor.sympy(model, numero_equacao)
                break

        if len(deltaVector) == 0:
            with open('deltaVector.txt', 'r') as arquivo:
                linha = arquivo.readline().strip()  # Lê a linha e remove espaços em branco
                valores_reais_delta = list(map(float, linha.split(',')))
                
        else:
            if len(valores_reais_delta) == 0:
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

                                valores_subs = {x0: x0, x1: sigma1, x2: sigma2, x3: sigma3, x4: G0, x5: WA}
                                valores_predicao.append(equacao.subs(valores_subs))

        # Ordena os valores em ordem crescente de Delta
        valores_ordenados = sorted(zip(valores_reais_delta, valores_predicao))
        valores_reais_ordenados = [v[0] for v in valores_ordenados]
        valores_predicao_ordenados = [v[1] for v in valores_ordenados]

        # Defino as propriedades dos pontos de indicação no gráfico
        plt.plot(np.arange(len(valores_reais_delta)), valores_reais_ordenados, color='blue', marker = 'o', linestyle='None', label='Valor Real do Delta')
        plt.plot(np.arange(len(valores_predicao)), valores_predicao_ordenados, color='red', marker='x', linestyle='None', label='Predição pelo PySR')
        
        # Mostro a equação no gráfico
        plt.text(0.5, 0.95, f'Equação: {equacao}', horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes, fontsize=12)

        plt.title('Comparação entre Valor Real do Delta e Predição pelo PySR')
        plt.xlabel('Índice dos Pontos')
        plt.ylabel('Valor do Delta')

        plt.legend()
        plt.show()
    
    