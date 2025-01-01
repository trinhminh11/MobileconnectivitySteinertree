import math

EPS = 1e-6 

class Point:
	def __init__(self, x: int = 0, y: int = 0, t = -1) -> None:
		self.x = x
		self.y = y
		self.t = t
	
	def __add__(self, other: "Point"):
		return Point(self.x + other.x, self.y + other.y)

	def __sub__(self, other: "Point"):
		return Point(self.x - other.x, self.y - other.y)

	def __mul__(self, k):
		return Point(self.x * k, self.y * k)

	def __div__(self, k):
		return Point(self.x/k, self.y/k)
	
	def norm(self):
		return self.x*self.x + self.y*self.y

	def length(self) -> float:
		return self.norm()**.5
	
	def dist(self, other: "Point"):
		return (self - other).length()
	
	def __lt__(self, other: "Point"):
		if abs(self.x - other.x) < EPS:
			return self.y < other.y
		
		return self.x < other.x
	
	def __str__(self):
		return f'({self.x:.3f}, {self.y:.3f})'

	def __repr__(self) -> str:
		return f'({self.x}, {self.y})'
	
	def toCircle(self, R):
		return f'(x-{self.x:.3f})^2 + (y-{self.y:.3f})^2 = {R*R}'


def distance(p1: Point, p2: Point):
	p = p1 - p2
	return p.length()

def getSides(A: Point, B: Point, C: Point):
	return [distance(B, C), distance(C, A), distance(A, B)]

def getAngle(a: float, b:float, c:float):
	if b < EPS or c < EPS:
		return math.pi

	alpha = (b*b+c*c-a*a)/(2*b*c)

	if alpha > 1 and alpha - 1 < EPS:
		alpha = 1
	elif alpha < -1 and alpha + 1 > - EPS:
		alpha = -1
	
	return math.acos(alpha)

def getSecantAngle(a: float, b: float, c: float):
	return 1/ math.cos(getAngle(a, b, c) - math.pi/6)

def getTrilinear(A: Point, B: Point, C: Point, p: float, q: float, r: float):
	x = (p*A.x + q*B.x + r*C.x) / (p+q+r)
	y = (p*A.y + q*B.y + r*C.y) / (p+q+r)
	return Point(x, y)

def getFermatPoints(A: Point, B: Point, C: Point):
	a, b, c = getSides(A, B, C)

	if getAngle(a, b, c) >= 2*math.pi/3:
		return A
	
	if getAngle(b, c, a) >= 2*math.pi/3:
		return B
	
	if getAngle(c, a, b) >= 2*math.pi/3:
		return C
	
	p = a * getSecantAngle(a, b, c)
	q = b * getSecantAngle(b, c, a)
	r = c * getSecantAngle(c, a, b)

	return getTrilinear(A, B, C, p, q, r)

def getFermatPointandDistance(A: Point, B: Point, C: Point):
	F = getFermatPoints(A, B, C)
	dis = distance(F, A) + distance(F, B) + distance(F, C)
	return F, dis

