# Find shortest path from source to all vertices in a graph.
import heapq

def dijkstra(n: int, adj: dict[int, list[tuple[int, int]]], src: int) -> list[int]:
    minHeap = [(0, src)]
    distances = [float('inf')] * n
    distances[src] = 0

    while minHeap:
        dist, node = heapq.heappop(minHeap)

        for neighborNode, neighborDist in adj.get(node, []):
            newDist = dist + neighborDist
            if newDist < distances[neighborNode]:
                distances[neighborNode] = newDist
                heapq.heappush(minHeap, (newDist, neighborNode))

    return distances