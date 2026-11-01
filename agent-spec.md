# agent-spec.md — modelo do meu agente

<!--
Este arquivo é para preencher, não para ler e devolver. As perguntas de cada
seção estão em comentário como este: elas não aparecem na pré-visualização,
aparecem no editor. Responda ABAIXO de cada seção, apagando nada delas.

As seções que ainda não foram vistas em aula ficam de pé, com a linha
"quando se preenche" dizendo o encontro em que isso acontece. O documento
cresce a cada laboratório — o de hoje é o primeiro.

Preencha com exemplos concretos do SEU domínio. Uma linha que funcionaria
para qualquer empresa é uma linha genérica — o exemplo do seu segmento
(agente-spec-exemplo.pdf, no mesmo pacote) mostra o contraste.
-->

**Domínio:** AMS - Assistente de Manutenção Segura
**Autor(a):** Leandro · **Última revisão:** 15/10/2026

---

## 1. PEAS

<!-- Perguntas que guiam o preenchimento:
  - Performance: o que conta como sucesso, em uma fórmula? Sobre o quê se
    conta, sobre qual conjunto, quanto é sucesso? Qual termo impede a
    trapaça mais óbvia (fechar rápido sem resolver)?
  - Environment: onde o agente opera? O que existe lá — sistemas, pessoas,
    documentos, ruído? Cite elementos concretos.
  - Actuators: o que o agente pode FAZER? Inclua comunicar e escalar:
    informar a decisão é uma ação, e passar adiante também é.
  - Sensors: o que o agente consegue PERCEBER? Só o que ele enxerga existe
    para ele.
  Um PEAS que menciona tecnologia de solução (banco vetorial, nome de modelo)
  está descrevendo a solução — o PEAS descreve o problema.
-->
**Quando se preenche:** no Laboratório 01, hoje. Refinado na Atividade Orientada.

**Performance:**

Medida principal: das máquinas que de fato falharam, a fração que o agente alarmou (decidiu inspecionar ou parar). Conta: casos com falha real alarmados ÷ total de casos com falha real. Conjunto: os 30 casos rotulados do conjunto de reserva do pacote D2-06 (11 falharam, 19 não) — sempre os mesmos, para comparar versões. Sucesso: no mínimo 90%. Valor de hoje (linha de base): 9 de 11 = 82%.

Contra a trapaça: alarmar tudo acertaria 100% sem decidir nada. Por isso, das máquinas que NÃO falharam, no máximo 20% podem ser alarmadas. Valor de hoje: 4 de 19 = 21%.

Segurança: nenhuma intervenção que precisa de bloqueio pode ser liberada sem bloqueio. Um único caso reprova a versão.

Revisão (N2): o conjunto passou das "200 ordens da AI4I" para os 30 casos da reserva, porque é sobre eles que a linha de base foi medida (a AI4I tem colunas diferentes das que o agente lê); o "valor de hoje", antes "a medir", agora tem o número medido.

**Environment:**

Uma fábrica com máquinas de usinagem de três classes (L, M, H); as ordens de
serviço que chegam à manutenção, com descrição em texto livre; o técnico de
manutenção, com pouco tempo entre uma ordem e outra; o supervisor de
segurança, que confere as recomendações depois; as normas NR-10, NR-12 e
NR-35. E os problemas reais: sensor sem leitura ou com valor impossível,
descrição vaga ("verificar barulho no eixo"), parte elétrica não mencionada
na ordem.

**Actuators:**

Classificar o risco de falha (baixo / médio / alto); indicar as normas que
valem para a intervenção; recomendar ou dispensar o bloqueio e etiquetagem;
explicar ao técnico a recomendação em poucas linhas; chamar o supervisor de
segurança quando a ordem estiver incompleta ou confusa; registrar cada
avaliação para conferência. O agente só recomenda: quem bloqueia a máquina e
libera o serviço é o técnico.

**Sensors:**

A leitura dos sensores da máquina na ordem — temperatura do ar, temperatura
do processo, rotação, torque e desgaste da ferramenta; a classe da máquina;
o texto da descrição do serviço; o código da máquina. O que o agente NÃO
percebe: o estado físico da máquina, se ela está energizada e o que foi
feito nela antes — isso só chega se estiver escrito na ordem.

---

## 2. O ambiente em sete dimensões

<!--
Perguntas que guiam o preenchimento (uma por dimensão):
  - Observabilidade: existe algo que muda a decisão e o agente não mede?
  - Número de agentes: existe alguém cujas ações mudam o seu resultado?
    Um humano que reage ao agente conta.
  - Determinismo: a mesma ação no mesmo estado dá sempre o mesmo efeito?
  - Episódico ou sequencial: a decisão de agora afeta as decisões seguintes?
  - Estático ou dinâmico: o ambiente muda enquanto o agente delibera?
  - Discreto ou contínuo: estados e ações são contáveis?
  - Conhecido ou desconhecido: o agente sabe de antemão as regras? (Trata do
    que ele SABE, não do que ele VÊ.)
  Cada classificação vem com uma frase de justificativa — a etiqueta sozinha
  não vale nada.
-->
**Quando se preenche:** no Laboratório 02, no sábado (encontro 2).

| Dimensão | Classificação | Justificativa |
|---|---|---|
| Observabilidade | Parcialmente observável | O agente não percebe se a máquina está energizada, nem o que foi feito nela antes, e a falha ainda não aconteceu — só enxerga a leitura do momento e o texto da ordem, que pode omitir a parte elétrica |
| Determinismo | Estocástico | Duas máquinas com a mesma leitura podem ter desfechos diferentes: a falha é probabilidade, não certeza; e a própria consulta que gera a recomendação pode variar ou falhar |
| Número de agentes | Agente único (com ressalva) | Técnico e supervisor recebem a recomendação e não disputam a decisão com o agente; a ressalva é que o técnico pode ignorar alertas — por isso a medida limita os alarmes falsos |
| Episódico ou sequencial | Episódico | Cada ordem é avaliada sozinha: errar uma não muda a avaliação da seguinte. Mudaria para sequencial se a recomendação de uma ordem passasse a depender do desfecho da anterior |
| Estático ou dinâmico | Semidinâmico | A máquina não muda durante a análise, mas o técnico está esperando: depois de certo tempo, a recomendação chega tarde demais para ser usada |
| Discreto ou contínuo | Percepções contínuas, ações discretas | Temperatura, rotação, torque e desgaste variam sem degraus; a saída é contável — três níveis de risco, um conjunto de normas, bloquear ou não |
| Conhecido ou desconhecido | Parcialmente conhecido | As normas estão documentadas; a relação entre a leitura dos sensores e a falha não é dada de antemão e precisa ser descoberta nos dados |

**O que essas respostas obrigam no projeto:**

- Parcialmente observável → guardar o histórico de falhas de cada máquina e escalar ao supervisor quando faltar informação.
- Estocástico → risco expresso em níveis de probabilidade, nova tentativa quando a consulta falha e tempo máximo de espera.
- Episódico → a avaliação usa um conjunto de ordens independentes (as 200 do PEAS), sem precisar avaliar trajetórias.
- Semidinâmico → prazo de resposta declarado; passado o prazo, o técnico segue sem a recomendação.
- Contínuo na entrada → os limites que separam baixo, médio e alto são decisão de projeto, a justificar.
- Parcialmente conhecido → a relação sensor → falha vem da análise dos dados, não de regra escrita à mão.

---

## 3. Tipo de agente pretendido

<!--
Perguntas que guiam o preenchimento:
  - O tipo mais simples que resolve: reativo simples, baseado em modelo,
    baseado em objetivos, baseado em utilidade, ou um deles com aprendizagem?
  - A caracterização do ambiente (seção 2) é que decide — parcialmente
    observável elimina o reativo simples.
  - Justifique com a dimensão do ambiente que obriga a escolha.
-->
**Quando se preenche:** no sábado (encontro 2, manhã).

**Baseado em modelo.**

O ambiente é parcialmente observável (seção 2), o que elimina o reativo
simples: a leitura do momento não basta — uma máquina que falhou duas vezes
na semana merece mais cuidado mesmo com a leitura de hoje normal. O agente
mantém um estado interno mínimo: o histórico de falhas de cada máquina.

Por que não um tipo acima: o ambiente é episódico e a decisão é uma
classificação (risco, normas, bloqueio), não uma sequência de passos a
planejar — por isso não é baseado em objetivos. O custo desigual dos erros
(liberar sem bloqueio custa muito mais que bloquear sem precisar) é tratado,
nesta versão, por regra fixa: na dúvida sobre a parte elétrica, recomenda o
bloqueio ou escala ao supervisor. A função de utilidade com pesos fica para
as restrições (seção 5). Aprendizagem fica para depois: exige registrar o
desfecho de cada recomendação, o que o sistema ainda não faz.

Na fronteira fluxo de trabalho × agente, o AMS é hoje um fluxo de trabalho:
o código decide a sequência (lê a ordem → consulta → valida → registra), não
o modelo. O problema tem caminho conhecido, e por isso essa é a escolha certa.

---

## 4. Medida de desempenho

<!--
Perguntas que guiam o preenchimento:
  - A fórmula do campo Performance, agora em definição operacional: como se
    calcula, passo a passo, sem ambiguidade?
  - Métrica primária e duas secundárias. As secundárias pegam o que a
    primária deixa passar (custo, latência, reabertura).
  - O conjunto de casos: de onde vêm, quantos são, de que período.
  - O limiar de sucesso e o valor de hoje.
-->
**Quando se preenche:** a fórmula começa no Laboratório 01; a definição
operacional completa — primária, secundárias, conjunto e limiar — é item da
Atividade Orientada.

Primária — falhas avisadas. Como se calcula: percorrer os casos em ordem cronológica; separar os que têm falhou_depois = 1; contar em quantos o agente decidiu inspecionar ou parar; dividir pelo total desses casos. Conjunto: os 30 casos da reserva (lab06/casos-de-reserva.csv, 02 a 20/03/2026). Sucesso: no mínimo 90%. Valor de hoje: 9/11 = 82%.

Secundária — alarmes falsos. Casos com falhou_depois = 0 em que o agente decidiu inspecionar ou parar, divididos pelo total desses casos. Meta: no máximo 20%. Valor de hoje: 4/19 = 21%. Pega a trapaça de alarmar tudo para acertar a primária.

Secundária — acerto da decisão. Decisões iguais ao rótulo divididas pelo total (a saída do medir.py). Meta: no mínimo 90%. Valor de hoje: 25/30 = 83%. Pega o que as duas anteriores não veem: mandar parar quando bastava inspecionar.

A restrição de segurança (nenhuma liberação sem bloqueio quando exigido) ainda não é medida: o conjunto de reserva não tem rótulo de bloqueio. Fica registrada como medida a construir na D7.

Revisão (N2): seção nova, escrita depois da devolutiva do E3, que pediu métrica com fórmula, conjunto e limiar — e com o valor de hoje medido.

---

## 5. Restrições

<!--
Perguntas que guiam o preenchimento:
  - Latência aceitável: a partir de quantos segundos a resposta perde valor?
  - Custo aceitável: quanto pode custar cada resolução?
  - O que o agente jamais pode fazer: a ação irreversível que ele não executa
    sozinho. Esta linha vira política em D12.
  - A troca que você aceita: quanto de qualidade por quanto de custo?
    Um exemplo numérico vale mais que a fórmula.
-->
**Quando se preenche:** na Atividade Orientada.

Latência: a recomendação deve chegar em até 10 segundos. O técnico tem pouco tempo entre uma ordem e outra (ambiente semidinâmico, seção 2): acima de 30 segundos ela chega tarde, e o técnico segue sem ela.

Custo: até R$ 0,05 por ordem avaliada, somando as chamadas ao modelo.

O que o agente jamais faz sozinho: liberar a intervenção (seção 6). O efeito não se desfaz, e o pior cenário é um acidente com o técnico.

A troca que aceito: perder até 3 pontos do acerto da decisão para cortar o custo pela metade — por exemplo, 25/30 a R$ 0,02 por ordem vale mais que 26/30 a R$ 0,05. Mas não aceito perder nenhum ponto de falhas avisadas por economia: deixar passar uma máquina que vai falhar custa muito mais que qualquer chamada, e o termo de risco pesa mais que os outros.

Revisão (N2): seção nova. A troca com exemplo numérico segue o encontro 4: o termo de risco (erro irreversível) tem peso maior que custo e latência.

---

## 6. Catálogo de ações

<!--
Perguntas que guiam o preenchimento:
  - Para cada ação: nome, entrada, saída, é reversível?, qual o risco se
    errar? As quatro colunas são obrigatórias — "baixo" não é descrição de
    risco.
  - Ações de leitura E de escrita: as que alteram o mundo são as que exigem
    cuidado, e são justamente as que mais ficam de fora.
  - Este catálogo é, literalmente, a lista de ferramentas que você vai
    implementar em D10.
-->
**Quando se preenche:** na Atividade Orientada — o pacote `D2-07` traz o
modelo da tabela e dois exemplos preenchidos.

| Ação | Entrada | Saída | É reversível? | Risco se errar |
|---|---|---|---|---|
| Ler a ordem de serviço | Número da ordem | Máquina, leitura dos sensores, descrição do serviço | Sim — só lê | Leitura com sensor falhando ou descrição vaga (sem citar a parte elétrica) leva a classificação errada; o técnico recebe recomendação baseada em dado ruim |
| Consultar o histórico de falhas da máquina | Código da máquina | Falhas recentes da máquina | Sim — só lê | Histórico desatualizado subestima o risco: a máquina que já falhou parece nova (o erro de C07 e C08 da linha de base) |
| Classificar o risco e indicar as normas | Leitura + histórico + descrição | Nível de risco (baixo/médio/alto) e normas aplicáveis (NR-10/12/35) | Sim — só calcula, não muda o mundo | Falso negativo: máquina que vai falhar sai como risco baixo, ou a NR-10 fica de fora numa intervenção elétrica. Falso positivo: parada à toa e alarme que o técnico passa a ignorar |
| Comunicar a recomendação ao técnico | Risco + normas + bloqueio sim/não + justificativa | Mensagem curta ao técnico | Não — a mensagem lida orienta a ação do técnico e não se recolhe | Comunicação: "não precisa bloquear" quando precisava expõe o técnico a energia na máquina; justificativa confusa faz a recomendação ser ignorada |
| Escalar ao supervisor de segurança | Ordem + o que já foi avaliado | Caso na fila do supervisor | Sim — o caso volta para o fluxo normal | Escalar demais cria fadiga e atrasa o serviço; escalar sem o que já foi avaliado obriga o supervisor a refazer tudo |
| Registrar a avaliação | Ordem + decisão + justificativa | Registro para auditoria | Parcialmente — o registro pode ser corrigido, mas a falta dele não se recupera depois | Registro incompleto impede o supervisor de auditar a decisão e deixa a responsabilidade indefinida num acidente |
| Liberar a intervenção | Ordem + bloqueio confirmado | Ordem liberada; o técnico começa o serviço | Não — o serviço começa, e um acidente não se desfaz | Escrita, risco alto: liberar máquina energizada ou sem proteção pode causar choque elétrico, prensagem ou amputação do técnico |

**Quem executa cada ação:** as ações de leitura e cálculo (ler a ordem, consultar o histórico, classificar o risco) e o registro, o agente executa sozinho. Comunicar a recomendação e escalar ao supervisor, o agente executa sozinho, porque são as formas de pôr um humano no circuito. Liberar a intervenção exige confirmação humana: o técnico confirma o bloqueio e, nos casos de risco alto ou de parte elétrica, o supervisor de segurança aprova.

**O que o agente JAMAIS executa sozinho:** liberar a intervenção. O efeito não se desfaz e o pior cenário é um acidente com o técnico. Por isso a entrada da ação já exige o "bloqueio confirmado", e a liberação fica sempre com um humano.

Revisão (N2): seção nova (Laboratório 07). Seguindo a devolutiva do E3, inclui as ações que alteram o mundo (liberar a intervenção, comunicar ao técnico) e as colunas de reversibilidade e risco com o cenário concreto.

---

## 7. Formulação por busca

<!--
Perguntas que guiam o preenchimento:
  - Qual fatia do problema é um espaço de estados? (Nem toda fatia é — e
    reconhecer a que não é vale tanto quanto formular a que é.)
  - Os cinco componentes: estado inicial, ações, modelo de transição, teste
    de objetivo, custo de caminho. Comece pelo teste de objetivo.
  - O estado descreve a SITUAÇÃO, não a história de como se chegou nela.
-->
**Quando se preenche:** no Laboratório 03, sábado à tarde (encontro 2).

A fatia do problema que é busca: em que ordem cumprir o roteiro de segurança
antes de liberar a intervenção numa máquina. Caminho padrão: subproblema 3 do
catálogo (roteiro de conformidade), copiado para `roteiro_ams.py` com os dados
trocados pelos do AMS — a lógica é a do catálogo, sem alteração.

| Componente | No AMS |
|---|---|
| Estado inicial | Nenhum item conferido, nenhuma pendência aberta |
| Ações | Verificar um item ainda não verificado, ou resolver uma pendência aberta |
| Transição | Verificar soma o item aos verificados e abre as pendências que ele revela; resolver tira a pendência das abertas |
| Teste de objetivo | Todos os itens verificados e nenhuma pendência aberta — só então a intervenção é liberada |
| Custo | Tempo da ação em minutos; verificar com pendência aberta custa o dobro, porque obriga a reconferir |

O estado é o par (itens verificados, pendências abertas) — a situação, não a
ordem em que as coisas foram feitas. Teste de sanidade: seis verificações
verdes nas duas instâncias (pequena: 5 itens, 3 pendências; maior: 10 itens,
5 pendências).

Simplificação: cada item revela sempre as mesmas pendências. No mundo real,
verificar pode ou não revelar um problema — o ambiente é estocástico (seção 2).

O que não é busca no AMS: classificar o risco de falha é classificação a
partir dos sensores, não sequência de passos; indicar as normas é consulta.

Resultado (Labs 04 e 05): o custo uniforme achou o roteiro ótimo de 83 minutos, contra 112 da largura, com os mesmos 15 passos; a A* com a heurística admissível achou os mesmos 83 expandindo 33.185 nós, contra 45.352 do custo uniforme (27% menos). Tabela completa em relatorio-de-desempenho.md.

---

## Registro de revisões (o que mudou e por quê)

| Seção | O que mudou | Por quê |
|---|---|---|
| 1. PEAS | Conjunto da medida: de 200 ordens da AI4I para os 30 casos da reserva; valor de hoje preenchido (82% e 21%) | A linha de base foi medida na reserva; sem o valor de hoje, não há como saber se o número novo é bom |
| 2. Ambiente | Sem mudança | A linha de base confirmou a observabilidade parcial (C07, C08) e o ambiente estocástico (C11, C22) |
| 3. Tipo | Sem mudança | Baseado em modelo foi confirmado; a revisão aponta que a memória deve ser por máquina, não por tipo (C10) |
| 4. Medida | Seção nova: primária, duas secundárias, conjunto, metas e valores | Devolutiva do E3: medida com fórmula, conjunto e limiar |
| 5. Restrições | Seção nova, com a troca qualidade × custo em número | Encontro 4: o custo de pensar e o peso do risco |
| 6. Catálogo | Seção nova, com ações de escrita e comunicação | Devolutiva do E3: ações que alteram o mundo, reversibilidade e risco |
| 7. Busca | Acrescentado o resultado das buscas | Labs 04 e 05 | 