#!/usr/bin/python3

import math
import random

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
#    eps =  1e-18
    
    for (var_objeto, passo_mut) in individuo:
        while True:
            passo_mutn = passo_mut * math.exp(tg + tau_fino * random.gauss(0,1))

#            if passo_mutn < eps:
                # evita passos de mutacao muito pequenos
#                passo_mutn = 1

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

def minimiza_ackley():
    pop = pop_init(30, 30)
    lamb = 200 # qtd de filhos
    i = 0
    ackleys = [ ackley(x) for x in pop ]
    print('menor ackley:', min(ackleys))
    print('ackley medio:', sum(ackleys)/len(ackleys))
    print('geracao:', i)
    print('X:', random.choice(pop))

    while min(ackleys) > 0 or i < 200000:
        filhos = [ mutaciona_nao_corre(recomb_pais_fixos(*seleciona_pais(pop))) for i in range(lamb) ]
        pop = selecao_virgula(30, filhos)
        ackleys = [ ackley(x) for x in pop ]
        i += 1

        if (i % 100 == 0):
            print('menor ackley:', min(ackleys))
            print('ackley medio:', sum(ackleys)/len(ackleys))
            print('geracao:', i)
        if (i % 1000 == 0):
            print('X:', random.choice(pop))

    print('menor ackley:', min(ackleys))
    print('ackley medio:', sum(ackleys)/len(ackleys))
    print('geracao:', i)


def minimiza_ackley_global():
    pop = pop_init(30, 30)
    lamb = 200 # qtd de filhos
    i = 0
    ackleys = [ ackley(x) for x in pop ]
    print('menor ackley:', min(ackleys))
    print('ackley medio:', sum(ackleys)/len(ackleys))
    print('geracao:', i)
    print('X:', random.choice(pop))

    while min(ackleys) > 0 or i < 200000:
        filhos = [ mutaciona_nao_corre(recomb_pais_globais(pop)) for i in range(lamb) ]
        pop = selecao_virgula(30, filhos)
        ackleys = [ ackley(x) for x in pop ]
        i += 1

        if (i % 100 == 0):
            print('menor ackley:', min(ackleys))
            print('ackley medio:', sum(ackleys)/len(ackleys))
            print('geracao:', i)
        if (i % 1000 == 0):
            print('X:', random.choice(pop))

    print('menor ackley:', min(ackleys))
    print('ackley medio:', sum(ackleys)/len(ackleys))
    print('geracao:', i)
    
minimiza_ackley()

