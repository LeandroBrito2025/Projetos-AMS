# Relatório de desempenho da linha de base — AMS

**Projeto:** AMS — Assistente de Manutenção Segura · **Data:** 01/11/2026

## 1. A métrica primária

Métrica do PEAS (seção 4 do `agent-spec.md`): **falhas avisadas** — dos casos
em que a máquina de fato falhou (`falhou_depois = 1`), a fração em que o
agente alarmou, isto é, decidiu inspecionar ou parar. Conta: casos com falha
real alarmados ÷ total de casos com falha real. Meta: no mínimo 90%.

Com ela, o termo contra a trapaça: **alarmes falsos** — dos casos em que a
máquina não falhou, a fração em que o agente alarmou. Meta: no máximo 20%.

O `medir.py` imprime também o **acerto da decisão** (decisões iguais ao
rótulo ÷ total), usado aqui como secundária: ele distingue inspecionar de
parar, o que as duas contas acima não distinguem.

## 2. O valor

Saída do `medir.py`:

```
Métrica primária: acerto da decisão (casos com decisão igual à rotulada, sobre o total)
Valor: 25/30 = 0.8333
```

| Métrica | Valor | Meta |
|---|---|---|
| Falhas avisadas (primária) | 9/11 = 0.82 | mínimo 0.90 |
| Alarmes falsos | 4/19 = 0.21 | máximo 0.20 |
| Acerto da decisão | 25/30 = 0.83 | mínimo 0.90 |

A linha de base não atinge nenhuma das metas. É o número contra o qual o
agente da D10 será comparado.

## 3. O conjunto

`lab06/casos-de-reserva.csv`: os 30 casos rotulados do conjunto de reserva do
pacote D2-06, de 02/03/2026 a 20/03/2026, em ordem cronológica. Distribuição
dos rótulos: 16 seguir operando, 7 inspecionar antes de operar, 7 parar para
manutenção; 11 casos falharam depois e 19 não.

**Declaração:** usei o conjunto de reserva, dados inventados pela coordenação
do curso para fim didático (ver `lab06/FONTE.md`). Os dados do AMS (AI4I 2020)
têm colunas diferentes das que o agente lê; a troca para um conjunto próprio é
uma linha (`CAMINHO_DOS_CASOS`) quando ele existir.

## 4. Onde o agente erra

```
Onde erra (o rótulo que o agente não deu):
  caso C07: decidiu seguir_operando, correto era inspecionar_antes_de_operar
  caso C08: decidiu seguir_operando, correto era inspecionar_antes_de_operar
  caso C10: decidiu inspecionar_antes_de_operar, correto era seguir_operando
  caso C11: decidiu parar_para_manutencao, correto era inspecionar_antes_de_operar
  caso C22: decidiu parar_para_manutencao, correto era inspecionar_antes_de_operar
```

**O padrão.** Os cinco erros não são aleatórios: caem em três grupos, e
nenhum deles está nos casos extremos — os sete casos de "parar" com vibração
ou temperatura alta foram todos acertados. C07 e C08 são as duas primeiras
falhas de tornos, com leituras normais, que o agente deixou passar. C10 é um
torno mais novo, inspecionado só por ser do mesmo tipo dos que falharam. C11 e
C22 são máquinas que vibram mais por natureza (um compressor de 3 meses e um
robô) e foram mandadas parar sem estar com defeito.

**A hipótese do porquê.** O agente não enxerga a história de cada máquina:
a memória é por tipo de máquina e só reage depois de duas falhas, por isso
chega atrasada nas primeiras (C07, C08) e pune o tipo inteiro depois (C10).
E o limite de vibração é único para todos os tipos, por isso confunde a
característica normal de uma máquina com defeito (C11, C22).

## 5. A tabela comparativa de busca

Formulação: subproblema 3 do catálogo (roteiro de conformidade) com os dados
do AMS — o roteiro de segurança antes da intervenção (`roteiro_ams.py`,
instância maior: 10 itens, 5 pendências).

| Busca | Custo | Ações | Nós expandidos | Nós gerados | Prof. máx. | Segundos |
|---|---:|---:|---:|---:|---:|---:|
| largura | 112.0 | 15 | 45352 | 45360 | 15 | 0.1041 |
| custo_uniforme | 83.0 | 15 | 45352 | 45360 | 15 | 0.1695 |
| profundidade_limitada(limite=32) | 112.0 | 15 | 16 | 15 | 15 | 0.0001 |
| aprofundamento_iterativo(limite=32) | 112.0 | 15 | 58336 | 317535 | 15 | 0.9699 |
| gulosa[admissivel] | 83.0 | 15 | 22 | 83 | 15 | 0.0015 |
| a_estrela[admissivel] | 83.0 | 15 | 33185 | 38704 | 15 | 0.3686 |
| gulosa[inadmissivel] | 83.0 | 15 | 22 | 83 | 15 | 0.0007 |
| a_estrela[inadmissivel] | 83.0 | 15 | 7638 | 10920 | 15 | 0.0926 |

**A pergunta do item 4.** Sim: a A estrela com a heurística admissível manteve
o custo ótimo (83 minutos, o mesmo do custo uniforme) e expandiu 33.185 nós
contra 45.352, cerca de 27% menos. A economia é modesta porque a heurística
estima baixo: ela soma o tempo do que falta sem contar as pendências que os
itens ainda vão abrir nem o custo dobrado, e o espaço tem muitas ordens
diferentes com custo parecido. A inadmissível também achou 83 nesta
instância, mas por sorte, não por garantia: ela superestima (com só o
bloqueio por resolver, o real é 10 minutos e ela estima 20).

**A ressalva de contagem.** Os 16 nós da profundidade limitada não significam
que ela foi melhor: ela é recursiva e não tem fronteira, então conta só as
entradas em um novo passo, e não as retiradas da lista como as outras. Além
disso, o roteiro que ela achou custou 112 minutos, e não o mais barato.
