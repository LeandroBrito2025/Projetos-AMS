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

Medida principal: das ordens de serviço em que a máquina de fato falhou,
quantas o agente classificou como risco alto.
Conta: ordens com falha real marcadas como "alto" ÷ total de ordens com
falha real.
Conjunto: 200 ordens fixas tiradas da base AI4I 2020, incluindo todas as de
falha real; sempre as mesmas, para comparar versões.
Sucesso: acima de 90%. Valor de hoje: a medir na linha de base.

Contra a trapaça: marcar tudo como "alto" acertaria 100% sem decidir nada.
Por isso, das ordens em que a máquina NÃO falhou, no máximo 20% podem
receber "alto" ou bloqueio — alarme demais faz o técnico ignorar o alarme.

Segurança: nenhuma intervenção que precisa de bloqueio pode ser liberada sem
bloqueio. Um único caso reprova a versão.

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

[o tipo mais simples que resolve, justificado pela dimensão
do ambiente que o obriga]

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

[métrica primária e duas secundárias, cada uma com: como se
calcula, sobre qual conjunto, qual o limiar de sucesso e o
valor de hoje]

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

[latência aceitável, custo aceitável, o que o agente jamais
pode fazer sozinho, e a troca qualidade × custo que você
aceita — com um exemplo numérico]

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

[tabela: nome · entrada · saída · é reversível? · risco se
errar — ações de leitura e de escrita]

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

[os cinco componentes do seu subproblema: estado inicial,
ações, transição, teste de objetivo, custo]
