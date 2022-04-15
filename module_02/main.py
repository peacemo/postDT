from graphGenerator import *

def get_fake_data():
    return ((1,3,3.1), (2,1,2.5), (3,7,3.1), (3,8,3.4), (4,2,2.4), (5,2,1.5), (6,2,1.4), (9,5,2.3), (10,9,2.5), (11,9,2.1))

def get_stacker(nodes):
    """
    找到拆叠箱机的 id 并返回其 index
    nodes: 顶点表 [ [顶点对象], [顶点的id] ]

    return: 拆叠箱机的 index
    """
    stacker_index = 0
    return stacker_index

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
    points_info = get_fake_data()
    graph = GraphGenerator.gen_graph(points_info)
    stacker = get_stacker(graph.nodes)

    show_info(graph)



if __name__ == "__main__":
    # execute only if run as a script
    main()
