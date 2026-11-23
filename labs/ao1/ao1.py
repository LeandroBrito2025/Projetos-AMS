"""Arquivo de apoio parcial para a AO1 da D3: compara a linha de base (A) com a sua variante B.

Fica na pasta ao1/, junto com o arquivo de casos. Rode com o .venv ativo:
    cd ao1
    python ao1.py
"""
import csv
import time

import numpy as np

# Do próprio projeto, src/ams/baseline.py:
# decidir() é a variante A; EstadoDaFrota guarda as falhas recentes; carregar_casos() lê o CSV.
from ams.baseline import EstadoDaFrota, carregar_casos, decidir

# Seus 60 casos rotulados (ou o casos-ams-60.csv do pacote do E2).
ARQUIVO_DE_CASOS = "casos-ams-60.csv"


# --- Variante B ---------------------------------------------------------------
# Um agente parecido com a variante A (decidir() de src/ams/baseline.py), com uma
# regra nova ou bem diferente. Tem que mudar o comportamento: ajustar um limite
# em poucos décimos não conta. Abaixo está a A, como ponto de partida.
#
# A minha mudança:
# R: faixa de atenção na vibração. Entre 7,0 e 8,0 mm/s a máquina vai para
#    inspeção, e não para a parada; só acima de 8,0 (ou temperatura acima de 78)
#    ela para. Vem da análise da D2: C11 e C22 pararam à toa logo acima de 7,0.

def decidir_b(caso, estado):
    vibracao = caso["vibracao_mm_s"]        # lê a vibração do caso
    temperatura = caso["temperatura_c"]      # lê a temperatura do caso

    # Muito quente, ou vibração MUITO alta (acima de 8): parar, como antes
    if temperatura > 78 or vibracao > 8.0:
        return "parar_para_manutencao"
    # A NOVIDADE: vibração entre 7 e 8 → só inspecionar, em vez de parar
    if vibracao > 7.0:
        return "inspecionar_antes_de_operar"
    # Daqui para baixo, igual à linha de base: memória das falhas da família
    if estado.falhas_recentes(caso["tipo_maquina"]) >= 2:
        return "inspecionar_antes_de_operar"
    return "seguir_operando"

# --- Acertos de A e B nos mesmos casos (item 1 do enunciado) -------------------
# 1 = acertou a ação, 0 = errou. Grava o acertos.csv que os labs 05 e 06 leem.

def contar_acertos(casos, funcao_de_decisao):
    estado = EstadoDaFrota()
    acertos = []
    for caso in casos:
        decisao = funcao_de_decisao(caso, estado)
        if decisao == caso["acao_correta"]:
            acertos.append(1)
        else:
            acertos.append(0)
        estado.registrar_desfecho(caso)   # o agente fica sabendo se a máquina falhou
    return acertos


casos = carregar_casos(ARQUIVO_DE_CASOS)
acertos_a = contar_acertos(casos, decidir)
acertos_b = contar_acertos(casos, decidir_b)

with open("acertos.csv", "w", newline="") as arquivo:
    escritor = csv.writer(arquivo)
    escritor.writerow(["linha_de_base", "variante_b"])
    for i in range(len(casos)):
        escritor.writerow([acertos_a[i], acertos_b[i]])

print(len(casos), "casos")
print("A acertou", sum(acertos_a), "· B acertou", sum(acertos_b))
for i in range(len(casos)):
    if acertos_a[i] != acertos_b[i]:
        print("discordam no", casos[i]["id_caso"], "· A:", acertos_a[i], "· B:", acertos_b[i])

if acertos_a == acertos_b:
    print("A e B acertaram os mesmos casos. A regra nova da B já foi escrita?")


# --- Latência da linha de base, p50 e p95 (item 2 do enunciado) ----------------
# Cronometra cada decisão, passando 50 vezes pelos casos.

tempos = []
for rodada in range(50):
    estado = EstadoDaFrota()
    for caso in casos:
        inicio = time.perf_counter()
        decidir(caso, estado)
        tempos.append((time.perf_counter() - inicio) * 1_000_000)   # em microssegundos
        estado.registrar_desfecho(caso)

print("latência (µs) em", len(tempos), "decisões:",
      "p50", round(np.percentile(tempos, 50), 1),
      "· p95", round(np.percentile(tempos, 95), 1),
      "· média", round(np.mean(tempos), 1),
      "· máximo", round(np.max(tempos), 1))


# O intervalo de confiança e o tamanho de amostra ficam no notebook (depois do E3, entregues com a N2).
