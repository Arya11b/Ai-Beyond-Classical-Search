import  random
import matplotlib.pyplot as plt
class GeneticAlgrithm:
    def __init__(self,chromosomeNo):
        self.gen = 0
        self.plot_data_best = []
        self.plot_data_mid = []
        self.plot_data_worst = []
        self.chromosomes = []
        self.sums = []
        self.fitness = []
        self.chromosomeNo = chromosomeNo
        self.sums = [0 for x in range(chromosomeNo)]
        for i in range(0,chromosomeNo):
            a = random.randint(0,40)
            b = random.randint(0,40)
            c = random.randint(0,40)
            d = random.randint(0,40)
            self.chromosomes.append([a, b, c, d])
    def evaluate(self):
            for i in range(self.chromosomeNo):
                e = Equation(*self.chromosomes[i])
                self.sums[i] = e.sum()
                if e.isGoalState():
                    return i
            return -1
    def select(self):
        total = 0
        self.fitness = [1/(1+abs(s)) for s in self.sums]
        self.calculateGen()
        for i in range(self.chromosomeNo): total += self.fitness[i]
        p = [f/total for f in self.fitness]
        c = [p[0]]
        r = [random.uniform(0,1) for x in range(self.chromosomeNo)]
        for i in range(1,len(p)): c.append(p[i] + c[i-1])
        oldChromosomes = self.chromosomes
        for i in range(len(c)-1):
            for j in range(len(r)):
                if (r[j] >= c[i] and r[j] < c[i+1]):
                    self.chromosomes[i + 1] = oldChromosomes[j]
    def crossover(self,pc):
        oldChromosomes = self.chromosomes
        parents = []
        r = [random.uniform(0,1) for x in range(self.chromosomeNo)]
        for k in range(self.chromosomeNo):
            if r[k] < pc:
                parents.append(k)
        for i in range(len(parents)):
            c = random.randint(1,3)
            self.chromosomes[parents[i]] = oldChromosomes[parents[i]][:c] + oldChromosomes[parents[(i+1)%len(parents)]][c:]

    def mutate(self,pm):
        total_gen = self.chromosomeNo * 4
        mutationNo = int(pm * total_gen)
        for i in range (mutationNo): self.chromosomes[random.randint(0,self.chromosomeNo-1)][random.randint(0,3)] = random.randint(0,40)
    def calculateGen(self):
        self.gen += 1
        self.fitness = [1/(1+abs(s)) for s in self.sums]
        sortedC = [x for _, x in sorted(zip(self.fitness, self.chromosomes))]
        bestIndex = self.chromosomes.index(sortedC[-1])
        worstIndex = self.chromosomes.index(sortedC[0])
        midIndex = self.chromosomes.index(sortedC[int(len(sortedC) / 2)])
        print("Generation ", self.gen, " : best fit: ", self.chromosomes[bestIndex], "mid fit: ",
              self.chromosomes[midIndex], "worst fit: ", self.chromosomes[worstIndex])
        self.plot_data_best.append(abs(self.sums[bestIndex]))
        self.plot_data_worst.append(abs(self.sums[worstIndex]))
        self.plot_data_mid.append(abs(self.sums[midIndex]))
    def solve(self):
        e = self.evaluate()
        while e == -1:
            self.select()
            self.crossover(0.25)
            self.mutate(0.2)
            e = self.evaluate()
        print("final Values:", self.chromosomes[e])


class Equation:
    def __init__(self,a,b,c,d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
    def sum(self): return self.a + 2 * self.b + 3 * self.c + 4 * self.d - 40
    def isGoalState(self): return self.a + 2 * self.b + 3 * self.c + 4 * self.d - 40 == 0
g = GeneticAlgrithm(20)
g.solve()
# plt.figure(figsize=(12,9))
plt.plot([x for x in range(len(g.plot_data_best))],g.plot_data_best,color = "green",linewidth = 0.4)#, color = "green")
plt.plot([x for x in range(len(g.plot_data_worst))],g.plot_data_worst,color = "red",linewidth = 0.4)#, color = "green")
plt.plot([x for x in range(len(g.plot_data_mid))],g.plot_data_mid,color = "blue",linewidth = 0.4)#, color = "green")
plt.axis([0, g.gen, 0, 500])
plt.ylabel('Equation Result')
plt.xlabel('generation index')
plt.show()
