from math import sqrt
import random as rd
from secrets import choice
from statistics import mean
import numpy as np
import copy as cp

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
        
        # print(population)

        return population
        pass


    @classmethod
    def allCost(cls, costFun, population):
        """
        计算整个群体的损失
        costFun: 损失函数
        population: 整个群体
        return: 群体中每一个个体的适应度值: list
        """
        fitnessList = [-1] * len(population)  # 初始化适应度值列表，用于记录每个个体对应的适应度值
        for i in range( len(fitnessList) ):
            fitnessList[i] = costFun(population[i])

        return fitnessList

    
    @classmethod
    def calSelectProb(cls, fitnessList):
        """
        计算每一个个体被选择的概率
        fitnessList: 群体的适应度值list
        return: 每个个体被选择的概率
        """
        fitnessAry = 1 / np.array(fitnessList)
        p = ( fitnessAry / sum(fitnessAry) )
        # p = (max(fitnessAry) - fitnessAry) / (max(fitnessAry) - min(fitnessAry))
        return p.tolist()
        pass

    
    @classmethod
    def genOffspring(cls, costFun, population, selectProb, fitnessList, bestEntityIndex):
        """
        生成新的种群
        costFun: 单个个体的损失计算函数
        population: 整个种群
        selectProb: 每个个体的被选择概率
        fitnessList: 群体的适应度值
        bestEntityIndex: 群体中最优的个体的索引
        return: 新的种群
        """
        offSprings = []

        while len(offSprings) < len(population):
            # 通过累积概率选择两个个体进行杂交
            motherIndex = cls.roulette(selectProb)
            fatherIndex = motherIndex
            while motherIndex == fatherIndex:
                fatherIndex = cls.roulette(selectProb)
            parents = [population[motherIndex], population[bestEntityIndex]]

            offSpring = cls.hybrid(population, parents, bestEntityIndex, 2)  # 交叉
            # if costFun(offSpring) <= fitnessList[motherIndex]:
            #     offSprings.append(offSpring)

            offSprings.append(offSpring)

            pass

        return offSprings

        pass


    @classmethod
    def hybrid(cls, population, parents, bestEntityIndex ,partition):
        """
        两个个体交叉
        population: 整个种群
        parents: 进行交叉的两个长辈
        partition: 交叉操作所需要进行交叉的序列长度的百分比，值为 int，若长度为 30%，则 partition=3
        return: 一个新的个体
        """
        partLen = len(parents[0]) - int(len(parents[0]) * partition * 0.1)
        startPosition = rd.randrange(0, partLen)
        endPositon = int(startPosition + len(parents[0]) * partition * 0.1)

        # mother, father = population[parents[0]], population[parents[1]]
        mother, father = parents[0], parents[1]
        child = cp.deepcopy(mother)

        for position in range(startPosition, endPositon):
            currentEle = father[position]
            child.remove(currentEle)
            child.insert(position, currentEle)
            pass

        if rd.random() < 0.1:
            child = cls.mutate(mother)
            pass

        return child

        pass


    @classmethod
    def mutate(cls, entity):
        """
        变异操作
        entity: 变异的个体
        return: 变异后的个体
        """
        partLen = len(entity) - int(len(entity) * 5 * 0.1)
        start = rd.randrange(0, partLen)
        end = int(start + len(entity) * 5 * 0.1 - 1)

        temp = cp.deepcopy(entity) 

        entity[start:end+1] = temp[end-len(temp) : start-len(temp)-1 : -1]

        return entity

        pass


    @classmethod
    def roulette(cls, selectProb):
        """
        轮盘赌选择
        selectProb: 种群中每个个体的被选择概率
        return: 被选中的个体的索引值
        """
        selection = -1
        p = rd.uniform(0, sum(selectProb))
        
        totalProb = 0
        for i in range(len(selectProb)):
            totalProb += selectProb[i]
            if totalProb >= p:
                selection = i
                break
            pass
        pass

        if selection == -1:
            selection = len(selectProb) - 1

        return selection


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
        # print(fitnessList)

        # 找到当前种群中最优的个体 
        bestEntityIndex = fitnessList.index( min(fitnessList) )  # 几下最优个体在种群中的索引值
        print(population[bestEntityIndex])

        # 创建一个列表来保存每次迭代中种群中的最优适应度值 
        fitnessHistory = []
        
        # TODO 遗传算法：
        for i in range(iters):  # 迭代次数
            # print(population)

            # 根据适应度值计算每一个个体被选中的概率()
            selectProb = cls.calSelectProb(fitnessList)
            # print(selectProb)

            # 生成新的种群
            population = cls.genOffspring(costFun, population, selectProb, fitnessList, bestEntityIndex)

             # 计算新种群中所有个体的适应度值()
            fitnessList = cls.allCost(costFun, population)

            bestEntityIndex = fitnessList.index( min(fitnessList) )

            fitnessHistory.append(min(fitnessList))


            pass

        # print(fitnessHistory)
        print(population)
        print("Best:\n", population[bestEntityIndex], "\n", fitnessList[bestEntityIndex])

        pass


    
####################################################################
def testCost(seq: list):
    cost = 0
    for i in range(len(seq)):
        cost += pow( (i+1) - seq[i], 2 )
    if cost == 0: cost = 0.1
    return cost

    pass

OptimizationAlgorithm.ga(testCost, 15, 50, 500)

####################################################################