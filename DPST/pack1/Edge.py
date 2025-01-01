from pack1.Point import Point

class Edge:
	def __init__(self, a, b, p1: Point, p2: Point, dd) -> None:
		self.id1 = a
		self.id2 = b
		self.point1 = p1
		self.point2 = p2
		self.doDai = dd
		self.isXoa = False
