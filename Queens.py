import copy
import random
SIZE = 8
class HillClimbing:
    nodes = []
    conflictValues = []
    # visited = []
    childs = []
    def __init__(self):
        initialState = Problem([[x,random.randint(0,SIZE -1)] for x in range(0,SIZE)])
        # initialState = Problem([[0,3],[1,5],[2,7],[3,1],[4,6],[5,0],[6,2],[7,4]])
        self.addNode(initialState)
    def addNode(self,state):
        self.childs.append([])
        # self.visited.append(False)
        self.nodes.append(state.queen)
        self.conflictValues.append(state.findConflicts())
    def expand(self,currentNode):
        print ("expanding node ",currentNode," :")
        parent = Problem(self.nodes[currentNode])
        childTemp = []
        for i in range(SIZE * SIZE - SIZE):
            child = copy.deepcopy(parent)
            child.doAction(i)
            if child.queen not in self.nodes:
            # if child.queen != self.nodes[currentNode]:
                self.addNode(child)
                childTemp.append(len(self.nodes)-1)
        self.childs[currentNode] = childTemp
    def firstChoiceNode(self,currentNode):
        minIndex = []
        min =  self.conflictValues[currentNode]
        for i in range(0,len(self.childs[currentNode])):
            seed = random.randint(0, len(self.childs[currentNode]) - 1)
            while self.childs[currentNode][seed] in minIndex:
                seed = random.randint(0, len(self.childs[currentNode]) - 1)
            minIndex.append(self.childs[currentNode][seed])
            if self.conflictValues[self.childs[currentNode][seed]] <= min: #and not self.visited[index]:
                return self.childs[currentNode][seed]
        return -1
    def findRandomNode(self,currentNode):
        minIndex = []
        min =  self.conflictValues[currentNode]
        for i in self.childs[currentNode]:
            if self.conflictValues[i] <= min: #and not self.visited[index]:
                minIndex.append(i)
        if len(minIndex) == 0:
            return -1
        seed = random.randint(0,len(minIndex)-1)
        return minIndex[seed]
    def findNode(self,currentNode):
        min = self.conflictValues[currentNode]
        minIndex = -1
        # index = self.nodes.index(node)
        for i in self.childs[currentNode]:
            if self.conflictValues[i] <= min: #and not self.visited[index]:
                min = self.conflictValues[i]
                minIndex = i
        return minIndex
    def normalHillClimbing(self):
        print ("Normal Hill climbing...")
        currentNode = 0
        while (not Problem(self.nodes[currentNode]).isGoalState()):
            self.expand(currentNode)
            print ("queen positions: ",self.nodes[currentNode]," Conflicting Values: ",self.conflictValues[currentNode])
            currentNode = self.findNode(currentNode)
            if currentNode == -1:
                print ("did not found the right Answer exiting Now ...")
                break
        print ("final positions in node", currentNode ,": ", self.nodes[currentNode]," Conflicting Values: ",self.conflictValues[currentNode])
        print ("complete nodes: ",self.nodes,"node count: ", len(self.nodes))
    def randomRestartHillClimbing(self,n):
        print ("random Restart Hill climbing...")
        observedNodes = []
        currentNode = 0
        while True:
            self.expand(currentNode)
            print ("queen positions: ",self.nodes[currentNode]," Conflicting Values: ",self.conflictValues[currentNode])
            if Problem(self.nodes[currentNode]).isGoalState():
                print ("final positions in node", currentNode, ": ", self.nodes[currentNode], " Conflicting Values: ", self.conflictValues[currentNode])
                break
            currentNode = self.findNode(currentNode)
            if currentNode == -1:
                currentNode = random.randint(1,len(self.nodes)-1)
                while currentNode in observedNodes:
                    currentNode = random.randint(1,len(self.nodes))
                observedNodes.append(currentNode)
            n -= 1
            if n == 0 :
                print ("did not found the right Answer exiting Now ...")
                break
    def stochasticHillClimbing(self):
        print ("Stochastic Hill climbing...")
        currentNode = 0
        while (not Problem(self.nodes[currentNode]).isGoalState()):
            self.expand(currentNode)
            print ("queen positions: ",self.nodes[currentNode]," Conflicting Values: ",self.conflictValues[currentNode])
            currentNode = self.findRandomNode(currentNode)
            if currentNode == -1:
                print ("did not found the right Answer exiting Now ...")
                break
        print ("final positions in node", currentNode ,": ", self.nodes[currentNode]," Conflicting Values: ",self.conflictValues[currentNode])
        print ("complete nodes: ",self.nodes,"node count: ", len(self.nodes))

    def firstChoiceHillClimbing(self):
        print ("first choice Hill climbing...")
        currentNode = 0
        while (not Problem(self.nodes[currentNode]).isGoalState()):
            self.expand(currentNode)
            print ("queen positions: ",self.nodes[currentNode]," Conflicting Values: ",self.conflictValues[currentNode])
            currentNode = self.firstChoiceNode(currentNode)
            if currentNode == -1:
                print ("did not found the right Answer exiting Now ...")
                break
        print ("final positions in node", currentNode ,": ", self.nodes[currentNode]," Conflicting Values: ",self.conflictValues[currentNode])
        print ("complete nodes: ",self.nodes,"node count: ", len(self.nodes))

class Problem:
    queen = [[x,x] for x in range(0,SIZE)]
    conflicts = 0
    # def __init__(self):
    #     self.findConflicts()
    def __init__(self,queen):
        self.queen = queen
        self.findConflicts()
    def move(self,i,j):
        # print i,j
        self.queen[i][1] = (self.queen[i][1] + j) % SIZE
    def doAction(self,i):
        steps = i % SIZE
        index = int(i / SIZE)
        self.move(index,steps)
    def findConflicts(self):
        self.conflicts = 0
        for i in self.queen:
            for j in self.queen[self.queen.index(i)+1:]:
                if i[0] == j[0] or i[1] == j[1] or abs(i[0] - j[0]) == abs(i[1] - j[1]):
                    self.conflicts += 1
        return self.conflicts
    def isGoalState(self):
        return True if self.conflicts == 0 else False

h = HillClimbing()
# h.normalHillClimbing()
# h.stochasticHillClimbing()
# h.firstChoiceHillClimbing()
# h.randomRestartHillClimbing(100) # -1 for infinite
