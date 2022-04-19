import scipy.stats
import numpy as np
import math
import bootstrap as bootstrap

# O cálculo de r e s considera o livro
# Confome página 144 do livro "Practical nonparametric statistics"
def calcula_r_s(n, quantil, confidence_interval):
    alpha = 1 - confidence_interval
    r = math.ceil(n*quantil + scipy.stats.norm.ppf(alpha/2) * math.sqrt(n*quantil*(1-quantil)))
    s = math.ceil(n*quantil + scipy.stats.norm.ppf(1 - alpha/2) * math.sqrt(n*quantil*(1-quantil)))
    return r, s

def encontra_min_n(quantil, confidence_interval):
    for n in range(50, 10000000):
        r, s = calcula_r_s(n, quantil, confidence_interval)
        
        idx_quantil = n*quantil
        
        if r > 1 and r < idx_quantil and s > idx_quantil and s < n:
            return n, r, s
        
    return -1, -1, -1

def print_tabela():
    confidence_intervals = np.array([0.90, 0.95, 0.99, 0.999])
    quantiles = np.array([0.9, 0.95, 0.99, 0.999, 0.9999, 0.99999])
    
    for c in confidence_intervals:
        print(f'Confidence interval: {c}')
        for q in quantiles:
            n, r, s = encontra_min_n(q, c)
            print(f'Quantile {q}. Min sample size: {n}. Index r and s: {r}, {s}')
        print('-------------------------------------')

def calcula_n(p, confidence_interval):
    alpha = 1 - confidence_interval
    z = scipy.stats.norm.ppf(1 - alpha/2)
    a = p*(1-p)
    
    aux = (a * (a*z*z + 4 - 4*p))**0.5
    n1 = math.ceil( (-2*p + 2 + a*z*z + z*aux) / (2 * (-2*p + p*p + 1)) )
    n2 = math.ceil( (-2*p + 2 + a*z*z - z*aux) / (2 * (-2*p + p*p + 1)) )
    
    n = n1 if n1 > n2 else n2
    r, s = calcula_r_s(n, p, confidence_interval)
    return n, r, s
    

def print_comparacao():
    confidence_intervals = np.array([0.90, 0.95, 0.99, 0.999])
    quantiles = np.array([0.9, 0.95, 0.99, 0.999, 0.9999, 0.99999])
    
    for c in confidence_intervals:
        print(f'Confidence interval: {c}')
        for q in quantiles:
            n, r, s = encontra_min_n(q, c)
            
            n1, r1, s1 = calcula_n(q, c)
            
            
            
            print(f'Quantile {q}. Min sample size: {n}, {n1}.')
        print('-------------------------------------')    


def print_tabela_artigo():
    confidence_intervals = np.array([0.90, 0.95, 0.99, 0.999])
    quantiles = np.array([0.9, 0.95, 0.99, 0.999, 0.9999, 0.99999])
    
    for q in quantiles:    
        print(f'Quantile: {q}')
        for c in confidence_intervals:           
            n1, r1, s1 = calcula_n(q, c)
            print(f' {c}. Min sample size: {n1}.')
        print('-------------------------------------')    