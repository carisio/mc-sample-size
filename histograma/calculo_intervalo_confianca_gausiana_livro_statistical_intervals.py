# Teste de cálculo do intervalo de confiança de acordo com a fórmula da página
# 83 do livro "Statistical Intervals"

import numpy as np
import scipy.stats
import bootstrap as bootstrap

def get_func_quantil(quantil):
    return lambda dados : np.percentile(dados, quantil)

# Dados de entrada: 
# Quantidade de amostras aleatórias
n = 10000
# Quantil estudado
q = 0.9
# Valores de média e desvio padrão da amostra
media_teorica = 50
desvio_padrao_teorico = 10
np.random.seed(42)
medidas = np.random.normal(media_teorica, desvio_padrao_teorico, n)

# Para refazer o exemplo da página 84, descomente as três linhas abaixo
# medidas = np.array([50.3, 48.3, 49.6, 50.4, 51.9]) 
# n = len(medidas)
# q = 0.9


print('Calcula intervalo de confiança')
##########################################################################
# Cálculo de acordo com o livro (obs.: no livro tem um sinal trocado)
media = np.mean(medidas)
s = np.std(medidas, ddof=1)
delta = -(n**0.5) * scipy.stats.norm.ppf(q)
ic_inf = media - scipy.stats.nct.ppf(q=0.975, df=n-1, nc=delta) * s / (n**0.5)
ic_sup = media - scipy.stats.nct.ppf(q=0.025, df=n-1, nc=delta) * s / (n**0.5)
print(f'Livro: {ic_inf} até {ic_sup}')


##########################################################################
# O mesmo cálculo feito com bootstrap
B = 10000
parametro_estimado, erro_padrao_estimado, ic_inf, ic_sup = bootstrap.bootstrap(medidas, B, get_func_quantil(q*100))
print(f'Boostrap: {ic_inf} até {ic_sup}')