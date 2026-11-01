# Lab 06 — agente de linha de base (AMS)

Conjunto: os 30 casos do conjunto de reserva do pacote (`casos-de-reserva.csv`),
dados inventados pela coordenação do curso para fim didático. Usei a reserva
porque os dados do AMS (AI4I) têm colunas diferentes das que o agente lê.

Agente: duas regras (`src/ams/baseline.py`). Regra reativa: vibração acima de
7 mm/s ou temperatura acima de 78 °C → parar para manutenção. Regra com estado
interno: duas falhas do mesmo tipo de máquina na última semana → inspecionar
antes de operar. Caso contrário, seguir operando.

## Resultados

| Métrica | Valor | Meta |
|---|---|---|
| Acerto da decisão (medir.py) | 25 de 30 = 83% | — |
| Falhas avisadas (PEAS) | 9 de 11 = 82% | mínimo 90% |
| Alarmes falsos (PEAS) | 4 de 19 = 21% | máximo 20% |

A linha de base não atinge nenhuma das duas metas do PEAS. É o número contra o
qual o agente da D10 será comparado.

## Onde erra, e por quê

O agente erra de forma sistemática em três situações: deixa passar as primeiras
falhas de cada tipo de máquina (C07 e C08, tornos com leituras normais que
falharam), inspeciona à toa máquinas que só são do mesmo tipo das que falharam
(C10, um torno mais novo que não falhou) e manda parar máquinas que vibram mais
por natureza, sem estar com defeito (C11, compressor de 3 meses, e C22, robô).

Isso acontece porque as regras usam um limite único de vibração para todos os
tipos de máquina e uma memória por tipo de máquina, que só reage depois de duas
falhas, e não a história de cada máquina individual. Um agente melhor precisaria
de limites próprios para cada tipo de máquina e de uma memória por máquina, não
por família; o padrão do erro mostra que o problema pede o agente baseado em
modelo com um modelo do mundo mais fino, e não mais regras genéricas.