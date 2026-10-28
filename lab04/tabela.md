# Labs 04 e 05 — buscas no roteiro de segurança do AMS (instância maior)

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

## Conclusão

Sim, o custo uniforme achou um roteiro de 83 minutos, contra 112 da largura, com o mesmo número de passos (15). A diferença está na ordem dos passos: a largura procura o caminho com menos passos e não olha os minutos, e por isso aceitou uma ordem em que itens foram conferidos com pendência aberta, pagando o dobro. Já o custo uniforme procura o caminho mais barato, e escolheu uma ordem que evita esse custo dobrado.

O número baixo da profundidade limitada não significa que ela foi melhor, porque ela é contada de outro jeito: as outras buscas contam cada vez que tiram algo da lista de caminhos, e ela, que não tem lista, conta só as vezes que entrou em um novo passo. Além disso, o roteiro que ela encontrou custou 112 minutos, o mesmo da largura, e não o mais barato.

## Dominância das heurísticas (Lab 05)

Entre duas heurísticas admissíveis, domina a que estima mais alto em todo estado, porque fica mais perto do custo real sem passar dele. A heurística inadmissível estima sempre o dobro da admissível e por isso examinou menos nós (7.638 contra 33.185), mas ela não pode dominar, porque passa do custo real. Por exemplo, quando só falta resolver o bloqueio, o custo real é 10 minutos e ela estima 20. A A* com a admissível achou o roteiro ótimo de 83 minutos examinando 33.185 nós, contra 45.352 do custo uniforme. A inadmissível também achou 83 nesta instância, mas por sorte, e não por garantia: em outros problemas, ela entrega roteiros piores.