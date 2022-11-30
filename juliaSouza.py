from bibliotecaJuliaSouza import *
import sys
'''
Autor: Júlia Carneiro Gonçalves de Souza
Componente Curricular: MI - Algoritmos
Concluido em: 14/10/2021
Declaro que este código foi elaborado por mim de forma individual e não contém nenhum
trecho de código de outro colega ou de outro autor, tais como provindos de livros e
apostilas, e páginas ou documentos eletrônicos da Internet. Qualquer trecho de código
de outra autoria que não a minha está destacado com uma citação para o autor e a fonte
do código, e estou ciente que estes trechos não serão considerados para fins de avaliação.
'''
pontuacao_inicial = 0 #pontuação inicial do jogador (0), para ser fornecida como parâmetro na funçõa pontuar
contador_gemas = 0  #serve para acumular quantos zeros foram formados na matriz - faz com que o programa saiba quando ainda tem jogadas prontas(ciclagem)
falha = 0 #acumula quantidade de falhas do jogador para personalizar a dica - é resetada quando o jogador atinge 3 falhas

menu() #função para tentar deixar o inicio menos feio :D
linhas, colunas, gemas = fornecer_dados() #validação do tamanho do tabuleiro e variação de gemas

#criando a matriz original:
matriz_original = criar_matriz_original(linhas, colunas, gemas)

#ciclando a matriz até não ter gemas prontas.
matriz_original, contador_gemas1, pontuacao = ciclagem(matriz_original, linhas, colunas, gemas, pontuacao_inicial)
while contador_gemas1 != 0:  #contador_gemas1 serve pra armazenar o return do contador da função gerar_novas_gemas e saber se ainda tem cadeias ja quebradas.
    matriz_original, contador_gemas1, pontuacao = ciclagem(matriz_original, linhas, colunas, gemas, pontuacao_inicial)
print(f'Pontuação: {pontuacao}')
printar_matriz(matriz_original, linhas, colunas)


encerrar_programa = encerrar(matriz_original, linhas, colunas) #caso não tenha mais movimentos o jogo encerra
while encerrar_programa:
    #movimento:
    mexer_linha, mexer_coluna, mexer_linha1, mexer_coluna1, falha = fornecer_movimento(matriz_original, falha)
    matriz_original, falha = mexer_gemas(matriz_original, mexer_linha, mexer_coluna, mexer_linha1, mexer_coluna1, falha)

    #ciclagem pós-movimento.
    matriz_original, contador_gemas1, pontuacao = ciclagem(matriz_original, linhas, colunas, gemas, pontuacao)
    while contador_gemas1 != 0:  #contador_gemas1 serve pra armazenar o return do contador da função gerar_novas_gemas.
        matriz_original, contador_gemas1, pontuacao = ciclagem(matriz_original, linhas, colunas, gemas, pontuacao)
    print(f'Pontuação: {pontuacao}')
    printar_matriz(matriz_original, linhas, colunas)

    #pergunta - deseja continuar a jogar?
    continuar = (input('Quer continuar a jogar? ')).strip().upper()[0]
    while (continuar != 'S') and (continuar != 'N'):  # validação de resposta
        continuar = (input('Quer continuar a jogar? [S/N] ')).strip().upper()[0]
    if (continuar == 'N'):
        print('\033[1;31mGame Over!\033[1;31m')
        sys.exit()

    #solicitar dica
    if falha >= 3 and pontuacao >= 1: #só vai ser possível pedir dicas depois de 2 erros
        falha = 0 #serve para resetar as falhas após os 2 erros.
        pedir_dica = (input('Precisa de dica? (Custa 1 ponto) ')).strip().upper()[0]
        while (pedir_dica != 'S') and (pedir_dica != 'N'): #validação de resposta
            pedir_dica = (input('Digite uma opção válida! [S/N] ')).strip().upper()[0]
        if (pedir_dica == 'S'): #só é possível pedir dica se tiver uma pontuação > ou = a 1.
            dicas(matriz_original, linhas, colunas)
            pontuacao -= 1
            print(f'\033[1;31mPontuação: {pontuacao}\033[m')
    if falha >= 4 and pontuacao < 1:
        falha = 0
        print('Vou tentar te ajudar! Mas ainda custa 1 ponto :p')
        dicas(matriz_original, linhas, colunas)
        pontuacao -= 1
        print(f'\033[1;31mPontuação: {pontuacao}\033[m')

else:
    print('Não existem combinações possíveis.\nGame Over!')

#Para complementar o vídeo-relatório:
"Possíveis erros no código:" \
"Uma pequena falha em um caso de teste específico na movimentação do usuário (quando digita-se um indice correto e um errado, acontece esse bug AS VEZES)" \
"Digitação de letras em variáveis tipo int - ValueError: invalid literal for int() with base 10: ''" \
"Digitação sem nenhum caracter - ValueError: invalid literal for int() with base 10: '' " \

