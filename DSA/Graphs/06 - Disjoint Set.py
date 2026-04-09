# Time - O(4 * alpha) | Space - O(n)
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

    def unionByRank(self, n1, n2):
        p1, p2 = self.findParent(n1), self.findParent(n2)

        if self.rank[p1] < self.rank[p2]:
            self.parent[p1] = p2
        elif self.rank[p2] < self.rank[p1]:
            self.parent[p2] = p1 
        else:
            self.parent[p2] = p1
            self.rank[p1] += 1