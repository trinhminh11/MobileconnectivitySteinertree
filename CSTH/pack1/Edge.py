class Edge:
	def __init__(self, verA, verB, length) -> None:
		self.id1 = verA
		self.id2 = verB
		self.length = length
	
	def getVerA(self):
		return self.id1

	def getVerB(self):
		return self.id2
	
	def getLength(self):
		return self.length
	