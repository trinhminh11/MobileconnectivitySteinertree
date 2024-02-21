from pack1 import *
import pack1.Method as Method
import random
import timeit
import os

cur_path = os.path.dirname(__file__)

def import_data(inp):
	PointSet = []

	with open(inp, 'r') as f:

		W, L = map(int, f.readline().split())

		base = Point(*map(int, f.readline().split()))

		carNum = int(f.readline())

		R = float(f.readline())

		periodCount = int(f.readline())


		n = carNum * periodCount


		k = int(periodCount * 16 / (R * R))
		
		if k > n:
			k = int(n/2)
		
		k = max(k, 1)

		for i in range(n):
			PointSet.append(Point(*map(float, f.readline().split())))
		
		PointSet.append(base)
	
	return W, L, R, PointSet, k


class Main:
	def __init__(self, W, L, R, PointSet, k) -> None:
		self.W = W
		self.L = L
		self.R = R
		self.PointSet: list[Point] = PointSet[:-1]
		self.base = PointSet[-1]
		self.n = len(self.PointSet)

		self.k = k

		self.addedPoint: list[Point] = []
		self.SpanningSet: list[list[int]] = []
		self.SensorSet: list[Point] = []
		self.mt = Method


		self.EdgeSet: list[list[int]] = []

		self.ClusterSet: list[Cluster] = []
	
	def randomCluster(self):
		lst = [i for i in range(self.n)]

		random.shuffle(lst)

		for numRan in lst[:self.k]:
			self.ClusterSet.append(Cluster(self.PointSet[numRan]))
		
	
	def Clustering(self):
		oldCluster = [None] * self.n
		newCluster = [None] * self.n

		def compareOldNew():
			for i in range(self.n):
				if oldCluster[i] != newCluster[i]:
					return False
			return True
		
		while True:
			for i in range(self.n):
				MinDist = self.PointSet[i].dist(self.ClusterSet[0].getCentroid())
				indexOfCluster = 0

				for j in range(1, self.k):
					dst = self.PointSet[i].dist(self.ClusterSet[j].getCentroid())
					if (dst < MinDist):
						MinDist = dst
						indexOfCluster = j
				
				self.ClusterSet[indexOfCluster].add(self.PointSet[i])
				newCluster[i] = indexOfCluster
			
			if compareOldNew():
				break

			for i in range(self.n):
				oldCluster[i] = newCluster[i]
			
			for i in range(self.k):
				self.ClusterSet[i] = Cluster(self.ClusterSet[i].center())
		
	def addPoint(self, d1: Point, d2: Point):
		if d1.dist(d2) <= 2 * self.R:
			return
		
		d3 = Point(0, 0)
		dst = d1.dist(d2)

		deltaX = 2*self.R* abs(d2.x - d1.x)/dst
		deltaY = 2*self.R* abs(d2.y - d1.y)/dst

		if d1.x < d2.x:
			d3.x = (d1.x + deltaX)
		else:
			d3.x = (d1.x - deltaX)
			
		if d1.y < d2.y:
			d3.y = (d1.y + deltaY)
		else:
			d3.y = (d1.y - deltaY)
			
		self.addedPoint.append(d3)
		self.addPoint(d3,d2)
	
	def addPointOfCluster(self):
		pointOfThisCluster: list[Point] = []
		toAddedPointMin = []
		idAddedPoint = []
		connected = []

		for clus in range(self.k):
			pointOfThisCluster = self.ClusterSet[clus].returnList()
			pointcount = len(pointOfThisCluster)
			centroid = self.ClusterSet[clus].getCentroid()
			self.addedPoint.append(centroid)

			toAddedPointMin = [pointOfThisCluster[i].dist(centroid) for i in range(pointcount)]
			connected = [False] * pointcount
			idAddedPoint = [len(self.addedPoint) - 1] * pointcount
			connectedCount = 0

			while connectedCount < pointcount:
				kcMin = float('inf')
				idMin = -1
				for i in range(pointcount):
					if not connected[i] and toAddedPointMin[i] < kcMin:
						kcMin = toAddedPointMin[i]
						idMin = i
				
				if idMin == -1:
					print("Error")
					exit()

				connected[idMin] = True
				connectedCount += 1
				
				pointMin = pointOfThisCluster[idMin]
				idBegin = len(self.addedPoint)
				plusPoint = self.addedPoint[idAddedPoint[idMin]]

				self.addPoint(pointMin, plusPoint)

				for i in range(pointcount):
					if not connected[i]:
						for j in range(idBegin, len(self.addedPoint)):
							point = pointOfThisCluster[i]
							plusPoint = self.addedPoint[j]

							if point.dist(plusPoint) < toAddedPointMin[i]:
								toAddedPointMin[i] = point.dist(plusPoint)
								idAddedPoint[i] = j

	def Kruskal(self):
		self.EdgeSet.sort(key= lambda x: x[2])

		root = [i for i in range(self.k+1)]

		def getRoot(x):
			if root[x] == x:
				return x
			else:
				root[x] = getRoot(root[x])
				return root[x]

		for i in range(self.EdgeCount):
			idA = self.EdgeSet[i][0]
			idB = self.EdgeSet[i][1]
			p = getRoot(idA)
			q = getRoot(idB)

			if p == q:
				continue
			
			root[p] = q
			
			self.SpanningSet.append([idA, idB, 0])
	

	def SteinerTree(self):

		for i in range(self.k):
			self.SensorSet.append(self.ClusterSet[i].getCentroid())
		
		self.SensorSet.append(self.base)

		deleted = [False] * len(self.SpanningSet)

		for i in range(len(self.SpanningSet)):
			if deleted[i]:
				continue

			idChoosed = -1
			alphaMax = float('-inf')

			for j in range(len(self.SpanningSet)):
				if i == j or deleted[j]:
					continue

				isIntersects = False
				e1 = self.SpanningSet[i]
				e2 = self.SpanningSet[j]

				if e1[0] == e2[0]:
					d1 = e1[1]
					d3 = e2[1]
					d2 = e1[0]
					isIntersects = True
				if e1[1] == e2[1]:
					d1 = e1[0]
					d3 = e2[0]
					d2 = e1[1]
					isIntersects = True
				
				if e1[0] == e2[1]:
					d1 = e1[1] 
					d3 = e2[0] 
					d2 = e1[0] 
					isIntersects = True

				if e1[1] == e2[0]:
					d1 = e1[0] 
					d3 = e2[1] 
					d2 = e1[1] 
					isIntersects = True
				
				if not isIntersects:
					continue

				alpha = self.mt.cos(self.SensorSet[d1], self.SensorSet[d2], self.SensorSet[d3])

				if alpha > alphaMax:
					alphaMax = alpha
					idChoosed = j

			if idChoosed == -1:
				continue

			e2 = self.SpanningSet[idChoosed]
		
		for i, e in enumerate(self.SpanningSet):
			if not deleted[i]:
				self.addPoint(self.SensorSet[e[0]], self.SensorSet[e[1]])
		

	def connectCluster(self):
		for i in range(self.k+1):
			for j in range(i+1, self.k+1):
				if i < self.k:
					p1 = self.ClusterSet[i].getCentroid()
				else:
					p1 = self.base
				
				if j < self.k:
					p2 = self.ClusterSet[j].getCentroid()
				else:
					p2 = self.base
				
				self.EdgeSet.append([i, j, p1.dist(p2)])
		
		self.EdgeCount = len(self.EdgeSet)

	
	def solve(self):
		self.randomCluster()

		self.Clustering()

		self.addPointOfCluster()

		self.connectCluster()

		self.Kruskal()

		self.SteinerTree()
	
	def export_data(self, out):
		with open(out, "w") as f:
			for diem in self.PointSet:
				f.write(diem.toDecimalString() + "\n")

			f.write(self.base.toDecimalString() + "\n\n")

			for diem in self.addedPoint:
				f.write(diem.toCircle(self.R) + "\n")


def main():
	for i in range(1, 19):
		print("Test-Case:", i)


		path = cur_path + "/Testmip/Test" + str(i)

		W, L, R, Ps, k = import_data(path + ".inp")

		solver = Main(W, L, R, Ps, k)

		starttime = timeit.default_timer()

		solver.solve()

		endtime = timeit.default_timer()

		solver.export_data(path + ".out")

		print("ADDED =", len(solver.addedPoint))

		print("time =", endtime - starttime)

		print("--------------------")

if __name__ == "__main__":
	main()
