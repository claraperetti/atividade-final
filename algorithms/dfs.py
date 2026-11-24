from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        result = SearchResult(solution=None, nodes_generated=1, max_frontier_size=1)

        frontier = [initial]  # pilha (LIFO)
        # Menor profundidade em que cada estado já foi alcançado. Um estado só é
        # revisitado se for alcançado por um caminho mais curto, o que garante
        # encontrar solução sempre que existir uma dentro do limite de profundidade.
        best_depth = {initial.tiles: 0}

        while frontier:
            state = frontier.pop()

            # Entrada obsoleta: o estado já foi empilhado de novo por um caminho mais curto.
            if best_depth.get(state.tiles, state.cost) < state.cost:
                continue

            if state.is_goal:
                result.solution = state
                result.depth = state.cost
                return result

            if state.cost >= self.depth_limit:
                continue

            result.nodes_expanded += 1

            # Empilha em ordem reversa para que o primeiro vizinho seja explorado primeiro.
            for child in reversed(state.neighbors()):
                known = best_depth.get(child.tiles)
                if known is not None and known <= child.cost:
                    continue
                best_depth[child.tiles] = child.cost
                frontier.append(child)
                result.nodes_generated += 1

            result.max_frontier_size = max(result.max_frontier_size, len(frontier))

        return result
