from utils.graphGenerator import *
from utils.graphSearch import *

def get_fake_data():
    # return ((1,3,3.1), (2,1,2.5), (3,7,3.1), (3,8,3.4), (4,2,2.4), (5,2,1.5), (6,2,1.4), (9,5,2.3), (10,9,2.5), (11,9,2.1))
    return [[1,3,3.1], [2,1,2.5], [3,7,3.1], [3,8,3.4], [4,2,2.4], [5,2,1.5], [6,2,1.4], [9,5,2.3], [10,9,2.5], [11,9,2.1]]


def get_stacker(dvcDictionary):
    """
    找到拆叠箱机的 id
    dvcDictionary: 设备 id 与其名称(类型)的对应字典

    return: 叠箱机的 id
    """
    stacker = 0
    for key, val in dvcDictionary.items():
        if '叠箱机' in val and '拆' not in val:
            stacker = key
        pass

    return stacker


def show_info(graph: AMGraph):

    for item in graph.nodes:
        print(item)

    for item in graph.weights:
        print(item)

    for i in range(len(graph.weights)):
        for j in range(len(graph.weights[i])):
            if graph.weights[i][j] != 0:
                print(graph.nodes[0][i], graph.nodes[0][j], graph.weights[i][j])


def main():
    # points_info = get_data(1)
    # points_info = get_fake_data()  # 获取边数据
    points_info, dvcDictionary = GraphGenerator.getEdges()
    graph = GraphGenerator.gen_graph(points_info)  # 通过边数据生成有向图邻接矩阵
    stacker = get_stacker(dvcDictionary)  # 获取拆叠箱机的位置
    # show_info(graph)

    level, graph.nodes[0] = BFS.AMG(graph, stacker)  # 对图进行广搜，获取层次
    print(level)
    print(graph.nodes[0])
    
    #################################################
    bias = abs( min(level) ) + 1
    tempDict = {}

    for i in range(len(level)):
        tempDict.update({graph.nodes[0][i] : level[i]})

    for item in points_info:
        try:
            if tempDict[item[0]] >= 0:
                item.insert(0, tempDict[item[0]] + 1 + bias )
            else:
                item.insert(0, tempDict[item[0]] + bias)
            pass
        except:
            print("入库产线不包含此点")
    print(points_info)
    #################################################

    # TODO 去除不可到达的点位
    return points_info

if __name__ == "__main__":
    # execute only if run as a script
    main()
