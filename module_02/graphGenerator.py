import numpy as np
from utils.mysqlTool import *
from entities.spot import *


def get_data(type: int):
    """
    从数据库中查询节点的边权表
    type: 查询类型
        0 为坐标表示，1 为 id 表示
    """
    points = selectCrossPoints(type)
    print("Points: \n", points)
    return points


def gen_graph(edgeSet):
    """
    根据边权表生成一个邻接矩阵
    edgeSet: 边权表
    """
    nodes = getNodes(edgeSet)  # 将所有的点的id生成一个顶点表
    graph = np.zeros((len(nodes[0]), len(nodes[0]))).tolist()  # 初始化邻接矩阵
    graph = fillWeight(graph, edgeSet, nodes)  # 向邻接矩阵中填入权值
    return nodes, graph
    pass


def getNodes(edgeSet):
    """
    生成顶点表
    edgeSet: 边权表 [ [p1, p2, weight], ... ]
    """
    nodes = [[],[]]
    for edge in edgeSet:  # 遍历每一条边
        for id in edge[:2]:  # 遍历边中的两个顶点
            if id not in nodes[0]:
                tempPoint = Point(0, 0, 0)
                tempSpot = Spot(id, tempPoint, 'default')
                nodes[1].append(tempSpot)  # 把没见过的顶点添加到表中
                nodes[0].append(id)  # 把没见过的顶点添加到表中
                
    
    return nodes  # 返回表
    pass


def fillWeight(graph, edgeSet, nodes):
    """
    向邻接矩阵中填入权值
    graph: 邻接矩阵
    edgeSet: 边权表
    nodes: 顶点表
    """
    for edge in edgeSet:  # 遍历边表中的每一条边
        id1, id2, weight = edge[0], edge[1], edge[2]  # 取出边的信息：顶点1， 顶点2， 权值
        graph[nodes[0].index(id1)][nodes[0].index(id2)] = weight  # 将邻接矩阵中两个顶点对应位置的值设定为权值，代表存在边
    
    return graph

    pass

