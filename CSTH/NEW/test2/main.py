from pack1 import *
import pack1.ToaDoMethod as ToaDoMethod

import timeit

class Main:
	fw = None 
	N_MAX = 5000

	numIter = 0
	root = []

	W, L = None, None

	def __init__(self) -> None:
		self.tapGiao1: list[Sensor] = []
		self.tapSensor: list[ToaDo] = []
		self.tapRelay: list[ToaDo] = []

		self.tapEdge: list[Edge] = []

		self.tapAdj: list[Adjacent] = []

		self.radius = 0
		self.n = 0
		self.relayNum = 0

		self.tapDiem: list[ToaDo] = [None] * self.N_MAX
		self.mark = [[False for _ in range(self.N_MAX)] for _ in range(self.N_MAX)]
		self.covered = [False] * self.N_MAX
	
	def giaoDiem(self, p1: ToaDo, p2: ToaDo, radius, id):
		x1, x2 = p1.getX(), p2.getX()
		y1, y2 = p1.getY(), p2.getY()

		xCenter = (x1 + x2)/2
		yCenter = (y1 + y2)/2
		distance = p1.khoangCach(p2)

		if y1 != y2:
			heSo = (x1-x2) / (y2-y1)
			xRes = xCenter + ( (radius * radius - distance * distance/4) / (1 + heSo * heSo) ) ** .5
			yRes = heSo * (xRes - xCenter) + yCenter
		else:
			xRes = xCenter
			yRes = yCenter + (radius * radius - distance * distance/4) **.5
		
		if id == 2:
			xRes = 2 * xCenter - xRes
			yRes = 2 * yCenter - yRes
		
		return ToaDo(xRes, yRes)

	def nhapDuLieu(self, inp, out):
		self.fw = open(out, 'w')

		with open(inp, 'r') as f:

			print("Nhap")

			self.W, self.L = map(int, f.readline().split())

			for i in range(3000):
				for j in range(3000):
					self.mark[i][j] = False
			
			BASE = ToaDo(*map(int, f.readline().split()))

			carNum = int(f.readline())

			self.radius = float(f.readline()) * 2

			periodNum = int(f.readline())
			self.n = carNum * periodNum

			for i in range(self.n):
				self.tapDiem[i] = ToaDo(*map(float, f.readline().split()))

			self.tapDiem[self.n] = BASE
			self.n += 1

			nFake = 0

			tapDiemFake: list[ToaDo] = [None] * self.n

			for i in range(self.n):
				isHave = False
				for j in range(i):
					if self.tapDiem[i] == self.tapDiem[j]:
						isHave = True
						break
				if isHave:
					continue
				tapDiemFake[nFake] = self.tapDiem[i]
				nFake += 1
			
			self.n = nFake

			for i in range(self.n):
				self.tapDiem[i] = tapDiemFake[i]
		

	def check(self, x, y, heso):
		for i in range(heso):
			for j in range(heso):
				if self.mark[x+i][y+j]:
					return False
				if y-j >= 0 and self.mark[x+i][y-j]:
					return False

				if x-i >= 0 and self.mark[x-i][y+j]:
					return False 

				if x-i >= 0 and y-j >= 0 and self.mark[x-i][y-j]:
					return False
		
		return True
	
	def timDiemGiao(self):
		for i in range(self.n):
			self.covered[i] = False

		for i in range(self.n):
			for j in range(i+1, self.n):
				p1 = self.tapDiem[i]
				p2 = self.tapDiem[j]

				if p1.khoangCach(p2) <= 2 * self.radius:
					gd = self.giaoDiem(p1, p2, self.radius, 1)
					
					roundX = round(gd.x)
					roundY = round(gd.y)

					if roundX >= 0 and roundY >= 0 and roundX <= self.W and roundY <= self.L and self.check(roundX, roundY, int(self.radius/20)):
						self.tapGiao1.append(Sensor(gd, self.radius))
						self.mark[roundX][roundY] = True
					
					gd = self.giaoDiem(p1, p2, self.radius, 2)
					roundX = round(gd.x)
					roundY = round(gd.y)

					if roundX >= 0 and roundY >= 0 and roundX <= self.W and roundY <= self.L and self.check(roundX, roundY, int(self.radius/20)):

						self.tapGiao1.append(Sensor(gd, self.radius))
						self.mark[roundX][roundY] = True
		
		for i in range(len(self.tapGiao1)):
			for j in range(self.n):
				if self.tapGiao1[i].isCover(self.tapDiem[j]):
					self.tapGiao1[i].add(j)
	
	def sapXep(self):
		self.tapGiao1.sort(key= lambda x: x.getTargetCount(), reverse= True)

	def bapPhu(self):
		self.sapXep()

		while True:
			coverMax = float('-inf')
			dGiaoMax = Sensor(ToaDo(0, 0), self.radius)

			for dGiao in self.tapGiao1:
				if dGiao.getTargetCount() > coverMax:
					coverMax = dGiao.getTargetCount()
					dGiaoMax = dGiao


			if coverMax <= 0:
				break

			self.fw.write(dGiaoMax.toCircle() + "\n")
			self.tapSensor.append(ToaDo(dGiaoMax.center))

			targetList = dGiaoMax.returnList()
			targetListCount = dGiaoMax.getTargetCount()

			for dGiao in self.tapGiao1:
				for i in range(targetListCount):
					dGiao.remove(targetList[i])
					self.covered[targetList[i]] = True
			

		for i in range(self.n):
			if not self.covered[i]:
				s = Sensor(self.tapDiem[i], self.radius)
				self.fw.write(s.toCircle() + "\n")
				self.tapSensor.append(ToaDo(s.center))
		
		self.relayNum = len(self.tapSensor)

	
	def inDuLieu(self):
		for i in range(self.n):
			self.fw.write(self.tapDiem[i].toDecimalString() + "\n")
	
	def sortEdge(self):
		self.tapEdge.sort(key= lambda x: x.getLength())

	def getRoot(self, x):
		if self.root[x] == x:
			return x
		else:
			self.root[x] = self.getRoot(self.root[x])
			return self.root[x]
	

	def addRelay(self, d1: ToaDo, d2: ToaDo):
		bkR = self.radius/2

		if d1.khoangCach(d2) <= 2*bkR:
			return
		
		d3 = ToaDo(0, 0)

		kCach = d1.khoangCach(d2)

		deltaX = 2 * bkR * abs(d2.getX() - d1.getX()) /  kCach
		deltaY = 2 * bkR * abs(d2.getY() - d1.getY()) /  kCach

		if d1.getX() < d2.getX():
			d3.setX(d1.getX() + deltaX)
		else:
			d3.setX(d1.getX() - deltaX)
		
		if d1.getY() < d2.getY():
			d3.setY(d1.getY() + deltaY)
		else:
			d3.setY(d1.getY() - deltaY)

		self.tapRelay.append(d3)
		ss = Sensor(d3, self.radius)


		self.fw.write(ss.toCircle() + "\n")
		
		self.relayNum += 1
		self.addRelay(d3, d2)
	
	def kruskal(self):
		n = len(self.tapSensor)
		for i in range(n):
			for j in range(i+1 , n):
				self.tapEdge.append(Edge(i, j, self.tapSensor[i].khoangCach(self.tapSensor[j])))
		
		self.sortEdge()

		self.root = [i for i in range(n)]

		self.tapAdj = [Adjacent() for _ in range(n)]

		for e in self.tapEdge:
			v1 = e.id1
			v2 = e.id2
			p = self.getRoot(v1)
			q = self.getRoot(v2)
			if p == q:
				continue

			self.root[p] = q
			self.tapAdj[v1].addDinhKe(v2)
			self.tapAdj[v2].addDinhKe(v1)

	def steiner(self):
		self.numIter = 0

		self.radius = self.radius/2

		print("R =", self.radius)

		self.root = [i for i in range(len(self.tapSensor))]

		while True:
			maxGain = -1
			uSaved = -1
			iSaved = -1
			vSaved = -1

			for i in range(len(self.tapSensor)):
				for iu in range(len(self.tapAdj[i].tapDinhKe)):
					for iv in range(iu+1, len(self.tapAdj[i].tapDinhKe)):
						u = self.tapAdj[i].tapDinhKe[iu]
						v = self.tapAdj[i].tapDinhKe[iv]

						p1 = self.tapSensor[i]
						p2 = self.tapSensor[u]
						p3 = self.tapSensor[v]


						gain = ToaDoMethod.gain(p1, p2, p3, self.radius)


						if gain > 0 and gain > maxGain:
							maxGain = gain
							iSaved = i
							uSaved = u
							vSaved = v 

			if maxGain > 1:
				self.numIter += 1
				p1 = self.tapSensor[iSaved]
				p2 = self.tapSensor[uSaved]
				p3 = self.tapSensor[vSaved]

				self.tapSensor.append(ToaDoMethod.getSteinerPoint(p1, p2, p3))
				stp = len(self.tapSensor) - 1


				self.tapAdj.append(Adjacent())

				ss = Sensor(self.tapSensor[stp], self.radius)
				self.fw.write(ss.toCircle() + "\n")
				self.relayNum += 1

				ri = self.getRoot(iSaved)
				ru = self.getRoot(uSaved)
				rv = self.getRoot(vSaved)

				self.root[ru] = self.root[rv] = ri

				self.tapAdj[iSaved].deleteDinhKe(uSaved)
				self.tapAdj[iSaved].deleteDinhKe(vSaved)
				self.tapAdj[uSaved].deleteDinhKe(iSaved)
				self.tapAdj[vSaved].deleteDinhKe(iSaved)

				self.tapAdj[iSaved].addDinhKe(stp)
				self.tapAdj[uSaved].addDinhKe(stp)
				self.tapAdj[vSaved].addDinhKe(stp)

				self.tapAdj[stp].addDinhKe(iSaved)
				self.tapAdj[stp].addDinhKe(uSaved)
				self.tapAdj[stp].addDinhKe(vSaved)
			
			else:
				break 
		
		self.radius *= 2
		for i in range(len(self.tapSensor)):
			for j in self.tapAdj[i].tapDinhKe:
				if i < j:
					self.addRelay(self.tapSensor[i], self.tapSensor[j])
		
		self.radius /= 2



	def xuat(self):
		print("Number iter of Steiner =", self.numIter)


	def checkIsConnected(self, Graph: list[list[int]], Redudant: list[int]):
		i = 0
		numVertex = self.relayNum
		listVS = []
		visited = [False]*numVertex
		stack = []
		listVS.append(i)
		stack.append(i)
		while stack:
			i = stack[-1]
			count = 0

			for j in range(numVertex):
				if j not in Redudant:
					if Graph[i][j] > 0 and not visited[j]:
						visited[j] = True
						listVS.append(j)
						stack.append(j)
						break
					else:
						count += 1
				else:
					count += 1
			
			if count == numVertex:
				stack.pop()

		for k in range(numVertex):
			if not visited[k] and k not in Redudant:
				return False
		
		return True

	def redudantRelay(self):
		Graph = [[0 for _ in range(self.relayNum)] for _ in range(self.relayNum)]

		allRelay: list[ToaDo] = self.tapSensor + self.tapRelay

		for i in range(len(allRelay)):
			for j in range(i+1, len(allRelay)):
				if allRelay[i].khoangCach(allRelay[j]) <= 2 * self.radius + 0.001:
					Graph[i][j] = Graph[j][i] = 1
		
		Redudant = []

		for i in range(len(self.tapRelay)):
			Redudant.append(i)

			if not self.checkIsConnected(Graph, Redudant):
				Redudant.pop()

		for e in self.tapRelay:
			allRelay.remove(e)
		
		tapRemove: list[ToaDo] = []

		for i in Redudant:
			tapRemove.append(self.tapRelay[i])
		
		for e in tapRemove:
			self.tapRelay.remove(e)

		allRelay += self.tapRelay
		
		
		self.relayNum = len(allRelay)


def main():
	for i in range(1, 19):
	# for i in range(17, 18):
		print("Test-Case:", i)
		x = Main()
		path = 	"/home/fool/Documents/code/Lab/MobileconnectivitySteinertree/CSTH/NEW/test2/Testmip/Test" + str(i)
		x.nhapDuLieu(path+".inp", path+".out")
		starttime = timeit.default_timer()

		x.inDuLieu()
		x.timDiemGiao()
		x.bapPhu()



		x.kruskal()

		x.steiner()

		x.redudantRelay()

		x.fw.close()

		endtime = timeit.default_timer()

		print(x.relayNum, "relay added")
		print("Time =:", endtime - starttime)
		x.xuat()
		print("-------------------")
	


if __name__ == "__main__":
	main()