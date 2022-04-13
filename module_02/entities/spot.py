import string


class Point():
	# 坐标
	def __init__(self):
		self.__X = None
		self.__Y = None
		self.__Z = None
		pass

	@property
	def X(self):
		return self.__X

	@X.setter
	def X(self, value):
		self.__X = value

	@property
	def Y(self):
		return self.__Y

	@Y.setter
	def Y(self, value):
		self.__Y = value

	@property
	def Z(self):
		return self.__Z

	@Z.setter
	def Z(self, value):
		self.__Z = value

	def ToDict(self):
		dict1={
			'X':self.__X,
			'Y':self.__Y,
			'Z':self.__Z,
			}
		return dict1
	pass


class Spot():
	# 交通点
	def __init__(self):
		self.__id = None  # 交通点的 ID
		self.__point = None  # 交通点的坐标
		self.__type = None  # 交通点的类型
		pass

	@property
	def id(self):
		return self.__id

	@id.setter
	def id(self, value: int):
		self.__id = value

	@property
	def point(self):
		return self.__point

	@point.setter
	def point(self, value: Point):
		self.__point = value

	@property
	def type(self):
		return self.__type

	@type.setter
	def type(self, value: string):
		self.__type = value

	def ToDict(self):
		dict1={
			'id':self.__id,
			'point':self.__point,
			'type':self.__type,
			}
		return dict1
	pass
