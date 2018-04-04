import random
import copy
import math
SIZE = 12
MIN = 3.1
class SimulatedAnnealing:
    nodes = []
    childs = []
    cost = []
    p = 1.0
    def __init__(self):
        n = random.randint(0,SIZE-1)
        init_array = []
        while n != 0:
            i = random.randint(0,SIZE-1)
            while i in init_array:
                i = random.randint(0,SIZE-1)
            init_array.append(i)
            n-=1
        initialState = GraphPartionProblem(init_array)
        self.addNode(initialState)
    def powerAnnealingMethod(self,step): return self.p * step if self.p > 0 else -1
    def linearAnnealingMethod(self,step): return self.p - step
    def exponentialAnnealingMethod(self,step): self.p -= 0.0002; return math.exp(1.0-1.0/self.p) if self.p >= 0 else -1
    def addNode(self,state):
        self.childs.append([])
        # self.visited.append(False)
        self.nodes.append(state.subNodes)
        self.cost.append(state.cost())
    def expand(self,currentNode):
        parent = GraphPartionProblem(self.nodes[currentNode])
        childTemp = []
        for i in range(0,2 * SIZE):
            child = copy.deepcopy(parent)
            child.doAction(i)
            if child.subNodes not in self.nodes:
                self.addNode(child)
                childTemp.append(len(self.nodes)-1)
        self.childs[currentNode] = childTemp
    def simulateAnnealing(self,method):
        print ("simulated Annealing...")
        currentNode = 0
        while (not GraphPartionProblem(self.nodes[currentNode]).isGoalState()):
            self.expand(currentNode)
            print ("sub node: ",self.nodes[currentNode]," Cost: ",self.cost[currentNode]," p:",self.p)
            currentNode = self.findNode(currentNode,method)
            print ("current Node: " , currentNode)
            if currentNode == -1:
                print ("did not found the right Answer exiting Now ...")
                break
        print ("final Partitions: ", self.nodes[currentNode] , [x for x in range(0,12) if x not in self.nodes[currentNode]],"cost: ",self.cost[currentNode])
        print ("complete nodes: ",self.nodes,"node count: ", len(self.nodes))
        print ("costs: ",self.cost)
    def annealingMethod(self,method):
        return {
            'linear': self.linearAnnealingMethod(0.005),
            'exponential': self.exponentialAnnealingMethod(0.005),
            'power':self.powerAnnealingMethod(0.5)
        }[method]
    def findNode(self,currentNode,method):
        seed = -1
        while self.p >= 0:
            if len(self.childs[currentNode]) > 0 :
                seed = random.choice(self.childs[currentNode])
            if self.cost[seed] < self.cost[currentNode]:
                self.p = self.annealingMethod(method)
                return seed
            elif random.uniform(0,1) < self.p:
                self.p = self.annealingMethod(method)
                return seed
        return seed
class GraphPartionProblem:
    nodes = []
    childs = []
    subNodes = []
    def __init__(self,subNodes):
        self.subNodes = []
        self.nodes = [x for x in range(0,SIZE)]
        self.childs = [[] for x in range(0,SIZE)]
        self.addEdge(0,1)
        self.addEdge(0,2)
        self.addEdge(1,2)
        self.addEdge(1,3)
        self.addEdge(1,4)
        self.addEdge(2,5)
        self.addEdge(3,6)
        self.addEdge(4,7)
        self.addEdge(4,5)
        self.addEdge(5,8)
        self.addEdge(6,7)
        self.addEdge(6,9)
        self.addEdge(6,10)
        self.addEdge(7,11)
        self.addEdge(7,8)
        self.addEdge(9,10)
        self.addEdge(10,11)
        self.subNodes = subNodes
    def isGoalState(self):
        return self.cost() < MIN
    def doAction(self,i):
        if i >= SIZE:
            if i-SIZE in self.subNodes:
                self.subNodes.remove(i-SIZE)
        elif i not in self.subNodes:
            self.subNodes.append(i)
    def addEdge(self,a,b): # adds a -> b
        self.childs[a].append(b)
        self.childs[b].append(a)
    def subGraphWeight(self,subNodes):
        weight = 0
        for i in subNodes:
            for c in self.childs[i]:
                if c in subNodes:
                    weight += 1
        return weight/2
    def joinedEdgesWeight(self):
        weight = 0
        for i in self.subNodes:
            for c in self.childs[i]:
                if c not in self.subNodes:
                    weight += 1
        return weight
    def subGraphWeightDifference(self):
        subNodes2 = [x for x in self.nodes if x not in self.subNodes]
        return abs(self.subGraphWeight(self.subNodes) - self.subGraphWeight(subNodes2))
    def cost(self):
        return self.subGraphWeightDifference() * 0.4 + self.joinedEdgesWeight()
s = SimulatedAnnealing()
s.simulateAnnealing('exponential')
# s.simulateAnnealing('linear')
# s.simulateAnnealing('power')