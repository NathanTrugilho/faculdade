import os
from itertools import product
from funcoes import *

def main():

    x0Vector = [9, 10, 11]
    sigma1Vector = [0.8, 1.2, 1.6, 1.8]
    sigma2Vector = [2, 4, 6]
    sigma3Vector = [2, 2.5, 3]
    G0Vector = [1, 2, 5]
    WAVector = [0.5, 1, 1.5]
    dados = []
    deltaVector = [] #(dir - esq)/2

    while(True):
        # Pequena interface =================================================
        os.system('clear')
        print("+--------------------------------------------------------+")
        print("|                      Programinha                       |")
        print("+--------------------------------------------------------+")
        print("| 1. Calcular os valores de delta                        |")
        print("| 2. Usar a Regressão simbólica                          |")
        print("| 3. Plotar o gráfico para comparar delta com a predição |")
        print("| 4. Sair                                                |")
        print("+--------------------------------------------------------+")
        print("|-> Primeiro Calcular os valores de delta antes de usar a|")
        print("| regressão simbólica ou plotar o gráfico !!!            |")
        print("+--------------------------------------------------------+\n")

        caso = int(input("Selecione a opção (1, 2, 3, 4): "))


        # Switch case para o usuário escolher o que quer fazer =================================================

        if caso == 1:

            deltaVector = []
            print("-Calculando os valores de delta...")
            calcula_delta(x0Vector, sigma1Vector, sigma2Vector, sigma3Vector, G0Vector, WAVector, deltaVector)
            print("-Valores calculados!\n-Gravando num arquivo...")

            # Grava o deltaVector num arquivo de texto =====================================
            with open('deltaVector.txt', 'w') as arquivo:
                # Escreve o vetor como uma única linha, separando os elementos por vírgula
                arquivo.write(','.join(map(str, deltaVector)))
            print("-Gravação concluída!")
            pausa_tela()

        elif caso == 2:
            
            dados = []
            # Serve para criar o vetor de dados com as combinações de valores das variáveis 
            for combinacao in product(x0Vector, sigma1Vector, sigma2Vector, sigma3Vector, G0Vector, WAVector):
                dados.append(list(combinacao))
            
            # Lê os valores de delta do arquivo de texto se os valores de delta não estiverem na memória 
            if len(deltaVector) == 0:
                print("-Lendo os valores de delta do arquivo de texto...")
                # Lê o deltaVector do arquivo de texto ==========================================
                with open('deltaVector.txt', 'r') as arquivo:
                    linha = arquivo.readline().strip()  # Lê a linha e remove espaços em branco
                    deltaVector = list(map(float, linha.split(',')))
                print("-Leitura concluída")

            print("-Iniciando Pysr...")
            Pysr(dados, deltaVector) 
            print("-Pysr finalizado!")
            pausa_tela()

        elif caso == 3:
            plota_grafico(x0Vector, sigma1Vector, sigma2Vector, sigma3Vector, G0Vector, WAVector, deltaVector)

        elif caso == 4:
            # Encerra o programa
            print("Programa encerrado!\n")
            return 0
        
        else:
            print("Opção inválida")
            pausa_tela()

main()

# Coleta os dados do arquivo ===============================================
#with open('dados.txt', 'r') as arquivo:
#    linhas = arquivo.readlines()
#
#for linha in linhas:
    # Serve para tirar os '\n' e espaços
#    valores = linha.strip().split(',')
#    
#    x0.append(float(valores[0]))
#    sigma1.append(float(valores[1]))
#    sigma2.append(float(valores[2]))
#    sigma3.append(float(valores[3]))
#    G0.append(float(valores[4]))
#    WA.append(float(valores[4]))
#    delta.append(float(valores[5]))

#dados = [x0, sigma1, sigma2, sigma3, WA, G0]
#dados_transpostos = list(map(list, zip(*dados)))