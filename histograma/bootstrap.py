# Roda bootstrap em uma amostra
# Entradas:
#   - sample: lista de amostras
#   - B: número de amostras de bootstrap
#   - func: função que será aplicada para extrair a estatística desejada
import numpy as np
import sklearn as sk
import time

def bootstrap(sample, B, func):
    bootstraped_value = np.zeros(B)

    for i in range(0, B):
        # Faz a reamostragem
        resampled = np.random.choice(sample, size=sample.shape, replace=True)
        # Aplica a função desejada
        bootstraped_value[i] = func(resampled)

    # Retorna o array bootstrap, o valor esperado, o intervalo de confiança e o erro padrão
    intervalo_confianca = np.percentile(bootstraped_value, [2.5,97.5])
    return [np.mean(bootstraped_value), 
            np.std(bootstraped_value),
            intervalo_confianca[0],
            intervalo_confianca[1]]

# Essa versão aqui, apesar de usar as funções do numpy, é mais
# lenta que o for loop. Provavelmente devido a quantidade de
# registros gerados e alocados em memória...
def bootstrap_temp(sample, n_resamples, func):
    bootstraped_value = np.zeros(n_resamples)

    # Aplica a reamostragem em sample.
    # O resultado é uma matriz de tamanho (qtd de amostras, n_resamples)
    resampled = np.random.choice(sample, size=(len(sample), n_resamples), replace=True)
    # Calcula a função que extrai a estatística (func) para cada coluna
    # O resultado é um vetor de tamanho (n_resamples)
    bootstraped_value = np.apply_along_axis(func, 0, resampled)
    # Retorna o array bootstrap, o valor esperado, o intervalo de confiança e o erro padrão
    return [bootstraped_value,
            np.mean(bootstraped_value), 
            np.percentile(bootstraped_value, [2.5,97.5]),
            np.std(bootstraped_value)]




def teste_bootstrap():
    np.random.seed(42)
    n = 100000
    B = 10000
    # Gera uma gausiana
    media = 1
    desvio_padrao = 1
    dadosTeste = np.random.normal(loc=media, scale=desvio_padrao, size=n)

    print('Simulando dados de uma gausiana')
    startTime = time.time()
    resultado = bootstrap(dadosTeste, B, np.mean)
    endTime = time.time()
    print(f'Tempo transcorrido na simulação: {endTime - startTime}')
    print('Resultado (média, erro padrão, intervalo de confiança):')
    print(resultado, '\n')
    
    media_estimada = resultado[0]
    erro_padrao_estimado = resultado[1]
    ic_estimado = resultado[2:4]
    
    media_dados = np.mean(dadosTeste)
    desvio_padrao_dados = np.std(dadosTeste)
    ic_dados_teorico = [media_dados - 1.96*desvio_padrao_dados/n**0.5, media_dados + 1.96*desvio_padrao_dados/n**0.5]
    erro_padrao_teorico = desvio_padrao/n**0.5
    
    print(f'Erro padrão teórico: {erro_padrao_teorico}')
    print(f'Erro padrão calculado: {erro_padrao_estimado}\n')
    
    print(f'Média estimada: {media_estimada}')
    print(f'Média dos dados: {media_dados}\n')
    
    print(f'Intervalo de confiança estimado: {ic_estimado}')
    print(f'Intervalo de confiança teórico: {ic_dados_teorico}')
    
# teste_bootstrap()