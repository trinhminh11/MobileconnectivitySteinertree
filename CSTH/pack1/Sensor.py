from pack1.Point import Point

class Sensor:
	def __init__(self, tam: Point, rad) -> None:
		self.center: Point = None
		self.targetCovered = []

		self.setCenter(tam)
		self.R = rad

	def setCenter(self, center: Point):
		self.center = Point(center)
		self.targetCovered = []
	
	def toCircle(self):
		return f'(x-{self.center.x:.3f})^2 +(y-{self.center.y:.3f})^2 = {self.R * self.R/4:.3f}'

	def getTargetCount(self):
		return len(self.targetCovered)

	def add(self, target):
		if target not in self.targetCovered:
			self.targetCovered.append(target)

	def remove(self, target):
		if target in self.targetCovered:
			self.targetCovered.remove(target)
	
	def isCover(self, target: Point):
		EPS = 1e-10

		return self.center.dist(target) - self.R < EPS

	def returnList(self):
		lst = self.targetCovered.copy()

		return lst

