# Análise — o que torna o problema difícil, e que agente ele exige

## O que torna o problema difícil

A observabilidade parcial (seção 2 do `agent-spec.md`) não é rótulo aqui: a
linha de base perdeu os casos C07 e C08, dois tornos com temperatura e
vibração normais que falharam depois. A informação que decide — o estado real
da máquina e a sua história individual — não está na percepção do instante,
e a memória por tipo de máquina só reage depois de duas falhas, chegando
atrasada justamente nas primeiras. No AMS real isso é ainda mais sério: o
agente não percebe se a máquina está energizada, e é isso que decide a NR-10
e o bloqueio.

O ambiente também é estocástico: leituras parecidas levam a desfechos
diferentes. C11 (compressor de 3 meses) e C22 (robô) passaram do limite de
vibração e não falharam, porque um limite único para todos os tipos confunde a
característica normal de uma máquina com defeito. Com a mesma percepção,
o que existe é probabilidade, não certeza — por isso o risco é dado em níveis.

Na fatia que é busca, a dificuldade é o tamanho: o roteiro de segurança tem
sempre 15 passos, mas a ordem muda o custo (112 minutos na largura, 83 no
ótimo), e a heurística admissível, que ignora as pendências futuras e o custo
dobrado, só economizou 27% dos nós (33.185 contra 45.352).

## Que tipo de agente o problema realmente exige

O reativo simples não basta: C07 e C08 mostram que a leitura do momento não
decide. O problema exige um agente baseado em modelo, mas com um modelo do
mundo mais fino que o da linha de base: memória por máquina, e não por tipo
(C10 foi inspecionado só por ser torno), e limites de vibração e temperatura
próprios de cada tipo de máquina (C11, C22). Busca só entra no roteiro de
segurança, que tem ordem a escolher; a classificação do risco não é busca. O
custo desigual dos erros — liberar sem bloqueio custa muito mais que bloquear
à toa — entra como restrição fixa, e não como regra a ser aprendida. Essa
escolha obriga o projeto a guardar o histórico de cada máquina com uma
janela de tempo, e dispensa planejamento na classificação.

## O que isto muda no projeto

A D10 precisa trazer o histórico individual de cada máquina (um dado novo),
limites por tipo de máquina, aprendidos dos dados em vez de fixos, e um
verificador determinístico para o bloqueio: o modelo sugere, o código
garante que nada é liberado sem bloqueio quando ele é exigido. Onde a linha
de base é competitiva — os sete casos de "parar" com vibração ou temperatura
alta, todos acertados —, a regra simples deve continuar valendo: isso é
informação valiosa, porque mostra onde o agente com modelo não precisa entrar.

Conjunto usado: os 30 casos de reserva do pacote D2-06, dados inventados pela
coordenação para fim didático.
