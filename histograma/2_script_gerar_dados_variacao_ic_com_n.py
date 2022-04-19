########################################################################
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import bootstrap as bootstrap
import time as time

# Função auxiliar para rodar o bootstrap para várias amostras
def roda_bootstrap(func, dados, n_amostras, B):
    parametro_estimado = []
    erro_padrao_estimado = []
    ic_inf = []
    ic_sup = []
    
    ti_tudo = time.time()
    for n in n_amostras:
        ti = time.time()
        n_dados_amostrados = dados[0:n]
        parametro_estimado_n, erro_padrao_n, ic_inf_n, ic_sup_n = bootstrap.bootstrap(n_dados_amostrados, B, func)
        parametro_estimado.append(parametro_estimado_n)
        erro_padrao_estimado.append(erro_padrao_n)
        ic_inf.append(ic_inf_n)
        ic_sup.append(ic_sup_n)
        tf = time.time()
        print(f'\t\tTempo para {n} amostras: {tf - ti} seg')

    tf_tudo = time.time()
    print(f'\t\tTempo para todas as amostras: {tf_tudo - ti_tudo} seg')

    return [n_amostras, parametro_estimado, erro_padrao_estimado, ic_inf, ic_sup]

def salvar_arquivo(id_histograma, quantil, n_amostras, parametro_estimado, erro_padrao_estimado, ic_inf, ic_sup):
    nome_arquivo = f'resultados_quantis_por_hist_e_n\Hist_{id_histograma} quantil_{quantil}.csv'
    df = pd.DataFrame();
    df['n'] = n_amostras;
    df['parametro estimado'] = parametro_estimado
    df['erro padrao'] = erro_padrao_estimado
    df['ic_inf'] = ic_inf
    df['ic_sup'] = ic_sup
    df.to_csv(nome_arquivo, sep=';', index=None)
    
def get_func_quantil(quantil):
    return lambda dados : np.percentile(dados, quantil)


# Inicia carregando o arquivo de amostras que foi gerado usando
# o script 1_script_gerar_amostras_a_partir_histograma.py
print('Carregando arquivo de amostras (amostras.csv)')
amostras = pd.read_csv('amostras.csv', sep=';')

# Verifica a quantidade de experiências que iremos estudar
qtd_experimentos = amostras.shape[1]

# Define que quantis iremos analisar
quantis = np.array([90, 99, 99.9, 99.99, 99.999])

# Define as quantidade de amostras que usaremos em cada simulação dos quantis
n = [1000, 2000, 4000, 6000, 8000, 10000, 12000, 14000, 16000, 18000, 20000,
     22000, 24000, 26000, 28000, 30000, 32000, 34000, 36000, 38000, 40000,
     42000, 44000, 46000, 48000, 50000, 52000, 54000, 56000, 58000,
     60000, 62000, 64000, 66000, 68000, 70000, 72000, 74000,
     76000, 78000, 80000, 82000, 84000, 86000, 88000, 90000, 
     92000, 94000, 96000, 98000, 100000, 102000, 104000, 106000,
     108000, 110000, 112000, 114000, 116000, 118000, 120000, 122000, 
     124000, 126000, 128000, 256000, 512000, 1000000]

#n = [130000, 132000, 134000, 136000, 138000, 140000, 142000, 144000, 146000, 148000, 150000, 152000, 154000, 156000, 158000, 160000, 162000, 164000, 166000, 168000, 170000, 172000, 174000, 176000, 178000, 180000]

# Total de amostras bootstrap
B = 10000

ti = time.time()
for experimento in range(11, qtd_experimentos + 1):
    print(f'SIMULANDO HISTOGRAMA {experimento}')
    todos_dados_do_experimento = amostras[f'sample {experimento}']
    
    for quantil in quantis:
        print(f'\tSIMULANDO HISTOGRAMA {experimento} E QUANTIL {quantil}')
        n_amostras, parametro_estimado, erro_padrao_estimado, ic_inf, ic_sup = roda_bootstrap(get_func_quantil(quantil), todos_dados_do_experimento, n, B)
        salvar_arquivo(experimento, quantil, n_amostras, parametro_estimado, erro_padrao_estimado, ic_inf, ic_sup)

tf = time.time()

print(f'Duração total da simulação: {tf - ti} seg')