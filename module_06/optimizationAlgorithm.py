import random as rd

class OptimizationAlgorithm:

    def __init__(self) -> None:
        pass
    

    @classmethod
    def gen_population(cls, seqLen, entityCount) -> list:
        """
        生成 entityCount 个从 1 ~ seqLen 的随机序列
        seqLen: 每一个序列的长度
        entityCount: 种群大小
        return: 种群（entityCount 个随机打乱的序列，类型为 list）
        """
        population = []
        for i in range(entityCount):
            # 生成 entityCount 个从 1 ~ seqLen 的随机序列
            entity = list(range(1, (seqLen+1), 1))
            rd.shuffle(entity)
            population.append(entity)    
        
        print(population)

        return population
        pass


    @classmethod
    def ga(cls, function, seqLen, entityCount=100, iters=50):
        # 遗传算法

        # 生成初始种群
        population = cls.gen_population(seqLen, entityCount)  # 生成初始种群

        # TODO 计算整个种群的适应度值
        fitnessList = [-1] * entityCount  # 初始化适应度值列表，用于记录每个个体对应的适应度值
        # TODO 填入计算过程（仿真算法）

        # TODO 找到当前种群中最优的个体

        # TODO 创建一个列表来保存每次迭代中种群中的最优适应度值

        """
        TODO 遗传算法：
        for i in range(iters):  # 迭代次数
            * 计算种群中所有个体的适应度值()

            * 根据适应度值计算每一个个体被选中的概率()

            * 生成新的种群()
                *


        """

        pass


    


# OptimizationAlgorithm.ga(10, 10, 50)