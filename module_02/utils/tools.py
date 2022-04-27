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
    def stdOutput(level: list, nodes: list, pointsInfo: list, stacker: int) -> list:
        """
        标准化输出: 将输出的边按层级和时间消耗排序, 层级升序, 时间降序
        level: 层级信息
        nodes: 顶点信息
        pointsInfo: 边信息
        stacker: 叠箱机的 id
        return: 带有层级信息且排好序的边信息用作输出
        """

        bias = abs( min(level) ) + 1  # 为所有的层级添加一个权重
        tempDict = {}  # 用字典记录下每一个点的层级

        for i in range(len(level)):
            tempDict.update({nodes[i] : level[i]})

        for item in pointsInfo:
            # 对于边表中的每一条边,插入其起点的层级参数
            try:
                if tempDict[item[0]] >= 0:
                    item.insert(0, tempDict[item[0]] + 1 + bias )
                else:
                    item.insert(0, tempDict[item[0]] + bias)
                pass
            except:
                print("入库产线不包含此点")
        
        pointsInfo = sorted(pointsInfo, key=lambda x: (x[0], -x[-1]))  # 按照pointsInfo中的第 1 个和最后一个值排序,第一个字段升序,最后一个字段降序
        pointsInfo = [points for points in pointsInfo if points[0] != float('inf')]  # 去除不连通的边
        # print(pointsInfo)

        outputData = {'graphOfSpots' : pointsInfo, 'stackerID' : 1}

        return outputData
        pass

    @staticmethod
    def getStacker(dvcDictionary):
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