class Point:
	EPS = 10e-9
	def __init__(self, *args) -> None:
		if len(args) == 1:
			other = args[0]
			self.x = other.x
			self.y = other.y
			self.cycle = -1
		
		elif len(args) == 2:
			x, y = args
			self.x = x
			self.y = y
			self.cycle = -1
			
		elif len(args) == 3:
			x, y, cycle = args
			self.x = x
			self.y = y
			self.cycle = cycle
	
	def __eq__(self, other) -> bool:
		return abs(self.x-other.x) < self.EPS and abs(self.y - other.y) < self.EPS

	def dist(self, other):
		return (pow(self.x-other.x, 2) + pow(self.y-other.y, 2) ) ** .5

	def toDecimalString(self):
		return f"({self.x:.3f},{self.y:.3f})"
	
	
	def printRelay(self, R):
		print(f'(x-{self.x:.3f})^2 +(y-{self.y:.3f})^2 = {R*R:.3f}')
	