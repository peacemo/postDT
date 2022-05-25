import random as rd
import numpy as np
import math
import copy as cp

from module_week.preMod.test import calFitness
from module_week.utils.planGenerator import PlanGenerator


class OptimizationAlgorithm:
    def __init__(self, typeCount, days) -> None:
        """初始化函数

        Args:
            typeCount (int): 货物总索引数
            days (int): 计划总天数
        """
        self.__typeCount = typeCount
        self.__days = days
        pass

    # @property
    # def ddjData

    def outputGenerator(self, sequence, fitness):
        return ...
        pass

    def genPopulation(self, entityCount) -> list:
        """生成初始总群

        Args:
            entityCount (int): 种群规模、个体数

        Returns:
            list: 由 entitiCount 个个体构成的列表（整个种群）
        """
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
        """计算整个种群中每个个体的适应度值

        Args:
            costFun (fun): 单个个体的适应度值计算函数
            population (list): 整个种群

        Returns:
            list: 种群中每个个体的适应度值所构成的列表
        """
        fitnessList = [-1] * len(population)  # 初始化适应度值列表，用于记录每个个体对应的适应度值
        for i in range(len(fitnessList)):
            # print(population[i])
            fitnessList[i] = costFun(population[i])

        return fitnessList

    def calSelectProb(self, fitnessList: list) -> list:
        """计算每个个体被选中的概率

        Args:
            fitnessList (list): 适应度值列表

        Returns:
            list: 每个个体被选中的概率
        """
        # fitnessAry = np.array(fitnessList)
        fitnessAry = 1 / np.array(fitnessList)
        p = (fitnessAry / sum(fitnessAry))
        # p = (max(fitnessAry) - fitnessAry) / (max(fitnessAry) - min(fitnessAry))
        return p.tolist()
        pass

    def genOffspring(self, costFun: function, population: list, selectProb: list, fitnessList: list, best10Index: list) -> list:
        """生成新的种群

        Args:
            costFun (function): 单个个体的损失计算函数
            population (list): 整个种群
            selectProb (list): 每个个体的被选择概率
            fitnessList (list): 群体的适应度值
            best10Index (list): 群体中最优的个体的索引

        Returns:
            list: 新的种群
        """
        offsprings = []  # 后代个体
        for index in best10Index:
            offsprings.append(population[index])

        while len(offsprings) < len(population):
            parentAIndex = self.roulette(selectProb)
            parentBIndex = rd.choice(best10Index.tolist())
            while parentAIndex == parentBIndex:
                parentAIndex = self.roulette(selectProb)
            parents = [population[parentAIndex], population[parentBIndex]]

            offspring = self.hybrid(costFun=costFun, population=population, parents=parents, fitnessList=fitnessList, partion = (int(self.__days / 10) if int(self.__days / 10) > 0 else 1))

            offsprings.append(offspring)
            pass

        return offsprings
        pass

    def hybrid(self, parents: list, partion: int) -> list:
        """两个个体交叉

        Args:
            parents (list): 进行交叉的两个双亲
            partion (int): 交叉操作所需要进行交叉的序列长度的百分比，
                            值为 int，若长度为 30%，则 partition=3

        Returns:
            list: 一个新的个体
        """
        planGrt = PlanGenerator(self.__typeCount, self.__days, 16119)
        adjustDays = rd.choices([day for day in range(self.__days)], k=partion)
        # mother, father = population[parents[0]], population[parents[1]]
        parentA, parentB = parents[0], parents[1]
        child = cp.deepcopy(parentA)

        for day in adjustDays:
            exOption = rd.choice(['cj', 'r'])
            child[exOption][day] = parentB[exOption][day]
            pass
        planGrt.adjustPlan(child, cp.deepcopy(planGrt.data))

        # if rd.random() < 0.1:
        #     child = self.mutate(child, partion = (int(self.__days / 10) if int(self.__days / 2) > 0 else 1))

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

    def roulette(self, selectProb: list) -> int:
        """轮盘赌选择一个个体的索引值

        Args:
            selectProb (list): 种群中每个个体的被选择概率

        Returns:
            int: 被选中的个体的索引值
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

    def ga(self, costFun: function, entityCount=100, iters=50):
        """遗传算法找到最优序列

        Args:
            costFun (function): 计算单个个体的损失函数
            entityCount (int, optional): 种群中的个体数量. Defaults to 100.
            iters (int, optional): 遗传算法迭代的次数. Defaults to 50.
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
    # print(pop)
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
optAlgo.ga(testCost, 50, 100)

# optAlgo.ga(testCost, 84, 300, 500)
# calFitness([250, 251, 251, 250])

####################################################################
