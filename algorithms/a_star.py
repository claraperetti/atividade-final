import heapq
from itertools import count
from puzzle.base_search import BaseSearch
from puzzle.state import State, GOAL_STATE
from puzzle.result import SearchResult

# Posição (linha, coluna) de cada peça no estado objetivo.
GOAL_POSITIONS = {tile: divmod(i, 3) for i, tile in enumerate(GOAL_STATE)}


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        """Distância de Manhattan: soma, para cada peça (exceto o vazio), da
        distância horizontal + vertical até sua posição no objetivo.
        É admissível porque cada movimento desloca uma única peça em uma casa."""
        distance = 0
        for i, tile in enumerate(state.tiles):
            if tile == 0:
                continue
            row, col = divmod(i, 3)
            goal_row, goal_col = GOAL_POSITIONS[tile]
            distance += abs(row - goal_row) + abs(col - goal_col)
        return distance

    def search(self, initial: State) -> SearchResult:
        result = SearchResult(solution=None, nodes_generated=1, max_frontier_size=1)

        tie = count()  # desempate estável (FIFO) entre nós com mesmo f
        frontier = [(self.heuristic(initial), next(tie), initial)]
        best_cost = {initial.tiles: 0}  # menor g conhecido para cada estado
        expanded = set()

        while frontier:
            _, _, state = heapq.heappop(frontier)

            if state.tiles in expanded:
                continue  # entrada obsoleta, já expandida com custo menor

            if state.is_goal:
                result.solution = state
                result.depth = state.cost
                return result

            expanded.add(state.tiles)
            result.nodes_expanded += 1

            for child in state.neighbors():
                if child.tiles in expanded:
                    continue
                if child.cost < best_cost.get(child.tiles, float("inf")):
                    best_cost[child.tiles] = child.cost
                    f = child.cost + self.heuristic(child)
                    heapq.heappush(frontier, (f, next(tie), child))
                    result.nodes_generated += 1

            result.max_frontier_size = max(result.max_frontier_size, len(frontier))

        return result
