def bellmanFord(n, edges, src):
    dist = [float('inf')] * n 
    dist[src] = 0

    # n - 1 Relaxations
    for i in range(n - 1):
        for u, v, wt in edges:
            if dist[u] != float('inf') and dist[u] + wt < dist[v]:
                dist[v] = dist[u] + wt

    # nth Relaxation to check negative cycle
    for u, v, wt in edges:
        if dist[u] != float('inf') and dist[u] + wt < dist[v]:
            return []

    return dist