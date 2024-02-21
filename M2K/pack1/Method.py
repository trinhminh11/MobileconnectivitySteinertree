from pack1.Point import Point

EPS = 10e-7
EPS2 = 10e-9
cos120 = -0.5


def getMidPoint(a: Point, b: Point):
	x = (a.x + b.x) / 2
	y = (a.y + b.y) / 2
	return Point(x, y)


def getD(a: Point, b: Point, c: Point):
	midPoint = getMidPoint(a, b)
	
	AB = a.dist(b)

	dst = (3**.5) * AB / 2
	cosAlpha = abs(a.y - b.y) / AB
	sinAlpha = (1-cosAlpha*cosAlpha) ** .5

	v = [dst * cosAlpha, dst * sinAlpha]

	if abs(a.x - b.x) < EPS2:
		if c.x > a.x:
			v[0] = -v[0]
		v[1] = 0
	
	elif abs(a.y - b.y) < EPS2:
		if c.y > a.y:
			v[1] = -v[1]
		v[0] = 0
	
	else:
		CoeA = (a.y - b.y) / (a.x - b.x)

		CoeB = a.y - CoeA * a.x

		if (a.x-b.x) * (a.y-b.y) > 0:
			v[0] = -v[0]
		
		if c.y < CoeA * c.x + CoeB:
			v = [-v[0], -v[1]]
		
		v = [-v[0], -v[1]]
	

	return Point(midPoint.x + v[0], midPoint.y + v[1])
	

def IntersectionPoint(a: Point, b: Point, c: Point, d: Point):
	deno = (a.x - b.x)*(c.y-d.y) - (a.y-b.y) * (c.x - d.x)

	x = (a.x*b.y - a.y * b.x) * (c.x - d.x) - (a.x - b.x) * (c.x * d.y - c.y * d.x)
	y = (a.x*b.y - a.y * b.x) * (c.y - d.y) - (a.y - b.y) * (c.x * d.y - c.y * d.x)

	x /= deno
	y /= deno

	return Point(x, y)

def getSteinerPoint(d1: Point, d2: Point, d3: Point):
	d4 = getD(d1, d2, d3)
	d5 = getD(d1, d3, d2)

	return IntersectionPoint(d4, d3, d5, d2)

def cos(a: Point, b: Point, c: Point):
	AB = a.dist(b)
	BC = b.dist(c)
	AC = a.dist(c)

	return (AB*AB + BC*BC - AC*AC) / (2*AB*BC)

def lessThan120(a: Point, b: Point, c: Point):
	cosAlpha = cos(a, b, c)

	return cosAlpha > cos120 and cosAlpha - cos120 > EPS
		
