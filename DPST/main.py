import os
import timeit
from pack1 import Point, Edge
import pack1.Method as Method

cur_path = os.path.dirname(__file__)

def import_data(file):
	nodes: list[Point] = []
	with open(file, 'r') as f:
		H, W = map(int, f.readline().split())
		
		base = Point(*map(float, f.readline().split()))

		num_car = int(f.readline())
		R = float(f.readline())
		num_time = int(f.readline())
		nodes.append(base)

		for i in range(num_car):
			for j in range(num_time):
				nodes.append(Point(*map(float, f.readline().split()), j))

		
	return nodes, R, num_time

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

class Solver:
	N_MAX = 5007
	def __init__(self, nodes: list[Point], R: float, period_num: int) -> None:
		self._SensorSet = nodes
		self.SensorSet = nodes.copy()
		self.PointSet = nodes.copy()
		self.SensorSet.sort()
		self.R = R
		self.period_num = period_num
		self.RelaySet: list[Point] = []

	def calcEnergy(self):
		Sensors = self.PointSet[1:]
		Relays = self.RelaySet
		Base = self.PointSet[0]

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

	def Kruskal(self, S: list[Point]):
		root = [i for i in range(len(S))]
		Edges = []

		def getRoot(x):
			if root[x] == x:
				return x
			else:
				root[x] = getRoot(root[x])
				return root[x]
		
		for i in range(len(S)):
			for j in range(i+1, len(S)):
				p1 = S[i]	
				p2 = S[j]	

				Edges.append([i, j, p1.dist(p2)])
		
		Edges.sort(key=lambda x: x[2])

		EdgeSet: list[tuple[int, int]] = []
		
		for e in Edges:
			idA = e[0]
			idB = e[1]

			p = getRoot(idA)
			q = getRoot(idB)
			if p == q:
				continue

			root[p] = q

			EdgeSet.append(e[:-1])
		
		return EdgeSet

	def SteinerTree(self, S: list[Point], EdgeSet: list[tuple[int, int]]):
		d1 = d2 = d3 = 0
		id1 = id2 = id3 = idSteiner = 0

		d1Choosed = Point(0, 0)
		d2Choosed = Point(0, 0)
		d3Choosed = Point(0, 0)

		e1 = [0, 0, 0]
		e2 = [0, 0, 0]

		deleted = [False] * len(EdgeSet)

		for i in range(len(EdgeSet)):
			if deleted[i]:
				continue

			idChoosed = -1
			alphaMax = float('-inf')

			for j in range(len(EdgeSet)):
				if i == j or deleted[j]:
					continue

				isIntersect = False
				e1 = EdgeSet[i]
				e2 = EdgeSet[j]

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

				# print(d1, d2, d3, len(S))

				alpha = Method.cos(S[d1], S[d2], S[d3])

				if alpha > alphaMax:
					alphaMax = alpha
					idChoosed = j
					d1Choosed = S[d1]
					d2Choosed = S[d2]
					d3Choosed = S[d3]
					id1 = d1
					id2 = d2
					id3 = d3

			if idChoosed == -1:
				continue

			if Method.lessThan120(d1Choosed, d2Choosed, d3Choosed):
				steinerP = Method.getSteinerPoint(d1Choosed, d2Choosed, d3Choosed)
				steinerP.t = d1Choosed.t

				dst1 = steinerP.dist(d1Choosed)
				dst2 = steinerP.dist(d2Choosed)
				dst3 = steinerP.dist(d3Choosed)

				if dst1 < 2 * self.R or dst2 < 2 * self.R or dst3 < 2 * self.R:
					continue

				deleted[i] = True
				deleted[idChoosed] = True
				S.append(steinerP)
				# self.SensorSet.append(steinerP)

				idSteiner = len(S) - 1

				EdgeSet.append([id1, idSteiner])
				EdgeSet.append([id2, idSteiner])
				EdgeSet.append([id3, idSteiner])

				deleted += [False] * 3

				self.RelaySet.append(steinerP)
		
		for i in range(len(EdgeSet)):
			if not deleted[i]:
				self.addRelay(S[EdgeSet[i][0]], S[EdgeSet[i][1]])
				# self.SteinerSet.append(self.EdgeSet[i])
	
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
	
	def solve(self):
		self.SensorSet_t: list[list[Point]] = [[] for _ in range(self.period_num)]

		for point in self.SensorSet:
			if point.t >= 0:
				self.SensorSet_t[point.t].append(point)
			
			if point.t == -1:
				base = point
		
		for i in range(self.period_num):
			self.SensorSet_t[i].append(base)

			EdgeSet = self.Kruskal(self.SensorSet_t[i])

			self.SteinerTree(self.SensorSet_t[i], EdgeSet)
		
		self.total_E, self.max_E, self.delta_E = map(round, self.calcEnergy(), [4]*3)

	def export_data(self, out: str):
		with open(out, 'w') as f:
			for p in self.RelaySet:
				f.write(f"(x-{p.x:.3f})^2 +(y-{p.y:.3f})^2 = {self.R*self.R:.3f}\n")

			for i in range(len(self.SensorSet)):
				f.write(self.SensorSet[i].toCircle(self.R) + "\n")	

def main():
	for i in range(1, 19):
		print("Test-Case:", i)

		path = cur_path + "/Testnew/" + str(i)

		nodes, R, period_num = import_data(path + ".inp")

		solver = Solver(nodes, R, period_num)

		starttime = timeit.default_timer()
		solver.solve()
		endtime = timeit.default_timer()

		solver.export_data(path + ".out")

		print("ADDED =", len(solver.RelaySet))

		print(f"Total, Max, Delta Energy: {solver.total_E}, {solver.max_E}, {solver.delta_E}")

		print("time =", endtime - starttime)

		print("------------------------")


if __name__ == "__main__":
	main()
