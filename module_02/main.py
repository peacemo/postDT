from utils.graphGenerator import *
from utils.graphSearch import *
from utils.tools import *

def getFakeData():
    # return ((1,3,3.1), (2,1,2.5), (3,7,3.1), (3,8,3.4), (4,2,2.4), (5,2,1.5), (6,2,1.4), (9,5,2.3), (10,9,2.5), (11,9,2.1))
    return [[1,3,3.1], [2,1,2.5], [3,7,3.1], [3,8,3.4], [4,2,2.4], [5,2,1.5], [6,2,1.4], [9,5,2.3], [10,9,2.5], [11,9,2.1]]


def main():
    # points_info = get_fake_data()  # 获取边数据
    points_info, dvcDictionary = GraphGenerator.getEdges()

    print("获取到的边表如下: ", points_info, "\n")

    graph = GraphGenerator.genGraph(points_info)  # 通过边数据生成有向图邻接矩阵
    stacker = Tools.getStacker(dvcDictionary)  # 获取拆叠箱机的位置
    # show_info(graph)

    level, graph.nodes[0] = BFS.AMG(graph, stacker)  # 对图进行广搜，获取层次

    ###############################################
    # print(level)
    # print(graph.nodes[0])
    ###############################################

    outputData = Tools.stdOutput(level, graph.nodes[0], points_info, stacker)

    print(dvcDictionary, '\n')

    print(outputData)

    return outputData

if __name__ == "__main__":
    # execute only if run as a script
    main()
