class Point:
	EPS = 10e-9
	def __init__(self, *args) -> None:
		if len(args) == 1:
			other = args[0]
			self.x = other.x
			self.y = other.y
			self.t = -1
			self.visited = True
		
		elif len(args) == 2:
			x, y = args
			self.x = x
			self.y = y
			self.t = -1
			self.visited = True
			
		elif len(args) == 3:
			x, y, t = args
			self.x = x
			self.y = y
			self.t = t
			self.visited = False
		
	def __eq__(self, other) -> bool:
		return abs(self.x-other.x) < self.EPS and abs(self.y - other.y) < self.EPS

	def dist(self, other):
		return (pow(self.x-other.x, 2) + pow(self.y-other.y, 2) ) ** .5

	def toDecimalString(self):
		return f"({self.x:.3f},{self.y:.3f})"
	
	def printRelay(self, R):
		print(f'(x-{self.x:.3f})^2 +(y-{self.y:.3f})^2 = {R*R:.3f}')

	def __add__(self, other):
		return Point(self.x + other.x, self.y + other.y)

	def __sub__(self, other):
		return Point(self.x - other.x, self.y - other.y)

	def __mul__(self, k):
		return Point(self.x * k, self.y * k)

	def __div__(self, k):
		return Point(self.x/k, self.y/k)
	
	def norm(self):
		return self.x*self.x + self.y*self.y

	def length(self) -> float:
		return self.norm()**.5
	
	def dist(self, other):
		return (self - other).length()
	
	def __lt__(self, other):
		if abs(self.x - other.x) < self.EPS:
			return self.y < other.y
		
		return self.x < other.x
	
	def __str__(self):
		return f'Point: ({self.x:.3f}, {self.y:.3f})'

	def __repr__(self) -> str:
		return f'({self.x}, {self.y})'
	
	def toCircle(self, R):
		return f'(x-{self.x:.3f})^2 + (y-{self.y:.3f})^2 = {R*R}'
	