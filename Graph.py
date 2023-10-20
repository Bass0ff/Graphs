class Node:
    def __init__(self, name="noname"):
        self.neighbours = []    #
        self.name = name

    def __str__(self):
        return str(self.name)

    def addNeighbour(self, neighbour, weight):
        for N in self.neighbours:
            if N[0] == neighbour:
                return
        self.neighbours.append((neighbour, weight))

    def remNeighbour(self, neighbour):
        index = -1
        for i in range(len(self.neighbours)):
            if self.neighbours[i][0] == neighbour:
                index = i
                break
        if index >= 0:
            self.neighbours.pop(index)

class Way:
    def __init__(self, length = -1):
        self.nodes = []
        self.length = length

    def __str__(self):
        string = "("
        for i in self.nodes[:-1]:
            string += f"{i.name}, "
        string += f"{self.nodes[-1]}): {self.length}"
        return string

class PriorityQueue:
    def __init__(self):
        self.nodes = []

    def pop(self):
        return self.nodes.pop(0)

    def push(self, node, mark, prevNode):
        if len(self.nodes):
            for it in range(len(self.nodes)):
                if mark < self.nodes[it][1]:
                    self.nodes.insert(it, (node, mark, prevNode))
                    return
            self.nodes.append((node, mark, prevNode))
        else:
            self.nodes.append((node, mark, prevNode))

    def empty(self):
        if self.nodes:
            return False
        else:
            return True

    def __str__(self):
        string = ""
        for i in self.nodes:
            string += f"{i[0]}:{i[1]}; "
        return string

class Graph:
    def __init__(self):
        self.nodes = []
        self.cur = -1

    def __str__(self):
        string = ""
        for i in self.nodes:
            string += f"{str(i)}, "
        return string

    def addNode(self, node):
        if not node in self.nodes:
            self.nodes.append(node)

    def remNode(self, remnode):
        if remnode in self.nodes:
            for node in self.nodes:
                node.remNeighbour(remnode)
            self.nodes.remove(remnode)

    def addEdge(self, begin, end, weight=1, bidir = False):
        if begin in self.nodes and end in self.nodes:
            begin.addNeighbour(end, weight)
            if bidir:
                end.addNeighbour(begin, weight)

    def remEdge(self, begin, end):
        if begin in self.nodes and end in self.nodes:
            begin.remNeighbour(end)

    def wideStroll(self, begin=-1):
        if begin == -1:
            begin = self.nodes[0]
        queue = [begin]
        for node in queue:
            for neigh in node.neighbours:
                queue.append(neigh[0])
        return queue

    def depthStroll(self, begin=-1):
        if begin == -1:
            begin = self.nodes[0]
        stack = [begin]
        visited = []
        while stack:
            cur = stack.pop(-1)
            visited.append(cur)
            for neigh in cur.neighbours[::-1]:
                stack.append(neigh[0])
        return visited

    def Dijkstra(self, begin, end):
        #print(" //START ALGORITHM.")
        nodes = PriorityQueue()
        nodes.push(begin, 0, 0)
        #print(f"    {nodes}")
        visited = {}
        while not nodes.empty():
            #print("\n NEW ITERATION")
            cur = nodes.pop()   #Сам нод, его расстояние и его предшественник достаются из очереди
            #print(f" {cur[0].name}, {cur[1]}, {str(cur[2])}")
            if visited.get(cur[0]): #Если такой уже посещался
                if cur[1] < visited[cur[0]][0]: #Если новый путь короче старого
                    visited[cur[0]] = (cur[1], cur[2])  #Запоминаем новый путь
            else: #Если же этот нод впервые видим
                visited[cur[0]] = (cur[1], cur[2]) #Запоминаем хоть какой-нибудь путь
                
            if end == cur[0]:   #Если добрались до точки назначения
                #print(" REACHED DESTINATION!")
                #print("\n //END ALGORITHM")
                return unroll(visited, begin, end)#Собираем из узлов путь и возвращаем его
            for neigh in cur[0].neighbours: #Иначе, вносим в список всех соседей этого узла.
                weight = neigh[1]+cur[1]    #Вес = предыдущий путь + вес следующего узла
                if not visited.get(neigh[0]): 
                    nodes.push(neigh[0], weight, cur[0])
                    #print(f"    Added node: {neigh[0]}, {weight}, {cur[0]}")
            #print(f"    QUEUE:({nodes})")
        return Way()

def unroll(visited, begin, cur):
    way = Way()
    way.length = visited.get(cur)[0]
    while cur != begin:
        way.nodes.insert(0, cur)
        cur = visited[cur][1]
    way.nodes.insert(0, begin)
    return way
        
                
        
#print("PRIORITY QUEUE TEST")     
#a = PriorityQueue()
#a.push(2, 2, 1)
#a.push(1,3, 2)
#a.push(5,5, 3)
#print(a)
#a.push(4, 4, 4)
#print(a)
#print(a.pop())
#print(a)

#print()
#print("GRAPH TEST")
#nodes = [Node(i) for i in range(7)]
#G = Graph()
#for i in range(7):
#    G.addNode(nodes[i])
#G.addEdge(nodes[0], nodes[1])
#G.addEdge(nodes[0], nodes[2])
#G.addEdge(nodes[1], nodes[3])
#G.addEdge(nodes[1], nodes[4])
#G.addEdge(nodes[2], nodes[5])
#G.addEdge(nodes[2], nodes[6])
#graph = G.wideStroll()
#for i in graph:
#    print(i.name)
    
#print()

#graph = G.depthStroll()
#for i in graph:
#    print(i.name)

print()
print("DIJKSTRA TEST")
nodes = [Node(i) for i in range(5)]
dGraph = Graph()
for i in range(5):
    dGraph.addNode(nodes[i])
dGraph.addEdge(nodes[0], nodes[4], 100)
dGraph.addEdge(nodes[0], nodes[1], 10)
dGraph.addEdge(nodes[0], nodes[3], 30)
dGraph.addEdge(nodes[1], nodes[2], 50)
dGraph.addEdge(nodes[2], nodes[4], 10)
dGraph.addEdge(nodes[3], nodes[2], 20)
dGraph.addEdge(nodes[3], nodes[4], 60)
print(dGraph)
print("По условиям задачи и с учётом нумерации ответ должен быть: 0 3 2 4 - 60")
way = dGraph.Dijkstra(nodes[0], nodes[4])
print(way)

print()
print("DIJKSTRA TEST 2")
nodes = [Node(i) for i in range(8)]
dGraph = Graph()
for i in range(8):
    dGraph.addNode(nodes[i])
dGraph.addEdge(nodes[0], nodes[1], 5, True)
dGraph.addEdge(nodes[0], nodes[3], 4, True)
dGraph.addEdge(nodes[1], nodes[2], 3, True)
dGraph.addEdge(nodes[1], nodes[4], 1, True)
dGraph.addEdge(nodes[2], nodes[5], 5, True)
dGraph.addEdge(nodes[2], nodes[7], 4, True)
dGraph.addEdge(nodes[3], nodes[4], 3, True)
dGraph.addEdge(nodes[4], nodes[5], 9, True)
dGraph.addEdge(nodes[4], nodes[6], 2, True)
dGraph.addEdge(nodes[5], nodes[7], 1, True)
dGraph.addEdge(nodes[6], nodes[7], 2, True)
print(dGraph)
print("По условиям задачи и с учётом нумерации ответ должен быть: 0 1 4 6 7 5 - 11")
way = dGraph.Dijkstra(nodes[0], nodes[5])
print(way)  #Должен выдать: 0 1 4 6 7 5
