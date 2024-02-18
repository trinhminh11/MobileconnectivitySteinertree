from pack1 import *
import pack1.ToaDoMethod as ToaDoMethod
import os
import timeit

cur_path = os.path.dirname(__file__)

class Main:
	N_MAX = 5007
	BASE = None
	def __init__(self) -> None:
		self.mt = ToaDoMethod
		self.tapSensor: list[ToaDo] = []
		self.tapRelay: list[ToaDo] = []
		self.tapEdge: list[Edge] = []
		self.tapSpanning: list[Edge] = []
		self.tapSteiner: list[Edge] = []
		
		self.W, self.L = 0, 0
		self.BASE: ToaDo = None
		self.carNum, self.periodNum, self.toaDoNum = 0, 0, 0
		self.R = 0
		self.root = []
		self.adj: list[DanhSachDinhKe] = []
		self.visited = [False] * self.N_MAX
		self.truyVet = [0] * self.N_MAX
	
	def print(self, s):
		print(s)

	def docFile(self, inp):
		with open(inp, 'r') as f:

			self.W, self.L = map(int, f.readline().split())

			
			self.BASE = ToaDo(*map(int, f.readline().split()))

			carNum = int(f.readline())

			self.R = float(f.readline())

			periodNum = int(f.readline())

			self.toaDoNum = carNum * periodNum

			for i in range(carNum):
				for j in range(periodNum):
					self.tapSensor.append(ToaDo(*map(float, f.readline().split()), j))
			
			self.tapSensor.append(self.BASE)

			self.toaDoNum += 1

	def sortEdge(self):
		self.tapEdge.sort(key= lambda x: x.doDai)
	
	def getRoot(self, x):
		if self.root[x] == x:
			return x
		else:
			self.root[x] = self.getRoot(self.root[x])
			return self.root[x]
	
	def addRelay(self, d1: ToaDo, d2: ToaDo):
		R = self.R

		if d1.khoangCach(d2) <= 2 * R:
			return
		d3 = ToaDo(0, 0)
		kCach = d1.khoangCach(d2)
		deltaX = 2*R* abs(d2.getX() - d1.getX())/kCach;
		deltaY = 2*R* abs(d2.getY() - d1.getY())/kCach;
		if d1.getX() < d2.getX():
			d3.setX(d1.getX() + deltaX)
		else:
			d3.setX(d1.getX() - deltaX)
		if d1.getY() < d2.getY():
			d3.setY(d1.getY() + deltaY)
		else:
			d3.setY(d1.getY() - deltaY)
		self.tapRelay.append(d3)
		self.addRelay(d3,d2)

	def spanningTree(self):
		for i in range(len(self.tapSensor)):
			for j in range(i+1, len(self.tapSensor)):
				p1 = self.tapSensor[i]	
				p2 = self.tapSensor[j]	

				self.tapEdge.append(Edge(i, j, p1, p2, p1.khoangCach(p2)))
		
		self.sortEdge()
	
		self.root = [i for i in range(self.toaDoNum)]

		for e in self.tapEdge:
			idA = e.id1
			idB = e.id2

			p = self.getRoot(idA)
			q = self.getRoot(idB)
			if p == q:
				continue

			self.root[p] = q
			self.tapSpanning.append(e)
		

	def steinerTree(self):
		d1 = d2 = d3 = 0
		id1 = id2 = id3 = idSteiner = 0

		d1Choosed = ToaDo(0, 0)
		d2Choosed = ToaDo(0, 0)
		d3Choosed = ToaDo(0, 0)

		e1 = Edge(0, 0, d1Choosed, d1Choosed, 0)
		e2 = Edge(0, 0, d1Choosed, d1Choosed, 0)

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

			if self.mt.lessThan120(d1Choosed, d2Choosed, d3Choosed):
				steinerP = self.mt.diemSteiner(d1Choosed, d2Choosed, d3Choosed)

				kc1 = steinerP.khoangCach(d1Choosed)
				kc2 = steinerP.khoangCach(d2Choosed)
				kc3 = steinerP.khoangCach(d3Choosed)

				if kc1 < 2 * self.R or kc2 < 2 * self.R or kc3 < 2 * self.R:
					continue

				e1.isXoa = True
				e2.isXoa = True
				self.tapSensor.append(steinerP)


				idSteiner = len(self.tapSensor) - 1

				self.tapSpanning.append(Edge(id1, idSteiner, d1Choosed, steinerP, 0))
				self.tapSpanning.append(Edge(id2, idSteiner, d2Choosed, steinerP, 0))
				self.tapSpanning.append(Edge(id3, idSteiner, d3Choosed, steinerP, 0))

				self.tapRelay.append(steinerP)
		
		for e in self.tapSpanning:
			if not e.isXoa:
				self.tapSteiner.append(e)
		
		self.adj: list[DanhSachDinhKe] = [DanhSachDinhKe() for _ in range(len(self.tapSensor))]

		for e in self.tapSteiner:
			self.addRelay(e.point1, e.point2)
			self.adj[e.id1].push(e.id2)
			self.adj[e.id2].push(e.id1)



	def ghiFile(self, out):
		with open(out, 'w') as f:
			for p in self.tapRelay:
				f.write(f"(x-{p.x:.3f})^2 +(y-{p.y:.3f})^2 = {self.R*self.R:.3f}\n")

			for i in range(self.toaDoNum):
				f.write(self.tapSensor[i].toDecimalString() + "\n")
		
		print("ADDED =", len(self.tapRelay))
	
	def datRelay(self, u):
		if self.tapSensor[u].chuKy == -1:
			return
		
		self.tapRelay.append(self.tapSensor[u])

		self.tapSensor[u].chuKy = -1
	
	def truyVetBack(self, u):
		v = u
		ck = self.tapSensor[u].chuKy

		if ck == -1:
			return
		
		while v != self.toaDoNum - 1:
			v = self.truyVet[v]

			if self.tapSensor[v].chuKy != ck:
				self.datRelay(v)
	
	def dfs(self, u: int):
		if self.visited[u]:
			return
		
		self.visited[u] = True

		self.truyVetBack(u)

		for i in range(self.adj[u].size()):
			v = self.adj[u].get(i)
			if not self.visited[v]:
				self.truyVet[v] = u
				self.dfs(v)
		
	def dfsMethod(self):
		self.truyVet[self.toaDoNum-1] = -1

		for i in range(len(self.tapSensor)):
			self.visited[i] = False
		
		self.dfs(self.toaDoNum-1)

def main():
	for i in range(1, 19):
		print("Test-Case:", i)
		starttime = timeit.default_timer()

		x = Main()

		path = cur_path + "/Testnew/" + str(i)

		x.docFile(path + ".inp")
		x.spanningTree()
		x.steinerTree()
		x.dfsMethod()
		x.ghiFile(path + ".out")

		endtime = timeit.default_timer()

		print("time =", endtime - starttime)

		print("------------------------")



if __name__ == "__main__":
	main()