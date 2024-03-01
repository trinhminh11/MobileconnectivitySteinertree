from pack1 import *
import pack1.Method as Method
import os
import timeit

cur_path = os.path.dirname(__file__)

class Node:
	def __init__(self, id) -> None:
		self.id = id
		self.parent: Node = None
		self.children: list[Node] = []
	
	def search_parent(self, lst: list):
		lst.append(self.id)
		if self.parent:
			self.parent.search_parent(lst)

class Tree:
	def __init__(self, root = None, size = 0) -> None:
		self.root = root
		self.size = size

def import_data(inp):
	PointSet: list[Point] = []

	with open(inp, 'r') as f:

		W, L = map(int, f.readline().split())
		
		BASE = Point(*map(int, f.readline().split()))

		carNum = int(f.readline())

		R = float(f.readline()) * 2

		periodNum = int(f.readline())
		n = carNum * periodNum

		temp_Point = []

		for i in range(carNum):
			for j in range(periodNum):
				temp_Point.append(Point(*map(float, f.readline().split()), j))


		temp_Point.append(BASE)

		n += 1

		for i in range(n):
			isHave = False
			for j in range(i):
				if temp_Point[i] == temp_Point[j]:
					isHave = True
					break

			if isHave:
				continue

			PointSet.append(temp_Point[i])
		
	return W, L, R, PointSet, periodNum
	

class Solver:
	N_MAX = 5007

	def __init__(self, W, L, R, PointSet: list[Point], period_num) -> None:
		self.W = W
		self.L = L
		self.R = R
		self.n = len(PointSet)
		self.PointSet = PointSet
		self.period_num = period_num

		self.IntersectSet: list[Sensor] = []
		self.SensorSet: list[Point] = []
		self.RelaySet: list[Point] = []

		self.AdjSet: list[list[int]] = []

		self.relayNum = 0

		self.mark = [[False for _ in range(self.N_MAX)] for _ in range(self.N_MAX)]

		self.numIter = 0

		self.out = ""

		for i in range(self.n):
			self.out += self.PointSet[i].toDecimalString() + "\n"
	

	# return 1 point intersect of 2 circle
	def Intersect(self, p1: Point, p2: Point, radius, id):
		x1, x2 = p1.x, p2.x
		y1, y2 = p1.y, p2.y

		xCenter = (x1 + x2)/2
		yCenter = (y1 + y2)/2
		distance = p1.dist(p2)

		if y1 != y2:
			v = (x1-x2) / (y2-y1)
			xRes = xCenter + ( (radius * radius - distance * distance/4) / (1 + v * v) ) ** .5
			yRes = v * (xRes - xCenter) + yCenter
		else:
			xRes = xCenter
			yRes = yCenter + (radius * radius - distance * distance/4) **.5
		
		if id == 2:
			xRes = 2 * xCenter - xRes
			yRes = 2 * yCenter - yRes
		
		return Point(xRes, yRes)
		

	def check(self, x, y, v):
		for i in range(v):
			for j in range(v):
				if self.mark[x+i][y+j]:
					return False
				if y-j >= 0 and self.mark[x+i][y-j]:
					return False

				if x-i >= 0 and self.mark[x-i][y+j]:
					return False 

				if x-i >= 0 and y-j >= 0 and self.mark[x-i][y-j]:
					return False
		
		return True
	
	def findIntersection(self):
		for i in range(self.n):
			for j in range(i+1, self.n):
				p1 = self.PointSet[i]
				p2 = self.PointSet[j]

				if p1.dist(p2) <= 2 * self.R:
					intersection_point = self.Intersect(p1, p2, self.R, 1)
					
					roundX = round(intersection_point.x)
					roundY = round(intersection_point.y)

					if roundX >= 0 and roundY >= 0 and roundX <= self.W and roundY <= self.L and self.check(roundX, roundY, int(self.R/20)):
						self.IntersectSet.append(Sensor(intersection_point, self.R))
						self.mark[roundX][roundY] = True
					
					intersection_point = self.Intersect(p1, p2, self.R, 2)
					roundX = round(intersection_point.x)
					roundY = round(intersection_point.y)

					if roundX >= 0 and roundY >= 0 and roundX <= self.W and roundY <= self.L and self.check(roundX, roundY, int(self.R/20)):

						self.IntersectSet.append(Sensor(intersection_point, self.R))
						self.mark[roundX][roundY] = True
		
		for i in range(len(self.IntersectSet)):
			for j in range(self.n):
				if self.IntersectSet[i].isCover(self.PointSet[j]):
					self.IntersectSet[i].add(j)
	
	def cover(self):
		self.IntersectSet.sort(key= lambda x: x.getTargetCount(), reverse= True)

		covered = [False] * self.n


		while True:
			coverMax = float('-inf')
			choosed = Sensor(Point(0, 0), self.R)

			for point in self.IntersectSet:
				if point.getTargetCount() > coverMax:
					coverMax = point.getTargetCount()
					choosed = point

			if coverMax <= 0:
				break
			
			self.out += choosed.toCircle() + "\n"
			self.SensorSet.append(Point(choosed.center))

			targetList = choosed.returnList()
			targetListCount = choosed.getTargetCount()

			for point in self.IntersectSet:
				for i in range(targetListCount):
					point.remove(targetList[i])
					covered[targetList[i]] = True
			

		for i in range(self.n):
			if not covered[i]:
				s = Sensor(self.PointSet[i], self.R)
				self.out += s.toCircle() + "\n"
				self.SensorSet.append(Point(s.center))
		
		self.relayNum = len(self.SensorSet)	

	def addRelay(self, d1: Point, d2: Point):
		bkR = self.R/2

		if d1.dist(d2) <= 2*bkR:
			return
		
		d3 = Point(0, 0)

		dst = d1.dist(d2)

		deltaX = 2 * bkR * abs(d2.x - d1.x) /  dst
		deltaY = 2 * bkR * abs(d2.y - d1.y) /  dst

		if d1.x < d2.x:
			d3.x = (d1.x + deltaX)
		else:
			d3.x = (d1.x - deltaX)
		
		if d1.y < d2.y:
			d3.y = (d1.y + deltaY)
		else:
			d3.y = (d1.y - deltaY)

		self.RelaySet.append(d3)
		ss = Sensor(d3, self.R)

		self.out += ss.toCircle() + "\n"
		
		self.relayNum += 1
		self.addRelay(d3, d2)
	
	def Kruskal(self):
		n = len(self.SensorSet)
		EdgeSet: list[list[int]] = []
		for i in range(n):
			for j in range(i+1 , n):
				EdgeSet.append([i, j, self.SensorSet[i].dist(self.SensorSet[j])])
		
		EdgeSet.sort(key= lambda x: x[2])

		root = [i for i in range(n)]

		def getRoot(x):
			if root[x] == x:
				return x
			else:
				root[x] = getRoot(root[x])
				return root[x]

		self.AdjSet = [[] for _ in range(n)]


		for e in EdgeSet:
			v1 = e[0]
			v2 = e[1]
			p = getRoot(v1)
			q = getRoot(v2)
			if p == q:
				continue

			root[p] = q
			self.AdjSet[v1].append(v2)
			self.AdjSet[v2].append(v1)

	def SteinerTree(self):
		self.numIter = 0

		self.R = self.R/2

		root = [i for i in range(len(self.SensorSet))]

		def getRoot(x):
			if root[x] == x:
				return x
			else:
				root[x] = getRoot(root[x])
				return root[x]

		while True:
			maxGain = -1
			uSaved = -1
			iSaved = -1
			vSaved = -1

			for i in range(len(self.SensorSet)):
				for iu in range(len(self.AdjSet[i])):
					for iv in range(iu+1, len(self.AdjSet[i])):
						u = self.AdjSet[i][iu]
						v = self.AdjSet[i][iv]

						p1 = self.SensorSet[i]
						p2 = self.SensorSet[u]
						p3 = self.SensorSet[v]


						gain = Method.gain(p1, p2, p3, self.R)


						if gain > 0 and gain > maxGain:
							maxGain = gain
							iSaved = i
							uSaved = u
							vSaved = v 

			if maxGain > 1:
				self.numIter += 1
				p1 = self.SensorSet[iSaved]
				p2 = self.SensorSet[uSaved]
				p3 = self.SensorSet[vSaved]

				self.SensorSet.append(Method.getSteinerPoint(p1, p2, p3))
				stp = len(self.SensorSet) - 1

				self.AdjSet.append([])

				ss = Sensor(self.SensorSet[stp], self.R)
				self.out += ss.toCircle() + "\n"
				self.relayNum += 1

				ri = getRoot(iSaved)
				ru = getRoot(uSaved)
				rv = getRoot(vSaved)

				root[ru] = root[rv] = ri

				self.AdjSet[iSaved].remove(uSaved)
				self.AdjSet[iSaved].remove(vSaved)
				self.AdjSet[uSaved].remove(iSaved)
				self.AdjSet[vSaved].remove(iSaved)

				self.AdjSet[iSaved].append(stp)
				self.AdjSet[uSaved].append(stp)
				self.AdjSet[vSaved].append(stp)

				self.AdjSet[stp].append(iSaved)
				self.AdjSet[stp].append(uSaved)
				self.AdjSet[stp].append(vSaved)
			
			else:
				break 
		
		self.R *= 2
		for i in range(len(self.SensorSet)):
			for j in self.AdjSet[i]:
				if i < j:
					self.addRelay(self.SensorSet[i], self.SensorSet[j])
		
		self.R /= 2

	# Minh Trinh		
	def calcEnergy(self):
		Sensors = self.PointSet[:-1]
		Relays = self.RelaySet + self.SensorSet
		Base = self.PointSet[-1]

		n = len(Sensors)

		m = len(Relays)

		Nodes = Sensors + Relays + [Base]

		EPS = 10e-9
		b = len(Nodes) - 1
		
		Edges: list[list[list]] = [[] for _ in range(self.period_num)]


		for i in range(n):
			t = Sensors[i].t
			# create Edge from Sensor and Sensor
			for j in range(i+1, n):
				if t == Sensors[j].t and Sensors[i].dist(Sensors[j]) <= 2 * self.R + EPS:
					Edges[t].append([i, j, Sensors[i].dist(Sensors[j])])
			
			# create Edge from Sensor to Relay
			for j in range(m):
				if Sensors[i].dist(Relays[j]) <= 2 * self.R + EPS:
					Edges[t].append([i, j+n, Sensors[i].dist(Relays[j])])
			
			# create Edge from Sensor to Base
			if Sensors[i].dist(Base) <= 2 * self.R + EPS:
				Edges[t].append([i, b, Sensors[i].dist(Base)])
		
		for i in range(m):

			for j in range(i+1, m):
				dst = Relays[i].dist(Relays[j])
				if dst <= 2 * self.R + EPS:
					for t in range(self.period_num):
						Edges[t].append([i+n, j+n, dst])
			
			dst = Relays[i].dist(Base)
			if dst <= 2 * self.R + EPS:
				for t in range(self.period_num):
					Edges[t].append([i+n, b, dst])

		def Kruskal(t):
			root = [i for i in range(len(Nodes))]

			E = Edges[t].copy()

			def getRoot(x):
				if root[x] == x:
					return x
				else:
					root[x] = getRoot(root[x])
					return root[x]

			E.sort(key= lambda x: x[2])

			SpanningEdges: dict[int, list] = {e: [] for e in range(len(Nodes))}

			for e in E:
				p = getRoot(e[0])
				q = getRoot(e[1])

				if p == q:
					continue

				root[p] = q

				SpanningEdges[e[0]].append(e[1])
				SpanningEdges[e[1]].append(e[0])

			root = Node(b)

			stack = [root]
			visited = [False] * len(Nodes)
			visited[b] = True

			Sensor_nodes: list[Node] = []

			while stack:
				current = stack.pop()
				if current.id < len(Sensors):
					Sensor_nodes.append(current)
				for v in SpanningEdges[current.id]:
					if not visited[v]:
						node = Node(v)
						current.children.append(node)
						node.parent = current
						stack.append(node)
						visited[v] = True
				
		
			return Sensor_nodes

		data = [[0, 0] for _ in range(len(Nodes)-1)]

		for t in range(self.period_num):
			Sensor_nodes = Kruskal(t)

			for S in Sensor_nodes:
				path: list[int] = []
				S.search_parent(path)

				data[path[0]][0] += 1


				for i in range(1, len(path)-1):
					node_idx = path[i]
					data[node_idx][0] += 1
					data[node_idx][1] += 1
		
		def energy(no_transmit, no_receive, R):
			E_elec = 50*1e-9
			E_freespace = 10*1e-12
			K = 525*8
			return no_receive*(E_elec)*K + no_transmit*(K*E_elec + K*E_freespace*R*R)


		total_E = 0
		max_E = float('-inf')
		min_E = float('inf')
		

		for values in data:
			no_transmit, no_receive = values

			energy_consumption = energy(no_transmit, no_receive, self.R)

			total_E += energy_consumption

			if energy_consumption > max_E:
				max_E = energy_consumption
			
			if energy_consumption < min_E:
				min_E = energy_consumption
		

		return total_E, max_E, max_E - min_E

	def solve(self):
		for i in range(self.n):
			self.out += self.PointSet[i].toDecimalString() + "\n"
		
		self.findIntersection()

		self.cover()

		self.Kruskal()

		self.SteinerTree()

		self.total_E, self.max_E, self.delta_E = map(round, self.calcEnergy(), [4]*3)

	
	def export_data(self, out):
		with open(out, 'w') as f:
			f.write(self.out)

def main():
	for i in range(1, 19):
		print("Test-Case:", i)
		path = cur_path + "/Testnew/" + str(i)
		W, L, R, Ps, p_num = import_data(path+".inp")
		solver = Solver(W, L, R, Ps, p_num)

		starttime = timeit.default_timer()
		solver.solve()
		endtime = timeit.default_timer()


		solver.export_data(path + ".out")


		print("Added =", solver.relayNum)
		print(f"Total, Max, Delta Energy: {solver.total_E}, {solver.max_E}, {solver.delta_E}")
		print("Time =", endtime - starttime)
		print("Number iter of Steiner =", solver.numIter)
		print("-------------------")

if __name__ == "__main__":
	main()
