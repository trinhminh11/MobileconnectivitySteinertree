from pack1 import *
import pack1.SteinerCalculator as SteinerCalculator
import random
import timeit
import os

cur_path = os.path.dirname(__file__)

class Main:
	N_MAX = 2000
	INVALID = -1
	def __init__(self) -> None:
		self.addedPoint: list[ToaDo] = []
		self.tapSpanning: list[CanhNoi] = []
		self.tapSensor: list[ToaDo] = []
		self.mt = SteinerCalculator

		self.base: ToaDo = None
		self.width = self.length = self.carCount = self.periodCount = 0

		self.tapCanh: list[CanhNoi] = []

		self.tapCanhCount = 0
		self.root = []
		self.R = 0
		self.n = self.k = 0

		self.tapDiem: list[ToaDo] = []
		self.tapCluster: list[Cluster] = []
		self.newCluster = [0] * self.N_MAX
		self.oldCluster = [0] * self.N_MAX
	
	def nhapDuLieu(self, inp):
		with open(inp, 'r') as f:

			self.W, self.L = map(int, f.readline().split())

			self.base = ToaDo(*map(int, f.readline().split()))

			self.carNum = int(f.readline())

			self.R = float(f.readline())

			self.periodCount = int(f.readline())


			self.n = self.carNum * self.periodCount


			self.k = int(self.periodCount * 16 / (self.R * self.R))

			
			if self.k > self.n:
				self.k = int(self.n/2)
			

			for i in range(self.n):
				self.tapDiem.append(ToaDo(*map(float, f.readline().split())))
			

	def inDuLieu(self, out):
		with open(out, "w") as f:
			for diem in self.tapDiem:
				f.write(diem.toDecimalString() + "\n")

			f.write(self.base.toDecimalString() + "\n\n")

			for diem in self.addedPoint:
				f.write(diem.toCircle(self.R) + "\n")
		
		print(len(self.addedPoint), "points added")


	def randomCum(self):
		numMax = self.n-1
		numMin = 0

		duocChon = [False] * self.n

		for i in range(self.k):
			while True:
				numRan = random.randint(numMin, numMax)
				if not duocChon[numRan]:
					break

			duocChon[numRan] = True

			self.tapCluster.append(Cluster(self.tapDiem[numRan]))
		
	
	def newSameOld(self):
		for i in range(self.n):
			if self.oldCluster[i] != self.newCluster[i]:
				return False
		
		return True

	def phanCum(self):
		done = False
		for i in range(self.n):
			self.oldCluster[i] = self.INVALID
		
		while not done:
			for i in range(self.n):
				kCachMin = self.tapDiem[i].khoangCach(self.tapCluster[0].getCentroid())
				indexOfCluster = 0

				for j in range(1, self.k):
					kCach = self.tapDiem[i].khoangCach(self.tapCluster[j].getCentroid())
					if (kCach < kCachMin):
						kCachMin = kCach
						indexOfCluster = j
				
				self.tapCluster[indexOfCluster].add(self.tapDiem[i])
				self.newCluster[i] = indexOfCluster
			
			if self.newSameOld():
				done = True
				break

			for i in range(self.n):
				self.oldCluster[i] = self.newCluster[i]
			
			for i in range(self.k):
				self.tapCluster[i] = Cluster(self.tapCluster[i].center())
		
	def addPoint(self, d1: ToaDo, d2: ToaDo):
		if d1.khoangCach(d2) <= 2 * self.R:
			return
		
		d3 = ToaDo(0, 0)
		kCach = d1.khoangCach(d2)
		deltaX = 2*self.R* abs(d2.getX() - d1.getX())/kCach;
		deltaY = 2*self.R* abs(d2.getY() - d1.getY())/kCach;
		if d1.getX() < d2.getX():
			d3.setX(d1.getX() + deltaX)
		else:
			d3.setX(d1.getX() - deltaX)
		if d1.getY() < d2.getY():
			d3.setY(d1.getY() + deltaY)
		else:
			d3.setY(d1.getY() - deltaY)
			
		self.addedPoint.append(d3)
		self.addPoint(d3,d2)
	
	def addPointOfCluster(self):
		pointOfThisCluster: list[ToaDo] = []
		toAddedPointMin = []
		idAddedPoint = []
		connected = []

		for clus in range(self.k):
			pointOfThisCluster = self.tapCluster[clus].returnList()
			pointcount = len(pointOfThisCluster)
			centroid = self.tapCluster[clus].getCentroid()
			self.addedPoint.append(centroid)

			toAddedPointMin = [pointOfThisCluster[i].khoangCach(centroid) for i in range(pointcount)]
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

							if point.khoangCach(plusPoint) < toAddedPointMin[i]:
								toAddedPointMin[i] = point.khoangCach(plusPoint)
								idAddedPoint[i] = j

	def sortTapCanh(self):
		self.tapCanh.sort(key= lambda x: x.getLength())
	
	def getRoot(self, x):
		if self.root[x] == x:
			return x
		else:
			self.root[x] = self.getRoot(self.root[x])
			return self.root[x]
	
	def buildCayKhung(self):
		self.root = [i for i in range(self.k+1)]

		for i in range(self.tapCanhCount):
			idA = self.tapCanh[i].id1
			idB = self.tapCanh[i].id2
			p = self.getRoot(idA)
			q = self.getRoot(idB)
			if p == q:
				continue
			self.root[p] = q

			if idA < self.k:
				p1 = self.tapCluster[idA].getCentroid()
			else:
				p1 = self.base
			
			if idB < self.k:
				p2 = self.tapCluster[idB].getCentroid()
			else:
				p2 = self.base
			
			self.tapSpanning.append(CanhNoi(idA, idB, 0))
	

	def steinerTree(self):

		for i in range(self.k):
			self.tapSensor.append(self.tapCluster[i].getCentroid())
		
		self.tapSensor.append(self.base)

		d1 = d2 = d3 = 0


		e1 = CanhNoi(0, 0, 0)
		e2 = CanhNoi(0, 0, 0)

		for i in range(len(self.tapSpanning)):
			if self.tapSpanning[i].isXoa:
				continue

			idCanh = -1
			alphaMax = float('-inf')

			for j in range(len(self.tapSpanning)):
				if i == j or self.tapSpanning[j].isXoa:
					continue

				giaoNhau = False
				e1 = self.tapSpanning[i]
				e2 = self.tapSpanning[j]

				if e1.id1 == e2.id1:
					d1 = e1.id2
					d3 = e2.id2
					d2 = e1.id1
					giaoNhau = True
				if e1.id2 == e2.id2:
					d1 = e1.id1
					d3 = e2.id1
					d2 = e1.id2
					giaoNhau = True
				
				if (e1.id1 == e2.id2):
					d1 = e1.id2 
					d3 = e2.id1 
					d2 = e1.id1 
					giaoNhau = True
				if (e1.id2 == e2.id1):
					d1 = e1.id1 
					d3 = e2.id2 
					d2 = e1.id2 
					giaoNhau = True
				
				if not giaoNhau:
					continue

				alpha = self.mt.cosGocGiua(self.tapSensor[d1], self.tapSensor[d2], self.tapSensor[d3])

				if alpha > alphaMax:
					alphaMax = alpha
					idCanh = j
					d1Choosed = self.tapSensor[d1]
					d2Choosed = self.tapSensor[d2]
					d3Choosed = self.tapSensor[d3]
					id1 = d1
					id2 = d2
					id3 = d3

			if idCanh == -1:
				continue

			e2 = self.tapSpanning[idCanh]

		
		for e in self.tapSpanning:
			if not e.isXoa:
				self.addPoint(self.tapSensor[e.id1], self.tapSensor[e.id2])

	def connectCluster(self):
		for i in range(self.k+1):
			for j in range(i+1, self.k+1):
				if i < self.k:
					p1 = self.tapCluster[i].getCentroid()
				else:
					p1 = self.base
				
				if j < self.k:
					p2 = self.tapCluster[j].getCentroid()
				else:
					p2 = self.base
				
				
				self.tapCanh.append(CanhNoi(i, j, p1.khoangCach(p2)))
		
		self.tapCanhCount = len(self.tapCanh)

		self.sortTapCanh()

		self.buildCayKhung()

		self.steinerTree()


def main():
	for i in range(1, 19):
		print("Test-Case:", i)
		x = Main()

		starttime = timeit.default_timer()

		path = cur_path + "/Testmip/Test" + str(i)

		x.nhapDuLieu(path + ".inp")
		x.randomCum()
		x.phanCum()
		x.addPointOfCluster()
		x.connectCluster()
		x.inDuLieu(path + ".out")
		endtime = timeit.default_timer()

		print("time =", endtime - starttime)

		print("--------------------")

if __name__ == "__main__":
	main()