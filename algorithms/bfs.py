from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class BFS(BaseSearch):

    def search(self, initial: State) -> SearchResult:
        result = SearchResult(solution=None, nodes_generated=1, max_frontier_size=1)

        if initial.is_goal:
            result.solution = initial
            return result

        frontier = deque([initial])
        reached = {initial.tiles}  # estados já gerados (na fronteira ou expandidos)

        while frontier:
            state = frontier.popleft()
            result.nodes_expanded += 1

            for child in state.neighbors():
                if child.tiles in reached:
                    continue
                result.nodes_generated += 1

                # Teste de objetivo na geração: o primeiro objetivo gerado já é o mais raso.
                if child.is_goal:
                    result.solution = child
                    result.depth = child.cost
                    return result

                reached.add(child.tiles)
                frontier.append(child)

            result.max_frontier_size = max(result.max_frontier_size, len(frontier))

        return result
