from webbrowser import get
from entities.AMGraph import *
from queue import Queue

class BFS:
    def __init__(self) -> None:
        pass

    @classmethod
    def AMG(cls, graph: AMGraph, stacker) -> list:
        """
        邻接矩阵形式的图的广搜
        graph: 邻接矩阵
        start: 起始位置
        """

        inque = Queue(graph.nodeCount)
        level = graph.nodeCount * [0]  # 用于存储搜索到的节点的层级数
        visited = graph.nodeCount * [False]  # 用于记录某节点是否已经访问
        checkedNodes = []
        start = graph.nodes[0].index(stacker)

        level[start] = 0  # 将起始节点的层级设置为 0
        visited[start] = True  # 将起始节点设置为已访问
        checkedNodes.append(graph.nodes[0][start])
        
        inque.put(start)

        while not inque.empty():  # 如果隊列中依然存在元素，則證明沒有遍歷完
            head = inque.get()  # 取出當前隊列中的首元
            for i in range(graph.nodeCount):  # 開始對首元的下一層節點遍歷
                currentLevel = abs(level[head])  # 取得当前节点的层次
                if (graph.weights[head][i] != 0) and (not visited[i]):  # 遍历边表，如果有边且没有访问过
                    print(graph.nodes[0][i])  # 输出这个节点的 id
                    checkedNodes.append(graph.nodes[0][i])
                    visited[i] = True  # 将这个子节点标记为已访问
                    level[i] = currentLevel + 1  # 将子节点的层级设置为母节点 +1
                    inque.put(i)  # 子节点入队，之后会对这个节点的子节点遍历
                if (graph.weights[head][i] == 0 and graph.weights[i][head] != 0) and (not visited[i]):
                    # 这一块的意思和上一个 if 模块中的意思差不多
                    # 这里是 A-B 没有路径，但是 B-A 有路径
                    # 也就是反向的下一层（将有向图按照无向图处理）
                    # 逻辑上层次会取反
                    print(graph.nodes[0][i])
                    checkedNodes.append(graph.nodes[0][i])
                    visited[i] = True
                    level[i] = - (currentLevel + 1)
                    inque.put(i)
        # level = [i + ( abs(min(level)) + 1 ) for i in level]
        print(checkedNodes)

        try:
            visited.index(False)
            print("不是一个连通图,以下是从叠箱机出发无法访问的节点: ")
            deVisited = []
            for i in range(len(visited)):
                if not visited[i]:
                    deVisited.append(graph.nodes[0][i])
                    level[i] = float('inf')
            print(deVisited)
            pass
        except:
            print("是一个连通图")
            pass

        # return level, checkedNodes
        return level, graph.nodes[0]


    @classmethod
    def ATG(cls):
        pass
