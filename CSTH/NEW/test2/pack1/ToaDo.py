class ToaDo:
	x = y = 0
	def __init__(self, *args):
		if len(args) == 1:
			other = args[0]
			self.init(other.getX(), other.getY())
		else:
			ax = args[0]
			ay = args[1]
			self.init(ax, ay)
	
	def init(self, ax, ay):
		self.setX(ax)
		self.setY(ay)
	
	def getX(self):
		return self.x
	
	def getY(self):
		return self.y
	
	def setX(self, ax):
		self.x = ax
	
	def setY(self, ay):
		self.y = ay
	
	def __eq__(self, other) -> bool:
		EPS = 1e-10

		return abs(self.x - other.x) < EPS and abs(self.y - other.y) < EPS
	
	def khoangCach(self, other):
		return (pow(self.x - other.x, 2) + pow(self.y - other.y, 2)) ** .5

	def toDecimalString(self):
		return f"({self.x:.3f}, {self.y:.3f})"
		
