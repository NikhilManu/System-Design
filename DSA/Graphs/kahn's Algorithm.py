from collections import deque

# Time - O(V + E) | Space - O(V)
def topoSort(n: int, adj: dict[int, list[int]]) -> list[int]:
    inDegree = [0] * n
    for i in range(n):
        for j in adj.get(i, []):
            inDegree[j] += 1

    queue = deque([])
    for i in range(n):
        if inDegree[i] == 0:
            queue.append(i)
    
    result = []
    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbour in adj[node]:
            inDegree[neighbour] -= 1
            if inDegree[neighbour] == 0:
                queue.append(neighbour)

    return result if len(result) == n else []