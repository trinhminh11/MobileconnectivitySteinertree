class Point:
	def __init__(self, *args) -> None:
		self.x = self.y = 0

		if len(args) == 1:
			other = args[0]
			self.x = other.x
			self.y = other.y
		else:
			ax, ay = args
			self.x = ax
			self.y = ay

	def dist(self, other):
		return (pow(self.x - other.x, 2) + pow(self.y - other.y, 2)) **.5
	
	def toDecimalString(self):
		return f'({self.x:.3f},{self.y:.3f})'

	def toCircle(self, R):
		return f'(x-{self.x:.3f})^2 +(y-{self.y:.3f})^2 = {R*R:.3f}'
	