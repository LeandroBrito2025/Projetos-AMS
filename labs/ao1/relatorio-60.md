# O meu dado, com rigor — relatório do Laboratório 03

Conjunto: `casos-ams-60.csv` · 60 linhas · 9 variáveis

Medidas geradas pelo `medidas.py`: desvio padrão amostral (ddof=1),
quartis por interpolação linear, extremos pela regra da amplitude
interquartil — fora de 1,5 × a caixa (slide 24). As medidas são do
programa; as decisões são SUAS. Preencha todos os blocos `R:` e
confira com `python teste.py`.

## Medidas por variável

| variável | tipo | n | faltantes | média | mediana | desvio | Q1 | Q3 | AIQ | mín | máx |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| id_caso | categórica (60 valores; moda: C09) | 60 | 0 | — | — | — | — | — | — | — | — |
| data | categórica (30 valores; moda: 2026-03-03) | 60 | 0 | — | — | — | — | — | — | — | — |
| tipo_maquina | categórica (4 valores; moda: PRENSA) | 60 | 0 | — | — | — | — | — | — | — | — |
| idade_meses | numérica | 60 | 0 | 52.1833 | 53.0000 | 28.3067 | 36.0000 | 64.0000 | 28.0000 | 3.0000 | 216.0000 |
| temperatura_c | numérica | 60 | 0 | 65.7617 | 63.0000 | 7.1741 | 61.0000 | 66.6250 | 5.6250 | 58.0000 | 83.0000 |
| vibracao_mm_s | numérica | 60 | 0 | 4.3892 | 3.6500 | 1.9195 | 3.0000 | 5.5750 | 2.5750 | 2.0000 | 8.6000 |
| horas_desde_manutencao | numérica | 60 | 0 | 118.9667 | 107.5000 | 51.7399 | 85.0000 | 152.5000 | 67.5000 | 20.0000 | 230.0000 |
| acao_correta | categórica (3 valores; moda: seguir_operando) | 60 | 0 | — | — | — | — | — | — | — | — |
| falhou_depois | numérica | 60 | 0 | 0.3333 | 0.0000 | 0.4754 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 |

## Extremos marcados (fora de 1,5 × a caixa — slide 24)

### Extremos de `idade_meses` — 1 valor(es), limites [-6.0000; 106.0000]

| linha | valor |
|---:|---:|
| 12 | 216.0000 |

Decisão sobre ESTES extremos — manter ou remover, caso a caso,
com o motivo (slide 25: quem remove sem dizer, mente por omissão):

R:

### Extremos de `temperatura_c` — 10 valor(es), limites [52.5625; 75.0625]

| linha | valor |
|---:|---:|
| 2 | 81.5000 |
| 6 | 77.5000 |
| 13 | 79.2000 |
| 17 | 76.0000 |
| 21 | 80.0000 |
| 27 | 82.5000 |
| 34 | 79.5000 |
| 41 | 83.0000 |
| 43 | 79.0000 |
| 53 | 81.0000 |

Decisão sobre ESTES extremos — manter ou remover, caso a caso,
com o motivo (slide 25: quem remove sem dizer, mente por omissão):

R:


## Faltantes (os três mecanismos do slide 26)

Nenhuma variável tem valores faltantes.

## As quatro perguntas do slide 29

**1. Média e mediana se separam em alguma variável? Em qual?**

R:

**2. Quantos extremos foram marcados, e quantos você decidiu manter?**

R:

**3. Algum faltante parece do terceiro mecanismo?**

R:

**4. O que a análise da D1 não tinha visto?**

R:

## Comparação com a análise exploratória da D1

O que mudou de lá para cá — o que a análise de lá não tinha visto,
e o que estas decisões escritas mudam no conjunto que a D5 vai usar:

R:
