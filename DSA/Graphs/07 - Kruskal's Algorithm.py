
# Time - O(E log E) | Space - O(V + E)
def kruskal(n: int, edges: list[list[int]]) -> list[list[int]]:
    edges.sort(key=lambda x: x[-1])
    dsu = DSU(n)
    mst = []
    pathSum = 0
    for u, v, wt in edges:
        if dsu.findParent(u) == dsu.findParent(v):
            continue

        dsu.unionBySize(u, v)
        mst.append([u, v, wt])
        pathSum += wt
            
    return pathSum, mst

class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * (n + 1)
        self.size = [1] * (n + 1)

    def findParent(self, n):
        if self.parent[n] == n:
            return n

        self.parent[n] = self.findParent(self.parent[n])
        return self.parent[n]
    
    def unionBySize(self, n1, n2):
        p1, p2 = self.findParent(n1), self.findParent(n2)

        if self.size[p1] < self.size[p2]:
            self.parent[p1] = p2
            self.size[p2] += self.size[p1]
        else:
            self.parent[p2] = p1
            self.size[p1] += self.size[p2]