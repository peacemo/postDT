from utils.sqlTools import *
from utils.planGenerator import *
import copy as cp
import random as rd
from utils.optimizer import *


def main():
    typeCount = 29
    days = 35
    planGenerator = PlanGenerator(typeCount, days, 16119)
    plan = planGenerator.getAFkPlan()
    print(plan)

#     optAlgo = OptimizationAlgorithm(typeCount=29, days=30)
# # # print(optAlgo.ddjData)
#     optAlgo.ga(testCost, 50, 100)
    pass


if __name__ == "__main__":
    # execute only if run as a script
    main()
