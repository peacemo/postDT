from utils.sqlTools import *
from utils.planGenerator import *
import copy as cp
import random as rd


def main():
    typeCount = 29
    days = 30
    planGenerator = PlanGenerator(typeCount, days, 16119)
    plan = planGenerator.getAFkPlan()
    print(plan)
    pass


if __name__ == "__main__":
    # execute only if run as a script
    main()
