class Adjacent:
	def __init__(self) -> None:
		self.tapDinhKe = []
	
	def addDinhKe(self, u):
		self.tapDinhKe.append(u)
	
	def deleteDinhKe(self, u):
		self.tapDinhKe.remove(u)