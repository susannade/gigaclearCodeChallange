import networkx as nx
from dataclasses import dataclass
from typing import List


@dataclass
class RateCard:
    Cabinet: int
    verge: int
    road: int
    Chamber: int
    Pot: int


class CostEstimate:
    def __init__(self, r: RateCard, d: bool, in_path, i: str = None):
        self.rate_card = r
        self.dependence = d
        self.G = nx.read_graphml(in_path)
        self.item_to_cab = i
        if self.dependence:
            self.cabinet = self.find_cabinet()

    def sum_total(self) -> int:
        return self.sum_items() + self.sum_trenches()

    def sum_items(self) -> int:
        sum_i = 0
        for node in self.G.nodes(data=True):
            sum_i += self.calculate_node_value(node)
        return sum_i

    def get_path(self, cab: str, pot: str):
        return nx.shortest_path(self.G, cab, pot)

    def sum_trench_pot_cab(self, path: List[str]) -> int:
        sum_p = 0
        for i in range(len(path) - 1):
            for edge in self.G.edges(data=True):
                if (edge[0], edge[1]) == (path[i], path[i + 1]) or (edge[0], edge[1]) == (path[i + 1], path[i]):
                    sum_p += edge[2]['length']
        return sum_p

    def sum_trenches(self) -> int:
        sum_t = 0
        for edge in self.G.edges(data=True):
            value = getattr(self.rate_card, edge[2]['material'])
            sum_t += (value * int(edge[2]['length']))
        return sum_t

    def find_cabinet(self) -> str:
        for node in self.G.nodes(data=True):
            if node[1]['type'] == 'Cabinet':
                return node[0]
        return 'No cabinet'

    def calculate_node_value(self, node: tuple) -> int:
        value = getattr(self.rate_card, node[1]['type'])
        if self.dependence and node[1]['type'] == self.item_to_cab:
            path = self.get_path(self.cabinet, node[0])
            length = self.sum_trench_pot_cab(path)
            value = value * length
        return value


if __name__ == "__main__":
    input_path = 'problem.graphml'

    rate_card_A = RateCard(Cabinet=1000, verge=50, road=100, Chamber=200, Pot=100)
    rate_card_B = RateCard(Cabinet=1200, verge=40, road=80, Chamber=200, Pot=20)

    cost_A = CostEstimate(rate_card_A, False, input_path)
    total_cost_A = cost_A.sum_total()

    cost_B = CostEstimate(rate_card_B, True, input_path, 'Pot')
    total_cost_B = cost_B.sum_total()

    print(f'Total cost for graph using Rate Card A is {total_cost_A}')
    print(f'Total cost for graph using Rate Card B is {total_cost_B}')


