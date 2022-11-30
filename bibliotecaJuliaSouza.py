import random
import string
from random import randint

def menu():
    print('-'*20)
    print('\033[1;95mBem vindo ao Gemas!\033[m')
    print('-' * 20)
    print('Forme uma \033[4;34mcadeia de 3 ou mais letras(gemas) iguais\033[m! Mas só pode \033[1;32mvertical\033[m ou \033[1;36mhorizontal\033[m e com uma casa de distância!\n')

def fornecer_dados(): #recebe dados para construção da matriz
    linha = int(input('Por favor, forneça o número de linhas do tabuleiro [3-10]: '))
    while (linha < 3) or (linha > 10):
        linha = int(input('Valor inválido! Forneça o número de linhas do tabuleiro [3-10]: '))

    coluna = int(input('Agora, forneça o número de colunas do tabuleiro [3-10]: '))
    while (coluna < 3) or (coluna > 10):  # o tabuleiro só pode ser de 10x10.
        coluna = int(input('Valor inválido! Forneça o número de colunas do tabuleiro [3-10]: '))
    #variação de gemas
    gema = int(input('Quantas variações de gema deseja? '))
    while gema < 3 or gema > 26: #if para mostrar duas frases diferentes de acordo com o erro.
        if gema < 3:
            gema = int(input('Escolha pelo menos 3 variações: '))
        elif gema > 26:
            gema = int(input('O máximo de variações é 26: '))
    return linha, coluna, gema

def criar_matriz_original(linha, coluna, gema):
    #Dicutida na sessão 3 do dia 23/09/2021 - gera letras aleatórias para a matriz
    matriz = [[string.ascii_uppercase[randint(0, gema - 1)] for c in range(coluna)] for l in range(linha)]
    return matriz

def printar_matriz(matriz, linha, coluna):
    for l in range(linha):  # 'l' como iteração das linhas
        for c in range(coluna):  # 'c' como iteração das colunas
            print(matriz[l][c], end=' ')
        print('')
    print('')

def validar_horizontais_prontas(matriz, linha, coluna): #função contida na "analisar_gemas"
    #Discutida na sessão 3 do dia 23/09/2021 - transforma as cadeias horizontais válidas em letras minúsculas
    for l in range(linha):  #'l' como iteração das linhas
        contador = 1  # contador para verificar se existem gemas válidas para serem quebradas
        for c in range(coluna - 1):  # 'c' como iteração das colunas
            if matriz[l][c].lower() == (matriz[l][c + 1]).lower():
                contador += 1
            else:
                contador = 1
            if contador >= 3:
                k = c + 1
                while (k > c + 1 - contador) and matriz[l][k].isupper():
                    matriz[l][k] = matriz[l][k].lower()
                    k -= 1
    return matriz

def validar_verticais_prontas(matriz, linha, coluna): #função contida na "analisar_gemas"
    #Discutida na sessão 3 do dia 23/09/2021 - transforma as cadeias verticais válidas em letras minúsculas
    for c in range(coluna):  # 'c' como iteração das colunas
        contador = 1
        for l in range(linha - 1):  # 'l' como iteração das linhas
            if matriz[l][c].lower() == matriz[l + 1][c].lower():
                contador += 1
            else:
                contador = 1
            if contador >= 3:
                p = l + 1
                while (p > l + 1 - contador):
                    matriz[p][c] = matriz[p][c].lower()
                    p -= 1
    return matriz

def analisar_gemas(matriz,linha,coluna): #função para analisar combinações de gemas, horizontais e verticais
    retorno = validar_verticais_prontas(matriz, linha, coluna)
    retorno = validar_horizontais_prontas(matriz, linha, coluna)
    return retorno

def quebrar_gemas(matriz, linha, coluna):
    for l in range(linha):
        for c in range(coluna):
            if matriz[l][c].islower(): #substitui a letra minúscula por 0
                matriz[l][c] = 0
    return matriz

def descer_gemas(matriz,linha,coluna):
    #Discutida na sessão 4 do dia 30/09/2021 - "gravidade" para as gemas
    for d in range(linha):
        for i in range(linha-1, 0, -1):#linha
            for j in range(coluna-1, -1, -1):#coluna
                if matriz[i][j] == 0:
                    matriz[i][j], matriz[i-1][j] = matriz[i-1][j], matriz[i][j]
    return matriz

def gerar_novas_gemas(matriz, gema):
    #Discutida na sessão 4 do dia 30/09/2021 - função simples, apenas substitui os 0 por novas letras aleatórias
    cont = 0
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            if matriz[i][j] == 0:
                cont += 1
                matriz[i][j] = string.ascii_uppercase[randint(0, gema - 1)]

    return matriz, cont  # se o contador continuar zero, a matriz nao precisa ser ciclada e já pode deixar o usuário jogar.

def pontuar(matriz, pontuacao1):
    #Função simples porém também foi discutida na sessão 4 - 30/09/2021
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            if matriz[i][j] == 0:
                pontuacao1 += 1
    return pontuacao1

def ciclagem(matriz, linha, coluna, gemas, pontos):
    #Todas as funções que alteram a matriz de alguma forma em apenas uma! - cicla a matriz até não ter jogadas prontas
    matriz_retorno = analisar_gemas(matriz, linha, coluna)
    matriz_retorno = quebrar_gemas(matriz_retorno, linha, coluna)
    pontos_retorno = pontuar(matriz_retorno, pontos)
    matriz_retorno = descer_gemas(matriz_retorno, linha, coluna)
    matriz_retorno, cont = gerar_novas_gemas(matriz_retorno, gemas)
    return matriz_retorno, cont, pontos_retorno

def fornecer_movimento(matriz, falhas):
    #Ideias discutidas na 5 sessão - 07/10/2021
    print('Faça seu movimento:')
    mexer_l = int(input('Linha: '))
    mexer_c = int(input('Coluna: '))
    print('Trocar para: ')
    mexer_l1 = int(input('Linha: '))
    mexer_c1 = int(input('Coluna: '))
    valido = True #variavel booleana para identificar se o que foi fornecido é válido ou não.
    if (abs(mexer_l - mexer_l1) + abs(mexer_c - mexer_c1)) != 1: #analisa se o movimento é de apenas uma casa de difereça
        valido = False
    elif(mexer_l > len(matriz)) or (mexer_c > len(matriz[0])) or (mexer_l < 0) or (mexer_c < 0) or \
            (mexer_l1 > len(matriz)) or (mexer_c1 > len(matriz[0])) or (mexer_l1 < 0) or (mexer_c1 < 0):
        #analisa se o movimento fornecido está no range da matriz ou é um número negativo.
        valido = False
    while not valido: #valido = False
        falhas += 1 #variavel acumuladora para contabilizar quantos erros o usuário teve
        print('Movimento inválido, tente novamente.')
        mexer_l = int(input('Linha: '))
        mexer_c = int(input('Coluna: '))
        print('Trocar para: ')
        mexer_l1 = int(input('Linha: '))
        mexer_c1 = int(input('Coluna: '))
        if (mexer_l > len(matriz)) or (mexer_c > len(matriz[0])) or (mexer_l < 0) or (mexer_c < 0) or \
                (mexer_l1 > len(matriz)) or (mexer_c1 > len(matriz[0])) or (mexer_l1 < 0) or (mexer_c1 < 0):
            valido = False
        elif (abs(mexer_l - mexer_l1) + abs(mexer_c - mexer_c1)) != 1:
            valido = False
        else:
            valido = True

    return mexer_l, mexer_c, mexer_l1, mexer_c1, falhas

def analise_de_quebra(matriz):
    quebrou = False
    #analisa horizontal
    for l in range(len(matriz)):
        contador = 1
        for c in range(len(matriz[0])-1):
            if matriz[l][c].lower() == (matriz[l][c + 1]).lower():
                contador += 1
            else:
                contador = 1
            if contador >= 3:
                quebrou = True
    #analisa vertical
    for l in range(len(matriz[0])): #analisando coluna
        contador = 1
        for c in range(len(matriz)-1):  #analisando linha
            if matriz[c][l].lower() == (matriz[c+1][l]).lower():
                contador += 1
            else:
                contador = 1
            if contador >= 3:
                quebrou = True
    return quebrou

def mexer_gemas(matriz, mexer_l, mexer_c, mexer_l1, mexer_c1, falhas):
    #essa função troca a gema de lugar e chama a função de analise de quebra
    matriz[mexer_l][mexer_c], matriz[mexer_l1][mexer_c1] = matriz[mexer_l1][mexer_c1], matriz[mexer_l][mexer_c]
    validacao = analise_de_quebra(matriz)
    if validacao: #se quebrar, a movimentação acontece
        matriz[mexer_l1][mexer_c1], matriz[mexer_l][mexer_c]
    else:
        print('Movimento inválido.') #se não, o movimento é inválido e a gema retorna ao lugar de inicio
        falhas += 1
        matriz[mexer_l1][mexer_c1], matriz[mexer_l][mexer_c] = matriz[mexer_l][mexer_c], matriz[mexer_l1][mexer_c1]

    return matriz, falhas

def dicas(matriz, linha, coluna):
    #também faz uso da analise de quebra e é baseada nas funções de validar horizontais e verticais.
    dicas = []
    for i in range(linha):
        for j in range(coluna - 1):
            matriz[i][j], matriz[i][j + 1] = matriz[i][j + 1], matriz[i][j] #verifica se uma esse movimento vai gerar uma quebra de cadeia
            validacao = analise_de_quebra(matriz)
            if validacao:
                dicas.append((f'{i}x{j} com {i}x{j+1}')) #adiciona o indice encontrado a uma lista de dicas
            matriz[i][j + 1], matriz[i][j] = matriz[i][j], matriz[i][j + 1]
    print(random.choice(dicas)) #escolha aleatória de um dos elementos das dicas

def encerrar(matriz, linha, coluna):
    #segue a mesma lógica das funções de analisar_gemas e também utiliza a analise_de_quebra
    #retorna um True caso ainda tenham jogadas a ser feitas
    encerramento = False
    for i in range(linha):
        for j in range(coluna - 1):
            matriz[i][j], matriz[i][j + 1] = matriz[i][j + 1], matriz[i][j] #faz um movimento
            validacao = analise_de_quebra(matriz) #analisa se quebrou
            if validacao:
                encerramento = True
            matriz[i][j + 1], matriz[i][j] = matriz[i][j], matriz[i][j + 1] #retorna a gema pra o local original
    for i in range(coluna):
        for j in range(linha - 1):
            matriz[j][i], matriz[j + 1][i] = matriz[j + 1][i], matriz[j][i]
            validacao = analise_de_quebra(matriz)
            if validacao:
                encerramento = True
            matriz[j + 1][i], matriz[j][i] = matriz[j][i], matriz[j + 1][i]

    return encerramento