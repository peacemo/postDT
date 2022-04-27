class Tools:

    def __init__(self) -> None:
        pass

    @staticmethod
    def showGraphInfo(graph):

        for item in graph.nodes:
            print(item)

        for item in graph.weights:
            print(item)

        for i in range(len(graph.weights)):
            for j in range(len(graph.weights[i])):
                if graph.weights[i][j] != 0:
                    print(graph.nodes[0][i], graph.nodes[0][j], graph.weights[i][j])

        pass


    @staticmethod
    def stdOutput(level: list, nodes: list, pointsInfo):

        bias = abs( min(level) ) + 1
        tempDict = {}

        for i in range(len(level)):
            tempDict.update({nodes[i] : level[i]})

        for item in pointsInfo:
            try:
                if tempDict[item[0]] >= 0:
                    item.insert(0, tempDict[item[0]] + 1 + bias )
                else:
                    item.insert(0, tempDict[item[0]] + bias)
                pass
            except:
                print("入库产线不包含此点")
        
        return pointsInfo
        pass