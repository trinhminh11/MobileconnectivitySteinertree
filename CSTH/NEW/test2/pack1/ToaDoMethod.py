from pack1.ToaDo import ToaDo
from math import ceil

def getDist(p1: ToaDo, p2: ToaDo):
	return p1.khoangCach(p2)

def addRelayNode(p1: ToaDo, p2: ToaDo, radius, tapRN: list[ToaDo]):
	dst = getDist(p1, p2)

	for i in range(2, ceil(dst/radius), 2):
		xk = p1.x + i * radius * (p2.x - p1.x) / dst
		yk = p1.y + i * radius * (p2.y - p1.y) / dst

		p3 = ToaDo(xk, yk)

		tapRN.append(p3)

def getSteinerPoint(p1: ToaDo, p2: ToaDo, p3: ToaDo):
	w = getDist(p1, p2)
	u = getDist(p2, p3)
	v = getDist(p1, p3)

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

	return ToaDo(sx, sy)

def setSteinerPoint(p1: ToaDo, p2: ToaDo, p3: ToaDo, radius, tapRN: list[ToaDo]):
	s = getSteinerPoint(p1, p2, p3)

	tapRN.append(s)

	addRelayNode(p1, s, radius, tapRN)
	addRelayNode(p2, s, radius, tapRN)
	addRelayNode(p3, s, radius, tapRN)

def numOfRelayByMST(p1: ToaDo, p2: ToaDo, p3: ToaDo, radius):
	dst = [None] * 4

	dst[1] = getDist(p2, p3)
	dst[2] = getDist(p1, p3)
	dst[3] = getDist(p1, p2)

	for i in range(1, 4):
		for j in range(i+1, 4):
			if dst[i] > dst[j]:
				dst[i], dst[j] = dst[j], dst[i]
	
	return ceil(dst[1]//radius) + ceil(dst[2]/radius)

def numOfRelayBySMT(p1: ToaDo, p2: ToaDo, p3: ToaDo, radius):
	s = getSteinerPoint(p1, p2, p3)

	su = getDist(p1, s)
	sv = getDist(p2, s)
	sw = getDist(p3, s)

	return ceil(su/radius) + ceil(sv/radius) + ceil(sw/radius)

def gain(p1, p2, p3, radius):
	return numOfRelayByMST(p1, p2, p3, radius) - numOfRelayBySMT(p1, p2, p3, radius)
