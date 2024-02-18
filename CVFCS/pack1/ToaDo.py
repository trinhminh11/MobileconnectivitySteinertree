class ToaDo:
	EPS = 10e-9
	def __init__(self, *args) -> None:
		x, y, chuKy = 0, 0, -1

		if len(args) == 1:
			other = args[0]
			self.init(other.getX(), other.getY(), -1)
		
		elif len(args) == 2:
			ax, ay = args 
			self.init(ax, ay, -1)
			
		elif len(args) == 3:
			ax, ay, ck = args
			self.init(ax, ay, ck)
		
	def init(self, ax, ay, ck):
		self.setX(ax)
		self.setY(ay)
		self.chuKy = ck
	
	def getX(self):
		return self.x

	def getY(self):
		return self.y

	def setX(self, ax):
		self.x = ax
	
	def setY(self, ay):
		self.y = ay
	
	def __eq__(self, other) -> bool:
		return abs(self.x-other.x) < self.EPS and abs(self.y - other.y) < self.EPS

	def khoangCach(self, other):
		return (pow(self.x-other.x, 2) + pow(self.y-other.y, 2) ) ** .5

	def toDecimalString(self):
		return f"({self.x:.3f},{self.y:.3f})"
	
	def print(self):
		print(self.toDecimalString())
	
	def printRelay(self, R):
		print(f'(x-{self.x:.3f})^2 +(y-{self.y:.3f})^2 = {R*R:.3f}')
	