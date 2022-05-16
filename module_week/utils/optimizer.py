import random as rd
import numpy as np
import math
import copy as cp

from module_week.preMod.test import calFitness
from module_week.utils.planGenerator import PlanGenerator


class OptimizationAlgorithm:

    def __init__(self, typeCount, days) -> None:
        self.__typeCount = typeCount
        self.__days = days
        pass

    # @property
    # def ddjData

    def outputGenerator(self, sequence, fitness):
        return ...
        pass

    def genPopulation(self, entityCount) -> list:
        planGenerator = PlanGenerator(self.__typeCount, self.__days, 16119)
        population = []
        for i in range(entityCount):
            # 生成 entityCount 个个体
            entity = planGenerator.getAFkPlan()
            population.append(entity)
            # print(population)

        return population
        pass

    def allCost(self, costFun, population):
        """
        计算整个群体的损失
        costFun: 损失函数
        population: 整个群体
        return: 群体中每一个个体的适应度值: list
        """
        fitnessList = [-1] * len(population)  # 初始化适应度值列表，用于记录每个个体对应的适应度值
        for i in range(len(fitnessList)):
            # print(population[i])
            fitnessList[i] = costFun(population[i])

        return fitnessList

    def calSelectProb(self, fitnessList):
        """
        计算每一个个体被选择的概率
        fitnessList: 群体的适应度值list
        return: 每个个体被选择的概率
        """
        # fitnessAry = np.array(fitnessList)
        fitnessAry = 1 / np.array(fitnessList)
        p = (fitnessAry / sum(fitnessAry))
        # p = (max(fitnessAry) - fitnessAry) / (max(fitnessAry) - min(fitnessAry))
        return p.tolist()
        pass

    def genOffspring(self, costFun, population, selectProb, fitnessList, best10Index):
        """
        生成新的种群
        costFun: 单个个体的损失计算函数
        population: 整个种群
        selectProb: 每个个体的被选择概率
        fitnessList: 群体的适应度值
        bestEntityIndex: 群体中最优的个体的索引
        return: 新的种群
        """
        offsprings = []  # 后代个体
        for index in best10Index:
            offsprings.append(population[index])

        while len(offsprings) < len(population):
            parentAIndex = self.roulette(selectProb)
            parentBIndex = rd.choice(best10Index.tolist())
            while parentAIndex == parentBIndex:
                parentBIndex = rd.choice(best10Index.tolist())
            parents = [population[parentAIndex], population[parentBIndex]]

            offspring = self.hybrid(costFun=costFun, population=population, parents=parents, fitnessList=fitnessList, partion = 3)
            pass

        return offsprings
        pass

    def hybrid(self, costFun, population, parents, fitnessList, partion):
        """
        两个个体交叉
        population: 整个种群
        parents: 进行交叉的两个双亲
        partition: 交叉操作所需要进行交叉的序列长度的百分比，值为 int，若长度为 30%，则 partition=3
        return: 一个新的个体
        """
        planGrt = PlanGenerator(self.__typeCount, self.__days, 16119)
        adjustDays = rd.choices([])
        # mother, father = population[parents[0]], population[parents[1]]
        parentA, parentB = parents[0], parents[1]
        child = cp.deepcopy(parentA)



        return child
        pass

    def mutate(self, entity, partion):
        """
        变异操作
        entity: 变异的个体
        partion: 变异时的编码的比例 4 = 40% 以此类推
        return: 变异后的个体
        """
        pass

    def roulette(self, selectProb):
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

    def ga(self, costFun, seqLen, entityCount=100, iters=50):
        """
        遗传算法找到最优序列
        costFun: 计算单个个体的损失函数
        seqLen: 单个个体的编码长度
        entityCount: 种群中的个体数量
        iters: 遗传算法迭代的次数

        return: 最优的编码以及它的适应度值
        """

        # 生成初始种群
        # seqLen = self.__codeLength
        population = self.genPopulation(entityCount)  # 生成初始种群

        # 计算整个种群的适应度值
        fitnessList = self.allCost(costFun, population)
        # print(fitnessList)
        # print(fitnessList)

        # 找到当前种群中最优的个体 
        bestEntityIndex = fitnessList.index(min(fitnessList))  # 几下最优个体在种群中的索引值
        best10Index = np.array(fitnessList).argsort()[0: math.ceil(len(fitnessList)*0.1): 1]
        print(population[bestEntityIndex], fitnessList[bestEntityIndex])

        # 创建一个列表来保存每次迭代中种群中的最优适应度值 
        fitnessHistory = []

        # 遗传算法：
        for i in range(iters):  # 迭代次数
            # print(population)

            # 根据适应度值计算每一个个体被选中的概率()
            selectProb = self.calSelectProb(fitnessList)
            # print(selectProb)

            # 生成新的种群
            population = self.genOffspring(costFun, population, selectProb, fitnessList, best10Index)

            # 计算新种群中所有个体的适应度值()
            fitnessList = self.allCost(costFun, population)

            bestEntityIndex = fitnessList.index(min(fitnessList))
            best10Index = np.array(fitnessList).argsort()[0:10:1]

            fitnessHistory.append(min(fitnessList))
            print(min(fitnessList))

            pass

        # print(fitnessHistory)
        print(population)
        # print("Best:\n", population[bestEntityIndex], "\n", fitnessList[bestEntityIndex])
        result = self.outputGenerator(population[bestEntityIndex], fitnessList[bestEntityIndex])
        print(result)

        # 写入数据库
        # data = [result['R'], result['S'], result['H'], result['C'], result['duration']]
        # insertDeepLearningData(data)

        pass


####################################################################
def testCost(pop):
    fit = 0
    print(pop)
    for i in range(len(pop['d'])):
        r, s, h, c = 0, 0, 0, 0
        r = sum(pop['r'][i].values())
        s = sum(pop['s'][i].values())
        h = sum(pop['h'][i].values())
        c = sum(pop['c'][i].values())
        fit += int(calFitness([r, s, h, c]))
    return fit
    pass


optAlgo = OptimizationAlgorithm(typeCount=29, days=30)
# # print(optAlgo.ddjData)
optAlgo.ga(testCost, 84, 5, 100)

# optAlgo.ga(testCost, 84, 300, 500)
calFitness([250, 251, 251, 250])

####################################################################
