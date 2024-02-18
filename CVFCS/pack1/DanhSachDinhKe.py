class DanhSachDinhKe:
	def __init__(self) -> None:
		self.adj = []
	
	def push(self, x):
		self.adj.append(x)
	
	def get(self, id):
		return self.adj[id]

	def show(self):
		print(self.adj)
	
	def size(self):
		return len(self.adj)
