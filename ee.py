#!/usr/bin/python3

import math
import matplotlib.pyplot as plt
import random
import sys

#random.seed(a=1) # para ficar previsiver

def ackley(X):
    "X eh um vetor de n posicoes, da forma [objeto,passo]"
    n = len(X)

    a = 20
    b = 0.2
    c = 2 * math.pi

    sum1 = 0
    sum2 = 0
    try:
        for (x,s) in X:
            sum1 += x**2
            sum2 += math.cos(c * x)

        result = (a + math.e) - (a * math.exp((-b) * math.sqrt((1/n) * sum1)) + math.exp((1/n) * sum2))
    except Exception as e:
        print(e)
        print(X)

    return result

def pop_init(m, n):
    "Inicia populacao com m individuos de n cromossomos"
    pop = []
    
    for i in range(m):
        individuo = [ [random.uniform(-15,15),1] for i in range(n) ]
        pop.append(individuo)

    return pop

def mutaciona_nao_corre(individuo):
    "Mutacao nao correlacionada de n desvios padroes"
    n = len(individuo)
    novo_individuo = []
    # taxa de aprendizagem global
    tau = 1/math.sqrt(2*n)
    # guassiana global
    ggauss = random.gauss(0,1)

    tg = tau * ggauss
    
    # taxa de aprendizagem de ajuste fino
    tau_fino = 1/math.sqrt(2*math.sqrt(n))
    

    # testar valores que ajudam
    # nenhum valor de epsilon ajuda neste caso... (eu acho)
    #eps =  1e-18
    
    for (var_objeto, passo_mut) in individuo:
        while True:
            #rg = random.gauss(0,1)
            passo_mutn = passo_mut * math.exp(tg + tau_fino * random.gauss(0,1))

            # if passo_mutn < eps:
            #     # evita passos de mutacao muito pequenos
            #     passo_mutn = eps

            var_objeton = var_objeto + passo_mutn * random.gauss(0,1)

            if abs(var_objeton) <= 15:
                break

        novo_individuo.append([var_objeton, passo_mutn])

    return novo_individuo
        
        
def recomb_pais_fixos(p1, p2):
    "Recombina dois pais e gera um filho"

    individuo_recomb = []

    for i in range(len(p1)): # ou len(p2), tanto faz
        # ponto local intermediario para passo de mutacao, que eh um parametro
        passo_mut = (p1[i][1] + p2[i][1]) / 2
        # ponto local discreto para variavel objeto
        var_objeto = p1[i][0] if random.random() < 0.5 else p2[i][0]

        individuo_recomb.append([var_objeto, passo_mut])

    return individuo_recomb

def recomb_pais_globais(pop):
    individuo_recomb = []

    for i in range(len(pop[0])):
        p1 = random.choice(pop)
        p2 = random.choice(pop)

        # ponto global intermediario para passo de mutacao, que eh um parametro
        passo_mut = (p1[i][1] + p2[i][1]) / 2
        # ponto global discreto para variavel objeto
        var_objeto = p1[i][0] if random.random() < 0.5 else p2[i][0]

        individuo_recomb.append([var_objeto, passo_mut])

    return individuo_recomb

def seleciona_pais(pop):
    "Seleciona dois pais"
    pai1 = random.choice(pop)
    pai2 = random.choice(pop)
    # se vierem 2 dois iguais, sorte dele

    return pai1,pai2

def selecao_virgula(m, l):
    "Selecao (mi, lambda), mi eh um int (tamanho da pop), l eh vetor (crias)"

    ranked = [ x for _,x in sorted(zip([ ackley(y) for y in l ], l)) ]

    return ranked[:m] # trunca!

def main(g=False):
    plt_y_min = []
    plt_y_medio = []
    plt_x = []
    
    pop = pop_init(30, 30)
    lamb = 200 # qtd de filhos
    i = 0
    ackleys = [ ackley(x) for x in pop ]
    ackley_min   = min(ackleys)
    ackley_medio = sum(ackleys)/len(ackleys)

    menor_ackley_encontrado = (ackley_medio, i)
    

    plt_y_min.append(ackley_min)
    plt_y_medio.append(ackley_medio)
    plt_x.append(i)
    recomb_f = None

    if g:
        recomb_f = recomb_pais_globais
    else:
        recomb_f = lambda x: recomb_pais_fixos(*seleciona_pais(x))

    while ackley_min > 0 and i < 2000:
        filhos = [ mutaciona_nao_corre(recomb_f(pop)) for i in range(lamb) ]
        pop = selecao_virgula(30, filhos)
        ackleys = [ ackley(x) for x in pop ]
        i += 1

        ackley_min   = min(ackleys)
        ackley_medio = sum(ackleys)/len(ackleys)
        plt_y_min.append(ackley_min)
        plt_y_medio.append(ackley_medio)
        plt_x.append(i)

        if ackley_medio < menor_ackley_encontrado[0]:
            menor_ackley_encontrado = (ackley_medio, i)
            
    return plt_x, plt_y_medio, plt_y_min, menor_ackley_encontrado

g=False
if len(sys.argv) > 1:
    g = True

y_medio = []
y_min = []
menor_ger = []
menor_val = []

n_iter = 30

for i in range(n_iter):
    xi, yi_medio, yi_min, menori = main(g)
    y_medio.append(yi_medio)
    y_min.append(yi_min)
    menor_val.append(menori[0])
    menor_ger.append(menori[1])
    print(i, 'done')

ym_medio = [0] * len(y_medio[0])
ym_min = [0] * len(y_min[0])
menor_germ = sum(menor_ger)/len(menor_ger)
menor_valm = sum(menor_val)/len(menor_val)

for i in range(len(y_medio[0])):
    for yi in y_medio:
        ym_medio[i] += yi[i]
    for yi in y_min:
        ym_min[i] += yi[i]

ym_medio = [ a/len(y_medio) for a in ym_medio ]
ym_min = [ a/len(y_min) for a in ym_min ]

sd_sum_menor_germ = 0
sd_sum_menor_valm = 0
for i in menor_ger:
    sd_sum_menor_germ += (i - menor_germ)**2

for i in menor_val:
    sd_sum_menor_valm += (i - menor_valm) ** 2

sd_media_menor_valm = sd_sum_menor_valm / len(menor_val)
sd_media_menor_germ = sd_sum_menor_germ / len(menor_ger)

sd_menor_valm = math.sqrt(sd_media_menor_valm)
sd_menor_germ = math.sqrt(sd_media_menor_germ)

menor_ger_arr = round(menor_germ)
plt.annotate('estabilizou!\ngeração média: ' + str(menor_ger_arr)
             + '\ndesvio padrão: ' + str(sd_menor_germ)
             + '\nvalor médio: ' + str(menor_valm)
             + '\ndesvio padrão: ' + str(sd_menor_valm),
             xy=(menor_ger_arr, ym_medio[menor_ger_arr]),
             arrowprops=dict(arrowstyle='->'),
             xytext=(menor_ger_arr - 400,
                     8),
             fontsize='small')

plt.plot(range(len(ym_medio)), ym_medio)
plt.xlabel('Geração')
plt.ylabel('Ackley médio')
print("GAUSSIANA DUAS VEZES")
if g:
    plt.title('Recombinação global, ' + str(n_iter) + ' iterações')
else:
    plt.title('Recombinação de pais fixos, ' + str(n_iter) + ' iterações')

plt.show()

print('menor ackley:', min(ym_min))
