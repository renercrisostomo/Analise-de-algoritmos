import timeit
import random
import matplotlib.pyplot as plt

# Recursivo com Memoização: O(2^n)
def mochila_recursiva(itens, capacidade, n, memo):
    if (capacidade, n) in memo:
        return memo[(capacidade, n)]
    
    if n == 0 or capacidade == 0:
        return 0
    
    if itens[n-1][0] > capacidade:
        memo[(capacidade, n)] = mochila_recursiva(itens, capacidade, n-1, memo)
        return memo[(capacidade, n)]
    
    memo[(capacidade, n)] = max(
        itens[n-1][1] + mochila_recursiva(itens, capacidade - itens[n-1][0], n-1, memo),
        mochila_recursiva(itens, capacidade, n-1, memo)
    )
    return memo[(capacidade, n)]

# Iterativo: O(n * capacidade)
def mochila_iterativa(itens, capacidade, n):
    dp = [[0] * (capacidade+1) for _ in range(n+1)]
    
    for i in range(1, n+1):
        for j in range(1, capacidade+1):
            if itens[i-1][0] > j:
                dp[i][j] = dp[i-1][j]
            else:
                dp[i][j] = max(dp[i-1][j], dp[i-1][j-itens[i-1][0]] + itens[i-1][1])
    
    return dp[n][capacidade]

def tempos_peso_fixo(itens_max, peso_max, qtd_vezes_exec):
    # Variar número de itens, Peso da mochila fixo e Gerar itens (peso/valor) com valores aleatórios
    recursivo_tempos, iterativo_tempos = [], []
    for numItens in range(5, itens_max+1):
        print(f"Quantidade de itens: {numItens} de {itens_max}...")

        itens = []
        while not itens or sum([peso for peso, _ in itens]) < peso_max:
            for i in range(numItens):
                itens.append((random.randint(1, peso_max), random.randint(1, 100)))

        tempo_recursivo_media = timeit.timeit(lambda: mochila_recursiva(itens, peso_max, numItens, {}), number=qtd_vezes_exec)
        tempo_iterativo_media = timeit.timeit(lambda: mochila_iterativa(itens, peso_max, numItens), number=qtd_vezes_exec)

        recursivo_tempos.append(tempo_recursivo_media)
        iterativo_tempos.append(tempo_iterativo_media)

        print(f"Quantidade de itens {numItens} concluída.")
        
    print("Todas as iterações foram concluídas.")

    return recursivo_tempos, iterativo_tempos

def tempos_itens_fixo(itens_max, peso_max, qtd_vezes_exec):
    # Variar número de Peso da mochila, Quantidade de itens fixo e Gerar itens (peso/valor) com valores aleatórios
    recursivo_tempos, iterativo_tempos = [], []
    for pesoMax in range(5, peso_max+1):
        print(f"Peso máximo da mochila: {pesoMax} de {peso_max}...")

        itens = []
        while not itens or sum([peso for peso, _ in itens]) < pesoMax:
            for i in range(itens_max):
                itens.append((random.randint(1, pesoMax), random.randint(1, 100)))

        tempo_recursivo_media = timeit.timeit(lambda: mochila_recursiva(itens, pesoMax, itens_max, {}), number=qtd_vezes_exec)
        tempo_iterativo_media = timeit.timeit(lambda: mochila_iterativa(itens, pesoMax, itens_max), number=qtd_vezes_exec)

        recursivo_tempos.append(tempo_recursivo_media)
        iterativo_tempos.append(tempo_iterativo_media)

        print(f"Peso máximo da mochila {pesoMax} concluído.")

    print("Todas as iterações foram concluídas.")

    return recursivo_tempos, iterativo_tempos


def main():

    PESO_MAX = 50
    QTD_VEZES_EXEC = 100
    ITENS_MAX = 50

    recursivo_tempos_peso_fixo, iterativo_tempos_peso_fixo = tempos_peso_fixo(ITENS_MAX, PESO_MAX, QTD_VEZES_EXEC)
    recursivo_tempos_qtd_itens_fixo, iterativo_tempos_qtd_itens_fixo = tempos_itens_fixo(ITENS_MAX, PESO_MAX, QTD_VEZES_EXEC)

    # Plotar os resultados
    plt.figure(figsize=(10, 5))

    # Gráfico 1 - Peso Máximo Fixo
    plt.subplot(1, 2, 1)
    plt.plot(range(5, 51), recursivo_tempos_peso_fixo, label='Recursivo - Peso Máximo Fixo')
    plt.plot(range(5, 51), iterativo_tempos_peso_fixo, label='Iterativo - Peso Máximo Fixo')
    plt.xlabel('Quantidade de Itens')
    plt.ylabel('Tempo (segundos)')
    plt.legend()

    # Gráfico 2 - Itens Fixos
    plt.subplot(1, 2, 2)
    plt.plot(range(5, PESO_MAX+1), recursivo_tempos_qtd_itens_fixo, label='Recursivo - Itens Fixos')
    plt.plot(range(5, PESO_MAX+1), iterativo_tempos_qtd_itens_fixo, label='Iterativo - Itens Fixos')
    plt.xlabel('Peso Máximo da Mochila')
    plt.ylabel('Tempo (segundos)')
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()