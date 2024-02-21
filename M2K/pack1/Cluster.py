from pack1.Point import Point

class Cluster:
	def __init__(self, center: Point) -> None:
		self.centroid = Point(center)
		self.pointOfCluster: list[Point] = []
	
	def add(self, diem):
		self.pointOfCluster.append(diem)
	
	def center(self):

		x = 0
		y = 0

		for diem in self.pointOfCluster:
			x += diem.x
			y += diem.y
		
		pointCount = len(self.pointOfCluster)

		x /= pointCount
		y /= pointCount

		return Point(x, y)

	def getCentroid(self):
		return self.centroid
	
	def returnList(self):
		return self.pointOfCluster