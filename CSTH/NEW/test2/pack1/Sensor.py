from pack1.ToaDo import ToaDo

class Sensor:
	def __init__(self, tam: ToaDo, rad) -> None:
		self.center: ToaDo = None
		self.targetCovered = []

		self.setCenter(tam)
		self.radius = rad
	
	def setCenter(self, tam: ToaDo):
		self.center = ToaDo(tam)
		self.targetCovered = []
	
	def toCircle(self):
		return f'(x-{self.center.getX():.3f})^2 +(y-{self.center.getY():.3f})^2 = {self.radius * self.radius/4:.3f}'

	def getTargetCount(self):
		return len(self.targetCovered)


	def add(self, target):
		if target not in self.targetCovered:
			self.targetCovered.append(target)

	def remove(self, target):
		if target in self.targetCovered:
			self.targetCovered.remove(target)
	
	def isCover(self, target: ToaDo):
		EPS = 1e-10

		return self.center.khoangCach(target) - self.radius < EPS

	def returnList(self):
		lst = self.targetCovered.copy()

		return lst

