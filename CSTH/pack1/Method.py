from pack1.Point import Point
from math import ceil


def addRelayNode(p1: Point, p2: Point, R, RNset: list[Point]):
	dst = p1.dist(p2)

	for i in range(2, ceil(dst/R), 2):
		xk = p1.x + i * R * (p2.x - p1.x) / dst
		yk = p1.y + i * R * (p2.y - p1.y) / dst

		p3 = Point(xk, yk)

		RNset.append(p3)

def getSteinerPoint(p1: Point, p2: Point, p3: Point):
	w = p1.dist(p2)
	v = p1.dist(p3)
	u = p2.dist(p3)

	p = (u + v + w) / 2
	S = ( p * (p-u) * (p-v) * (p-w) ) ** .5
	k = ((u*u + v*v + w*w)/2 + 2 * (3**.5) * S) ** .5

	def temp(_u, _v, _w):
		return (_u*_u + _v*_v - 2 * _w * _w + k*k) / (3*k)

	d = temp(v, w, u)
	e = temp(u, w, v)
	f = temp(v, u, w)

	tuSoX = (f*f - d*d - p3.x*p3.x + p1.x*p1.x - p3.y*p3.y + p1.y*p1.y) * (p1.y - p2.y) - (e*e - d*d - p2.x*p2.x + p1.x*p1.x - p2.y*p2.y + p1.y*p1.y) * (p1.y - p3.y)
	mauSoX = 2 * ((p1.x - p3.x)*(p1.y - p2.y) - (p1.x - p2.x)*(p1.y - p3.y))

	sx = tuSoX / mauSoX

	tuSoY = (f*f - d*d - p3.x*p3.x + p1.x*p1.x - p3.y*p3.y + p1.y*p1.y) * (p1.x - p2.x) - (e*e - d*d - p2.x*p2.x + p1.x*p1.x - p2.y*p2.y + p1.y*p1.y) * (p1.x - p3.x)
	mauSoY = 2 * ((p1.x - p2.x)*(p1.y - p3.y) - (p1.x - p3.x)*(p1.y - p2.y))
	sy = tuSoY / mauSoY

	return Point(sx, sy)


def setSteinerPoint(p1: Point, p2: Point, p3: Point, R, RNset: list[Point]):
	s = getSteinerPoint(p1, p2, p3)

	RNset.append(s)

	addRelayNode(p1, s, R, RNset)
	addRelayNode(p2, s, R, RNset)
	addRelayNode(p3, s, R, RNset)

def numOfRelayByMST(p1: Point, p2: Point, p3: Point, R):
	dst = [None] * 3

	dst[0] = p2.dist(p3)
	dst[1] = p1.dist(p3)
	dst[2] = p1.dist(p2)

	for i in range(3):
		for j in range(i+1, 3):
			if dst[i] > dst[j]:
				dst[i], dst[j] = dst[j], dst[i]

	
	return ceil(dst[0]/R) + ceil(dst[1]/R)

def numOfRelayBySMT(p1: Point, p2: Point, p3: Point, R):
	s = getSteinerPoint(p1, p2, p3)

	su = p1.dist(s)
	sv = p2.dist(s)
	sw = p3.dist(s)

	return ceil(su/R) + ceil(sv/R) + ceil(sw/R)

def gain(p1, p2, p3, R):
	return numOfRelayByMST(p1, p2, p3, R) - numOfRelayBySMT(p1, p2, p3, R)

