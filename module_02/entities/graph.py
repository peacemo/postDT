class EdgeNode():
    # 邻接表的边表
	def __init__(self):
		self.__adjoinVex = None  # 与顶点相连的邻接点
		self.__nextNode = None  # 顶点的下一个邻接点
		pass

	@property
	def adjoinVex(self):
		return self.__adjoinVex

	@adjoinVex.setter
	def adjoinVex(self, value):
		self.__adjoinVex = value

	@property
	def nextNode(self):
		return self.__nextNode

	@nextNode.setter
	def nextNode(self, value):
		self.__nextNode = value

	def ToDict(self):
		dict1={
			'adjoinVex':self.__adjoinVex,
			'nextNode':self.__nextNode,
			}
		return dict1
	pass


class VertexNode():
    # 顶点表的结点
	def __init__(self):
		self.__vex = None  # 存储顶点名 顶点在结构体数组中的下标
		self.__nextNode = None  # 边表的头指针，指向顶点的第一个邻接点
		pass

	@property
	def vex(self):
		return self.__vex

	@vex.setter
	def vex(self, value):
		self.__vex = value

	@property
	def nextNode(self):
		return self.__nextNode

	@nextNode.setter
	def nextNode(self, value):
		self.__nextNode = value

	def ToDict(self):
		dict1={
			'vex':self.__vex,
			'nextNode':self.__nextNode,
			}
		return dict1
	pass


class Graph():
    # 有向图
	def __init__(self):
		self.__adjList = None  # 描述图结构的邻接表  结构体数组
		self.__vexNum = None  # 顶点的数目
		self.__edgeNum = None  # 边的数目
		pass

	@property
	def adjList(self):
		return self.__adjList

	@adjList.setter
	def adjList(self, value):
		self.__adjList = value

	@property
	def vexNum(self):
		return self.__vexNum

	@vexNum.setter
	def vexNum(self, value):
		self.__vexNum = value

	@property
	def edgeNum(self):
		return self.__edgeNum

	@edgeNum.setter
	def edgeNum(self, value):
		self.__edgeNum = value

	def ToDict(self):
		dict1={
			'adjList':self.__adjList,
			'vexNum':self.__vexNum,
			'edgeNum':self.__edgeNum,
			}
		return dict1
	pass

