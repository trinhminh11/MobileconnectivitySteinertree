from pack1 import *
import pack1.Method as Method
import os
import timeit

cur_path = os.path.dirname(__file__)

def import_data(inp):
	SensorSet = []
	with open(inp, 'r') as f:

		W, L = map(int, f.readline().split())

		BASE = Point(*map(int, f.readline().split()))

		carNum = int(f.readline())

		R = float(f.readline())

		periodNum = int(f.readline())


		for i in range(carNum):
			for j in range(periodNum):
				SensorSet.append(Point(*map(float, f.readline().split()), j))
		
		SensorSet.append(BASE)

	return W, L, R, SensorSet

class Solver:
	N_MAX = 5007
	def __init__(self, W, L, R, SensorSet) -> None:
		self.W = W
		self.L = L
		self.R = R
		self.n = len(SensorSet)
		self.SensorSet: list[Point] = SensorSet
		self.RelaySet: list[Point] = []
		self.EdgeSet: list[Edge] = []
		self.SteinerSet: list[Edge] = []

	def Kruskal(self):
		root = [i for i in range(self.n)]
		Edges = []

		def getRoot(x):
			if root[x] == x:
				return x
			else:
				root[x] = getRoot(root[x])
				return root[x]
		
		for i in range(self.n):
			for j in range(i+1, self.n):
				p1 = self.SensorSet[i]	
				p2 = self.SensorSet[j]	

				Edges.append([i, j, p1.dist(p2)])
		
		Edges.sort(key=lambda x: x[2])
		
		for e in Edges:
			idA = e[0]
			idB = e[1]

			p = getRoot(idA)
			q = getRoot(idB)
			if p == q:
				continue

			root[p] = q

			self.EdgeSet.append(e[:-1])
	
	def addRelay(self, d1: Point, d2: Point):
		R = self.R

		if d1.dist(d2) <= 2 * R:
			return
		
		d3 = Point(0, 0)

		dst = d1.dist(d2)
		deltaX = 2*R* abs(d2.x - d1.x)/dst;
		deltaY = 2*R* abs(d2.y - d1.y)/dst;
		if d1.x < d2.x:
			d3.x = (d1.x + deltaX)
		else:
			d3.x = (d1.x - deltaX)
		if d1.y < d2.y:
			d3.y = (d1.y + deltaY)
		else:
			d3.y = (d1.y - deltaY)

		self.RelaySet.append(d3)
		self.addRelay(d3, d2)

	def SteinerTree(self):
		d1 = d2 = d3 = 0
		id1 = id2 = id3 = idSteiner = 0

		d1Choosed = Point(0, 0)
		d2Choosed = Point(0, 0)
		d3Choosed = Point(0, 0)

		e1 = [0, 0, 0]
		e2 = [0, 0, 0]

		deleted = [False] * len(self.EdgeSet)

		for i in range(len(self.EdgeSet)):
			if deleted[i]:
				continue

			idChoosed = -1
			alphaMax = float('-inf')

			for j in range(len(self.EdgeSet)):
				if i == j or deleted[j]:
					continue

				isIntersect = False
				e1 = self.EdgeSet[i]
				e2 = self.EdgeSet[j]

				if e1[0] == e2[0]:
					d1 = e1[1]
					d2 = e1[0]
					d3 = e2[1]
					isIntersect = True

				if e1[1] == e2[1]:
					d1 = e1[0]
					d2 = e1[1]
					d3 = e2[0]
					isIntersect = True
				
				if (e1[0] == e2[1]):
					d1 = e1[1] 
					d2 = e1[0] 
					d3 = e2[0] 
					isIntersect = True

				if (e1[1] == e2[0]):
					d1 = e1[0] 
					d2 = e1[1] 
					d3 = e2[1] 
					isIntersect = True
				
				if not isIntersect:
					continue

				alpha = Method.cos(self.SensorSet[d1], self.SensorSet[d2], self.SensorSet[d3])

				if alpha > alphaMax:
					alphaMax = alpha
					idChoosed = j
					d1Choosed = self.SensorSet[d1]
					d2Choosed = self.SensorSet[d2]
					d3Choosed = self.SensorSet[d3]
					id1 = d1
					id2 = d2
					id3 = d3

			if idChoosed == -1:
				continue
			

			if Method.lessThan120(d1Choosed, d2Choosed, d3Choosed):
				steinerP = Method.getSteinerPoint(d1Choosed, d2Choosed, d3Choosed)

				dst1 = steinerP.dist(d1Choosed)
				dst2 = steinerP.dist(d2Choosed)
				dst3 = steinerP.dist(d3Choosed)

				if dst1 < 2 * self.R or dst2 < 2 * self.R or dst3 < 2 * self.R:
					continue

				deleted[i] = True
				deleted[idChoosed] = True
				self.SensorSet.append(steinerP)


				idSteiner = len(self.SensorSet) - 1

				self.EdgeSet.append([id1, idSteiner])
				self.EdgeSet.append([id2, idSteiner])
				self.EdgeSet.append([id3, idSteiner])

				deleted += [False] * 3

				self.RelaySet.append(steinerP)
		
		for i in range(len(self.EdgeSet)):
			if not deleted[i]:
				self.SteinerSet.append(self.EdgeSet[i])
		
		self.AdjSet: list[list[int]] = [[] for _ in range(len(self.SensorSet))]

		for e in self.SteinerSet:
			self.addRelay(self.SensorSet[e[0]], self.SensorSet[e[1]])
			self.AdjSet[e[0]].append(e[1])
			self.AdjSet[e[1]].append(e[0])		
	
	def putRelay(self, u):
		if self.SensorSet[u].cycle == -1:
			return
		
		self.RelaySet.append(self.SensorSet[u])

		self.SensorSet[u].cycle = -1
	
	def TraceBack(self, u):
		v = u
		cycle = self.SensorSet[u].cycle

		if cycle == -1:
			return
		
		while v != self.n - 1:
			v = self.Trace[v]

			if self.SensorSet[v].cycle != cycle:
				self.putRelay(v)
	
	def DFS(self, u: int):
		if self.visited[u]:
			return
		
		self.visited[u] = True

		self.TraceBack(u)

		for i in range(len(self.AdjSet[u])):
			v = self.AdjSet[u][i]
			if not self.visited[v]:
				self.Trace[v] = u
				self.DFS(v)
		
	def DFSMethod(self):
		self.Trace = [False] * len(self.SensorSet)
		self.visited = [False] * len(self.SensorSet)
		self.Trace[self.n-1] = -1

		self.DFS(self.n-1)
	
	def solve(self):

		self.Kruskal()
		self.SteinerTree()
		self.DFSMethod()

	def export_data(self, out):
		with open(out, 'w') as f:
			for p in self.RelaySet:
				f.write(f"(x-{p.x:.3f})^2 +(y-{p.y:.3f})^2 = {self.R*self.R:.3f}\n")

			for i in range(self.n):
				f.write(self.SensorSet[i].toDecimalString() + "\n")

def main():
	for i in range(1, 19):
		print("Test-Case:", i)


		path = cur_path + "/Testmip/Test" + str(i)

		W, L, R, Ss = import_data(path + ".inp")

		solver = Solver(W, L, R, Ss)

		starttime = timeit.default_timer()
		solver.solve()
		endtime = timeit.default_timer()

		solver.export_data(path + ".out")

		print("ADDED =", len(solver.RelaySet))

		print("time =", endtime - starttime)

		print("------------------------")



if __name__ == "__main__":
	main()
