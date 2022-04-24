import random as rd
import numpy as np

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
    def allCost(cls, costFun, population):
        fitnessList = [-1] * len(population)  # 初始化适应度值列表，用于记录每个个体对应的适应度值
        for i in range( len(fitnessList) ):
            fitnessList[i] = costFun(population[i])

        return fitnessList

    
    @classmethod
    def calSelectProb(cls, fitnessList):
        fitnessAry = np.array(fitnessList)
        return ( fitnessAry / sum(fitnessAry) ).tolist()
        pass

    
    @classmethod
    def genOffspring(cls, population, selectProb):
        offSpring = []

        while len(offSpring) < len(population):
            # 通过累积概率选择一个个体

            pass

        pass


    @classmethod
    def ga(cls, costFun, seqLen, entityCount=100, iters=50):
        """
        遗传算法找到最优序列
        costFun: 计算单个个体的损失函数
        seqLen: 单个个体的编码长度
        entityCount: 种群中的个体数量
        iters: 遗传算法迭代的次数

        return: 最优的编码以及它的适应度值
        """

        # 生成初始种群
        population = cls.gen_population(seqLen, entityCount)  # 生成初始种群

        # 计算整个种群的适应度值
        fitnessList = cls.allCost(costFun, population)
        print(fitnessList)

        # 找到当前种群中最优的个体 
        bestEntityIndex = fitnessList.index( min(fitnessList) )  # 几下最优个体在种群中的索引值

        # TODO 创建一个列表来保存每次迭代中种群中的最优适应度值 
        fitnessHistory = []

        
        # TODO 遗传算法：
        for i in range(iters):  # 迭代次数
            # 计算种群中所有个体的适应度值()
            fitnessList = cls.allCost(costFun, population)

            # 根据适应度值计算每一个个体被选中的概率()
            selectProb = cls.calSelectProb(fitnessList)

            # 生成新的种群()
            # population = cls.genOffspring(population, selectProb)

            pass

        pass


    
####################################################################
def testCost(seq):
    cost = 0
    for i in range(len(seq)):
        cost += abs(i - seq[i])
    cost = round(cost / 10.0, 4)
    return cost

    pass

OptimizationAlgorithm.ga(testCost, 10, 10, 50)

####################################################################