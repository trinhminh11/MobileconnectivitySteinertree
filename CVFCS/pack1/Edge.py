from pack1.ToaDo import ToaDo

class Edge:
	def __init__(self, a, b, p1: ToaDo, p2: ToaDo, dd) -> None:
		self.id1 = a
		self.id2 = b
		self.point1 = p1
		self.point2 = p2
		self.doDai = dd
		self.isXoa = False
