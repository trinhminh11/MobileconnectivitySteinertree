from pack1.ToaDo import ToaDo

class Cluster:
	def __init__(self, center: ToaDo) -> None:
		self.centroid = ToaDo(center)
		self.pointOfCluster: list[ToaDo] = []
	
	def add(self, diem):
		self.pointOfCluster.append(diem)
	
	def center(self):

		x = 0
		y = 0

		for diem in self.pointOfCluster:
			x += diem.getX()
			y += diem.getY()
		
		pointCount = len(self.pointOfCluster)

		x /= pointCount
		y /= pointCount

		return ToaDo(x, y)

	def getCentroid(self):
		return self.centroid
	
	def returnList(self):
		return self.pointOfCluster