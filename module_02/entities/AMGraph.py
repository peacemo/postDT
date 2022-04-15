class AMGraph():
	"""
	使用邻接矩阵存储图
	nodes: 顶点表
	weights: 边表
	nodeCount: 顶点数目
	weightCount: 边数目
	"""
	def __init__(self):
		self.__nodes = None
		self.__weights = None
		self.__nodeCount = 0
		self.__weightCount = 0
		pass

	@property
	def nodes(self):
		return self.__nodes

	@nodes.setter
	def nodes(self, value):
		self.__nodes = value

	@property
	def weights(self):
		return self.__weights

	@weights.setter
	def weights(self, value):
		self.__weights = value

	@property
	def nodeCount(self):
		return self.__nodeCount

	@nodeCount.setter
	def nodeCount(self, value):
		self.__nodeCount = value

	@property
	def weightCount(self):
		return self.__weightCount

	@weightCount.setter
	def weightCount(self, value):
		self.__weightCount = value

	def ToDict(self):
		dict1={
			'nodes':self.__nodes,
			'weights':self.__weights,
			'nodeCount':self.__nodeCount,
			'weightCount':self.__weightCount,
			}
		return dict1
	pass
