from geo import *
from copy import deepcopy
import timeit
import os

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

class Solver:
	def __init__(self, nodes: list[Point], R: float, period_num: int) -> None:
		self._SensorSet = nodes
		self.SensorSet = nodes.copy()
		self.SensorSet.sort()
		self.R = R
		self.period_num = period_num
		self.RelaySet: list[Point] = []

	def discard_sensor_node(self, root: int, sensor_node: list[Point], target: list[bool]):
		n = len(sensor_node)
		deleted = [False] * n
		g = [[] for _ in range(n)]

		for i in range(n):
			for j in range(i+1, n):
				dis = (sensor_node[j] - sensor_node[i]).length()

				if dis < self.R + EPS:
					g[i].append(j)
					g[j].append(i)

		def still_connected():
			check = [False] * n
			queue = []
			queue.append(root)

			check[root] = True

			while queue:
				u = queue.pop(0)

				for e in g[u]:
					if deleted[e] or check[e]:
						continue
					check[e] = 1
					if not target[e]:
						queue.append(e)

			
			ok = True

			for i in range(n):
				if target[i]:
					ok &= check[i]
			
			return ok

		for i in range(n):
			if target[i] or i == root:
				continue

			deleted[i] = True

			if not still_connected():
				deleted[i] = False
		
		return deleted

	def calc_Edge(self, listNode: list[Point]):
		listEdge: list[list[int]] = []
		listEdge.append([0, 1])
		for i in range(2, len(self.SensorSet)):
			best = -1
			valBest = float('inf')

			for j in range(len(listEdge)):
				edge = listEdge[j]

				foo = getFermatPointandDistance(listNode[edge[0]], listNode[edge[1]], listNode[i])
				delta = foo[1] - distance(listNode[edge[0]], listNode[edge[1]])
				
				if delta < valBest:
					best = j
					valBest = delta
			

			e1 = listNode[listEdge[best][0]]
			e2 = listNode[listEdge[best][1]]


			F = getFermatPointandDistance(e1, e2, listNode[i])[0]
			fId = len(listNode)


			if distance(F, e1) < EPS:
				fId = listEdge[best][0]
			
			elif distance(F, e2) < EPS:
				fId = listEdge[best][1]
			
			elif distance(F, listNode[i]) < EPS:
				fId = i
			

			edgeBest = listEdge[best]

			if fId == len(listNode):
				listNode.append(F)

				listEdge[best], listEdge[-1] = listEdge[-1], listEdge[best]

				listEdge.pop()
				listEdge.append([i, fId])
				listEdge.append([edgeBest[0], fId])
				listEdge.append([edgeBest[1], fId])
			
			elif fId == i:
				listEdge[best], listEdge[-1] = listEdge[-1], listEdge[best]
				listEdge.pop()
				listEdge.append([edgeBest[0], fId])
				listEdge.append([edgeBest[1], fId])
			
			else:
				listEdge.append([fId, i])
			
		return listEdge

	def calcEnergy(self):
		Sensors = self._SensorSet[1:]
		Relays = self.RelaySet
		Base = self._SensorSet[0]

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
		listNode: list[Point] = []
		listEdge: list[list[int]] = []

		if len(self.SensorSet) <= 1:
			return len(self.SensorSet)
		
		listNode = deepcopy(self.SensorSet)

		listEdge = self.calc_Edge(listNode)

		activeNodes: list[int] = []
		isactive = [False] * len(listNode)

		for e1, e2 in listEdge:
			activeNodes.append(e1)
			activeNodes.append(e2)
			isactive[e1] = True 
			isactive[e2] = True

		activeNodes = list(set(activeNodes))

		activeNodes.sort()

		ans = float('inf')


		g: list[list[int]] = [[] for _ in range(len(listNode))]

		for e1, e2 in listEdge:
			g[e1].append(e2)
			g[e2].append(e1)

		for root in range(0, 1):
			pushed = [False] * len(listNode)
			f = [0.] * len(listNode)

			queue: list[int] = []

			queue.append(activeNodes[root])
			pushed[activeNodes[root]] = True
			f[activeNodes[root]] = self.R
			tmp_ans = 1
			sensor_nodes = deepcopy(self.SensorSet)
			sensor_nodes.append(Point(activeNodes[root], 0))
			# sensor_nodes.append(activeNodes[root])

			while queue:
				u = queue.pop(0)
				sta = listNode[u]

				for e in g[u]:
					if pushed[e]:
						continue
					en = listNode[e]
					pushed[e] = True

					dis = distance(listNode[u], listNode[e])
					t = math.ceil((dis-f[u])/self.R)
					tmp_ans += t

					dir = en - sta
					start_sensor = sta + dir *(f[u]/dis)
					dir = dir * (self.R/dir.length())
					for i in range(t):
						sensor_nodes.append(start_sensor + dir * i)
					
					f[e] = t * self.R - (dis - f[u])
					queue.append(e)
			
			isTarget = [False] * len(sensor_nodes)

			for i in range(len(self.SensorSet)):
				isTarget[i] = True
			
			deleted = self.discard_sensor_node(len(self.SensorSet), sensor_nodes, isTarget)
			tmp_ans = 1

			temp_Relay_Set = []

			for i in range(len(sensor_nodes)):
				if not isTarget[i] and not deleted[i]:
					temp_Relay_Set.append(sensor_nodes[i])
					tmp_ans += 1

			if tmp_ans < ans:
				ans = tmp_ans
				self.RelaySet = temp_Relay_Set
				
		
		self.total_E, self.max_E, self.delta_E = map(round, self.calcEnergy(), [4]*3)
	

	def export_data(self, out):
		with open(out, 'w') as f:
			for S in self._SensorSet:
				f.write(S.__str__() + "\n")
				# f.write(S.toCircle(self.R/2) + "\n")
			
			for R in self.RelaySet:
				f.write(R.toCircle(self.R/2) + "\n")

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



def main():
	for i in range(1, 19):
		print(f"Test-Case: {i}")

		starttime = timeit.default_timer()

		path = cur_path + "/Testmip/Test" + str(i)
		nodes, R, period_num = import_data(path + ".inp")
		R *= 2
		solver = Solver(nodes, R, period_num)
		solver.solve()

		solver.export_data(path + ".out")

		endtime = timeit.default_timer()
		print(f'ADDED = {len(solver.RelaySet)}')
		print(f"Total, Max, Delta Energy: {solver.total_E}, {solver.max_E}, {solver.delta_E}")
		print(f'time = {endtime - starttime}')
		print("------------------------")



if __name__ == "__main__":
	main()
