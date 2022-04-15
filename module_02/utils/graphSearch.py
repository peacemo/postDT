from entities.AMGraph import *
from queue import Queue

class BFS:
    def __init__(self) -> None:
        pass

    @classmethod
    def AMG(cls, graph: AMGraph, nodes, start):
        """
        邻接矩阵形式的图的广搜
        graph: 邻接矩阵
        nodes: 边表
        start: 起始位置
        """

        inque = Queue(graph.nodeCount)
        level = graph.nodeCount * [0]
        visited = graph.nodeCount * [False]
        currentLevel = 0

        level[start] = currentLevel
        visited[start] = True
        
        inque.put(start)

        while not inque.empty():
            currentLevel += 1
            head = inque.get()
            for i in range(len(graph.nodeCount)):
                if (graph.weights[head][i] != 0) and (not visited[i]):
                    print(graph.nodes[i])
                    visited[i] = True
                    level[i] = currentLevel
                    inque.put(i)


        pass
    @classmethod
    def ATG(cls):
        pass
