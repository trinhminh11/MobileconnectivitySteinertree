class Point:
	x = y = 0
	def __init__(self, *args):
		if len(args) == 1:
			other = args[0]
			self.x = other.x
			self.y = other.y
		else:
			x, y = args
			self.x = x
			self.y = y
	
	def __eq__(self, other) -> bool:
		EPS = 1e-10

		return abs(self.x - other.x) < EPS and abs(self.y - other.y) < EPS
	
	def dist(self, other):
		return (pow(self.x - other.x, 2) + pow(self.y - other.y, 2)) ** .5

	def toDecimalString(self):
		return f"({self.x:.3f}, {self.y:.3f})"
		
