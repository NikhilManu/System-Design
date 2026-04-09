from collections import defaultdict
import heapq

# Time - O(E log V) | Space - O(V)
def MST(n: int, edges: list[list[int, int, int]]):
    graph = defaultdict(list)
    for u, v, wt in edges:
        graph[u].append((wt, v))
        graph[v].append((wt, u)) 
    
    visited = set()
    pathSum = 0
    mst = []

    minHeap = [(0, 0, -1)]
    while len(visited) < n:
        wt, node, parent = heapq.heappop(minHeap)
        if node in visited:
            continue
        
        visited.add(node)
        pathSum += wt
        
        if parent != -1:
            mst.append((parent, node, wt))
            
        for neiWt, neiNode in graph.get(node, []):
            heapq.heappush(minHeap, (neiWt, neiNode, node))

    return pathSum, mst