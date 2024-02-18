class ToaDo:
	def __init__(self, *args) -> None:
		self.x = self.y = 0
		if len(args) == 1:
			other = args[0]

			self.init(other.getX(), other.getY())
		
		else:
			ax, ay = args
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

	def khoangCach(self, other):
		return (pow(self.x - other.x, 2) + pow(self.y - other.y, 2)) **.5
	
	def toDecimalString(self):
		return f'({self.x:.3f},{self.y:.3f})'

	def toCircle(self, R):
		return f'(x-{self.x:.3f})^2 +(y-{self.y:.3f})^2 = {R*R:.3f}'
	