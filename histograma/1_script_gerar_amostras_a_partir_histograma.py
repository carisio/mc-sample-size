########################################################################
# Esse script gera amostras a partir de um arquivo csv contendo
# dados de histogramas
#
# Os histogramas foram criados com o utilitário GerarHistograma
# e salvos no Excel (Histogramas - dados originais e gráfico.xlsx).
#
# O xlsx contém a relação entre a quantidade de amostras em cada bin.
# A partir dele, exportei para o arquivo histogramas.csv, que é a fonte usada
# para gerar os samples.
#
# Os samples são gerados considerando cada histograma e considerando
# uma distribuição uniforme em cada bin. O resultado é salvo em um 
# csv que não é salvo no git devido ao tamanho, mas que é rapidamente gerado
# executando esse script
########################################################################
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#####################################################
# Função gera amostras a partir de um histograma
# 
# As entradas bins_i e bins_f representamo o valor de início
# e fim de cada bin. A entra histograma contém os dados do histograma
#
# A leitura das entradas é o seguinte: todas as três entradas são
# listas de mesmo tamanho (n_bins). Para um determinando bin b,
# sabemos que deverão ser geradas histograma[b] amostras
# no intervalo bins_i[b] até bins_f[b]
#####################################################
def gerar_amostras(bins_i, bins_f, histograma):
    n_bins = len(histograma)
    # Gera as amostras para o histograma
    amostras = []
    for bin in range(n_bins):
        amostras.extend(np.random.uniform(bins_i[bin], bins_f[bin], size=histograma[bin]))
    # Embaralha os dados
    np.random.shuffle(amostras)
    
    return amostras

# Função auxiliar para plotar histograma gerado
def plota_histograma(sample_df, id_histograma):
    # Plota um histograma com os dados gerados
    plt.hist(sample_df[f'sample {id_histograma}'], density=False, bins=bins_center)
    plt.ylabel('Probability')
    plt.xlabel('Data');


# Semente = 42 para assegurar que os dados gerados sempre serão iguais
# independente de quando roda o script. Uso random tanto para gerar os 
# dados quanto 
np.random.seed(42)

# Carrega a lista de todos os histogramas
hist_df = pd.read_csv('histogramas.csv', sep=';')

# A coluna 0 contém o centro dos bins. Supõe-se que os bins
# estão igualmente espaçados
bins_center = hist_df.iloc[:, 0].to_numpy()
largura_bin = bins_center[1] - bins_center[0]
bins_i = bins_center - largura_bin/2
bins_f = bins_center + largura_bin/2

# Quantidade de colunas do data_frame de histogramas
# A coluna 0 é o centro dos bins. A coluna 1 a qtd_colunas_hist_df 
# representam os histogramas
qtd_colunas_hist_df = hist_df.shape[1]

# Gera amostras para cada histograma
sample_df = pd.DataFrame()
for idx_histograma in range(1, qtd_colunas_hist_df):
    print(f'Iniciando cálculo para {idx_histograma}')
    # Obtém os dados do histograma
    histograma = hist_df.iloc[:, idx_histograma].to_numpy()
    
    # Gera a amostra e salva no data frame
    sample_df[f'sample {idx_histograma}'] = gerar_amostras(bins_i, bins_f, histograma)

print(sample_df)

# Salva o csv em um arquivo para ser usado depois
sample_df.to_csv('amostras.csv', sep=';', index=None)