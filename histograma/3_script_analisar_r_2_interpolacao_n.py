import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from scipy.stats import linregress

quantis = np.array([90, 99, 99.9, 99.99, 99.999])

for quantil in quantis:
    arquivoPdf = PdfPages(f'quantil_{quantil}_estimado_e_r2.pdf')
    
    for hist in range(1, 71):
        amostras = pd.read_csv(f'resultados_quantis_por_hist_e_n\Hist_{hist} quantil_{quantil}.csv', sep=';')
        
        # Seleciona só as amostras com potência de 2
        amostras = amostras[amostras.n.isin([1000, 2000, 4000, 8000, 16000, 32000, 64000, 128000, 256000, 512000, 1000000])]
        amostras.reset_index(drop=True, inplace=True)
        
        um_sobre_raiz_n = 1/np.sqrt(amostras['n'])
        intervalo_confianca = amostras['ic_sup'] - amostras['ic_inf']
        
        # Os índices das csv vão de 0 (n=1000) até 130 (n=1M).
        # Vamos analisar de 0 (n=1000) até 128 (n=256k)
        total_linhas = len(amostras)
        plot_n = np.zeros((total_linhas,1))
        plot_ic_inf = np.zeros((total_linhas,1))
        plot_parametro = np.zeros((total_linhas,1))
        plot_ic_sup = np.zeros((total_linhas,1))
        plot_r_2 = np.zeros((total_linhas,1))
        for i in range (0, total_linhas):
            amostras_a_partir_de_i = amostras[i:total_linhas]
            n = amostras_a_partir_de_i['n']
            um_sobre_raiz_n = 1/np.sqrt(n)
            intervalo_confianca = amostras_a_partir_de_i['ic_sup'] - amostras_a_partir_de_i['ic_inf']
            slope, intercept, r_2, _, _ = linregress(um_sobre_raiz_n, intervalo_confianca)
            print(f'{n[i]}\t{r_2}')
            plot_n[i] = n[i]
            # Para plotar o r2
            plot_r_2[i] = r_2
            # Para plotar o parâmetro (quantil)
            plot_parametro[i] = amostras_a_partir_de_i[0:1]['parametro estimado']
            plot_ic_inf[i] = amostras_a_partir_de_i[0:1]['ic_inf']
            plot_ic_sup[i] = amostras_a_partir_de_i[0:1]['ic_sup']
        
        fig = plt.figure()

        plt.subplot(211)
        plt.plot(plot_n[0:total_linhas-2], plot_ic_inf[0:total_linhas-2], 'r')
        plt.plot(plot_n[0:total_linhas-2], plot_parametro[0:total_linhas-2], 'b')
        plt.plot(plot_n[0:total_linhas-2], plot_ic_sup[0:total_linhas-2], 'r')
        # plt.xticks(range(10000, 260000, 10000))
        plt.title(f'{hist} {quantil} (estimado, r2)')
        plt.grid(linestyle='-.', linewidth=1)

        plt.subplot(212)
        plt.plot(plot_n[0:total_linhas-2], plot_r_2[0:total_linhas-2])
        plt.grid(linestyle='-.', linewidth=1)

        arquivoPdf.savefig(fig)
        
    arquivoPdf.close()