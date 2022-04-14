from graphGenerator import *

def get_fake_data():
    return ((1,3,3.1), (2,1,2.5), (3,7,3.1), (3,8,3.4), (4,2,2.4), (5,2,1.5), (6,2,1.4), (9,5,2.3), (10,9,2.5), (11,9,2.1))

def get_stacker(nodes):
    """
    找到拆叠箱机的 id 并返回其 index
    nodes: 顶点表 [ [顶点对象], [顶点的id] ]
    """
    stacker_index = 0
    print('id of stacker:', nodes[1][stacker_index].id)
    return stacker_index

# points_info = get_data(1)
points_info = get_fake_data()
nodes, graph = gen_graph(points_info)
stacker = get_stacker(nodes)
print(type(nodes), type(graph))
print(nodes[0])

for item in graph:
    print(item)

for i in range(len(graph)):
    for j in range(len(graph[i])):
        if graph[i][j] != 0:
            print(nodes[0][i], nodes[0][j], graph[i][j])