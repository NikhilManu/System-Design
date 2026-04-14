from collections import defaultdict


class Solution:
    def __init__(self):
        self.timer = 0

    def tarjan(self, n: int, connections: list[list[int]]) -> list[list[int]]:
        graph = defaultdict(list)
        for a, b in connections:
            graph[a].append(b)
            graph[b].append(a)

        visited = set()
        tin, low = [float('inf')] * n, [float('inf')] * n

        bridges = []
        for i in range(n):
            if i in visited:
                continue

            self.dfs(i, None, visited, graph, tin, low, bridges)
            
        return bridges

    def dfs(self, node, parent, visited, graph, tin, low, bridges):
        visited.add(node)
        tin[node] = low[node] = self.timer
        self.timer += 1

        for nei in graph.get(node, []):
            if nei == parent:
                continue

            if nei not in visited:
                self.dfs(nei, node, visited, graph, tin, low, bridges)
                low[node] = min(low[node], low[nei])

                if low[nei] > tin[node]:
                    bridges.append([node, nei])
            else:
                low[node] = min(low[node], tin[nei])

