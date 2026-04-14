from collections import defaultdict

# Time - O(V + E) | Space - O(V)  
def kosaraju(n: int, edges: list[list[int, int]]):
    graph = defaultdict(list)
    revGraph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        revGraph[v].append(u)

    visited = set()
    stack = []
    for i in range(n):
        if i in visited:
            continue
        
        dfs(i, visited, graph, stack)

    scc = 0
    visited = set()
    while stack:
        node = stack.pop()
        if node in visited:
            continue

        scc += 1
        traverse(node, visited, revGraph)

    return scc

def traverse(i, visited, graph):
    if i in visited:
        return
    
    visited.add(i)
    for nei in graph.get(i, []):
        traverse(nei, visited, graph)

def dfs(i, visited, graph, stack):
    if i in visited:
        return
    
    visited.add(i)
    for nei in graph.get(i, []):
        dfs(nei, visited, graph, stack)
    
    stack.append(i)