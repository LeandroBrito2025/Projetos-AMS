"""Subproblema 3 do catálogo: o roteiro de checagens de conformidade.

A formulação vem do plano da D2, seção 9 (catálogo de subproblemas):
Estado: itens verificados e pendências abertas. Ação: verificar um item ou
resolver uma pendência. Custo: esforço. Objetivo: nenhuma pendência aberta.

Duas interpretações registradas (a coordenação as aprovou na forma do
catálogo; mudou a regra, muda o módulo):

  - "Nenhuma pendência aberta" pressupõe o roteiro completo: os itens do
    roteiro todos verificados E nenhuma pendência em aberto. Sem a parte do
    roteiro, não verificar coisa nenhuma já "cumpriria" o objetivo.
  - Verificar um item com pendências já abertas custa o esforço multiplicado
    pelo `fator_retrabalho` (padrão 2.0): auditar com pendências em aberto
    obriga a rever o que foi visto. É isso que faz a ORDEM importar — fechar
    a pendência antes de seguir a checagem pode sair mais barato. Com
    `fator_retrabalho=1.0` o motor fica com custos uniformes (os testes
    usam isso para provar a otimalidade da busca em largura).

Uma pendência nasce de uma verificação (o caso é fixo: verificar o item X
sempre abre as mesmas pendências) e só sai do estado quando resolvida.

Os dados são inventados e moram nas constantes do módulo — troque pelos do
seu domínio (lab-03) sem tocar na classe.
"""

from __future__ import annotations

from dataclasses import dataclass

VERIFICAR = "verificar"
RESOLVER = "resolver"


@dataclass(frozen=True)
class Item:
    """Um item do roteiro de checagens."""

    nome: str
    esforco: float              # custo de verificar o item (minutos)
    abre: tuple[str, ...] = ()  # pendências que verificar este item abre


@dataclass(frozen=True)
class Pendencia:
    """Uma pendência que uma verificação pode abrir."""

    nome: str
    esforco: float              # custo de resolvê-la (minutos)


# Dados do AMS: roteiro de segurança antes de uma intervenção numa máquina
# de usinagem (ex.: troca do insert de corte). Tempos em minutos.

ITENS_PEQUENOS: tuple[Item, ...] = (
    Item("fontes de energia identificadas", 5.0, ("aplicar bloqueio e etiquetagem",)),
    Item("proteções da máquina no lugar (NR-12)", 3.0, ("reinstalar a proteção do eixo",)),
    Item("ferramentas e EPI conferidos", 2.0),
    Item("permissão de trabalho assinada", 4.0),
    Item("área de trabalho sinalizada", 3.0, ("isolar a área com fita e placa",)),
)
PENDENCIAS_PEQUENAS: dict[str, float] = {
    "aplicar bloqueio e etiquetagem": 10.0,
    "reinstalar a proteção do eixo": 8.0,
    "isolar a área com fita e placa": 5.0,
}

ITENS_MAIORES: tuple[Item, ...] = (
    Item("fontes de energia identificadas", 5.0, ("aplicar bloqueio e etiquetagem",)),
    Item("proteções da máquina no lugar (NR-12)", 3.0, ("reinstalar a proteção do eixo",)),
    Item("ferramentas e EPI conferidos", 2.0),
    Item("permissão de trabalho assinada", 4.0),
    Item("área de trabalho sinalizada", 3.0, ("isolar a área com fita e placa",)),
    Item("instalação elétrica avaliada (NR-10)", 6.0, ("chamar eletricista habilitado",)),
    Item("trabalho em altura descartado (NR-35)", 2.0),
    Item("energia residual descarregada", 4.0, ("aliviar a pressão do circuito pneumático",)),
    Item("histórico de falhas da máquina consultado", 3.0),
    Item("operador do turno avisado", 2.0),
)
PENDENCIAS_MAIORES: dict[str, float] = {
    "aplicar bloqueio e etiquetagem": 10.0,
    "reinstalar a proteção do eixo": 8.0,
    "isolar a área com fita e placa": 5.0,
    "chamar eletricista habilitado": 20.0,
    "aliviar a pressão do circuito pneumático": 6.0,
}


class Conformidade:
    """O problema de busca: em que ordem verificar e resolver.

    O estado é o par (itens verificados, pendências abertas), cada um como
    tupla ordenada. As ações têm verbo no nome — `"verificar:<item>"` e
    `"resolver:<pendência>"` — para o caminho do Resultado ser legível.
    """

    def __init__(
        self,
        itens: tuple[Item, ...],
        pendencias: dict[str, float],
        fator_retrabalho: float = 2.0,
    ):
        self.itens = itens
        self.pendencias = pendencias
        self.fator_retrabalho = fator_retrabalho
        self._item_por_nome = {i.nome: i for i in itens}
        self.estado_inicial: tuple[tuple[str, ...], tuple[str, ...]] = ((), ())

    @staticmethod
    def _partes(acao: str) -> tuple[str, str]:
        verbo, _, nome = acao.partition(":")
        return verbo, nome

    def acoes(self, estado: tuple[tuple[str, ...], tuple[str, ...]]) -> list[str]:
        verificados, abertas = estado
        disponiveis = [f"{VERIFICAR}:{i.nome}" for i in self.itens if i.nome not in verificados]
        return disponiveis + [f"{RESOLVER}:{p}" for p in abertas]

    def transicao(
        self, estado: tuple[tuple[str, ...], tuple[str, ...]], acao: str,
    ) -> tuple[tuple[str, ...], tuple[str, ...]]:
        verificados, abertas = estado
        verbo, nome = self._partes(acao)
        if verbo == VERIFICAR:
            novos_verificados = tuple(sorted((*verificados, nome)))
            novas_abertas = tuple(sorted((*abertas,
                                          *(p for p in self._item_por_nome[nome].abre
                                            if p not in abertas))))
            return novos_verificados, novas_abertas
        if verbo == RESOLVER:
            return verificados, tuple(p for p in abertas if p != nome)
        raise ValueError(f"ação desconhecida: {acao}")

    def objetivo(self, estado: tuple[tuple[str, ...], tuple[str, ...]]) -> bool:
        verificados, abertas = estado
        return len(verificados) == len(self.itens) and not abertas

    def custo(
        self,
        estado: tuple[tuple[str, ...], tuple[str, ...]],
        acao: str,
        estado_seguinte: tuple[tuple[str, ...], tuple[str, ...]],
    ) -> float:
        verbo, nome = self._partes(acao)
        if verbo == VERIFICAR:
            esforco = self._item_por_nome[nome].esforco
            _, abertas = estado
            if abertas:  # auditar com pendência em aberto obriga a rever
                return esforco * self.fator_retrabalho
            return esforco
        return self.pendencias[nome]

    def _trabalho_basico(self, estado: tuple[tuple[str, ...], tuple[str, ...]]) -> float:
        verificados, abertas = estado
        faltar_itens = sum(i.esforco for i in self.itens if i.nome not in verificados)
        fechar_abertas = sum(self.pendencias[p] for p in abertas)
        return faltar_itens + fechar_abertas

    def heuristica_admissivel(
        self, estado: tuple[tuple[str, ...], tuple[str, ...]],
    ) -> float:
        """Esforço base do que falta: itens por verificar + pendências em aberto.

        Admissível: todo item que falta será verificado, e custa no mínimo o
        seu esforço base (o re-trabalho só aumenta); toda pendência aberta
        AGORA terá de ser resolvida, e resolver é a única forma de fechá-la.
        Ignora as pendências que as verificações futuras ainda vão abrir.
        """
        return self._trabalho_basico(estado)

    def heuristica_inadmissivel(
        self, estado: tuple[tuple[str, ...], tuple[str, ...]],
    ) -> float:
        """O dobro do trabalho que falta — a "folga de segurança".

        NÃO é admissível, e é tentadora por isso: estimar com folga para
        "não ser pego de surpresa" superestima o caminho sempre que a folga
        passar do custo real (o lab-05 mede o que isso faz com o A*).
        """
        return 2.0 * self._trabalho_basico(estado)


PEQUENA = Conformidade(ITENS_PEQUENOS, PENDENCIAS_PEQUENAS)
MAIOR = Conformidade(ITENS_MAIORES, PENDENCIAS_MAIORES)
