from utils.sqlTools import *
import copy as cp
import random as rd
import json
import sys

class PlanGenerator:
    def __init__(self, typeCount, days, L) -> None:
        """
        对象初始化
        typeCount: 总的货物类型
        days: 总的天数
        L: 立库容量
        """
        self.__typeCount = typeCount
        self.__days = days
        self.__L = 16119
        pass


    def getAFkPlan(self):
        """
        获取一个月度计划

        return: 生成的月度计划，类型为字典
        """
        data = self.getData()
        if self.checkByMon(data):
            R = self.genR(data)
            CJ = self.genCJ(data, R)
            data['ruKu'] = R
            data['chouJian'] = CJ
            monPlan = self.genPlan(data)
            monPlan = self.adjustPlan(monPlan, data)
            output = self.genOutput(monPlan)

            # with open('monPlan.json', 'w') as fp:
            #     json.dump(output, fp,  indent=4)
            
            return output
            pass
        else:
            print('月度任务总量不可行')


    def toList(inputDict: dict):
        for key in inputDict.keys():
            pass
        result = []
        return result


    def getData(self):
        """
        从数据库中获取各种所需要的数据
        """
        mysqlTools = MysqlTools()
        cargoOld = mysqlTools.getCargoOld(self.__typeCount)
        cargoNew = mysqlTools.getCargoNew(self.__typeCount)
        cargoEmpty = mysqlTools.getCargoEmpty()

        whOld = mysqlTools.getWarehouseOld(self.__typeCount)
        whNew = mysqlTools.getWarehouseNew(self.__typeCount)
        whEmpty = mysqlTools.getWarehouseEmpty()

        arrivalInfo = mysqlTools.getArrivalInfo(self.__typeCount)
        checkInfo = mysqlTools.getCheckInfo(self.__typeCount)
        depositeInfo = mysqlTools.getDepositeInfo(self.__typeCount)

        # print(cargoOld, '\n', cargoNew, '\n', cargoEmpty, '\n', whOld, '\n', whNew, '\n', whEmpty, '\n', arrivalInfo, '\n', checkInfo, '\n', depositeInfo)

        return {
            'cargoOld' : cargoOld,
            'cargoNew': cargoNew,
            'cargoEmpty': cargoEmpty,
            'whOld': whOld,
            'whNew': whNew,
            'whEmpty': whEmpty,
            'arrivalInfo': arrivalInfo,
            'checkInfo': checkInfo,
            'depositeInfo': depositeInfo
        }
        pass


    def checkByMon(self, monData: dict):
        """
        检查月度计划的总量是否可行
        monData: 原始的月度计划的字典（到检配，以及其他状态参数）

        return: 是否可行 True / False  (bool)
        """
        try:
            S = monData['checkInfo']
            L_1 = monData['cargoNew']
            L_2 = monData['cargoOld']
            C = monData['depositeInfo']
            D = monData['arrivalInfo']
            P_1 = monData['whNew']
            P_2 = monData['whOld']
        except:
            return False

        if len(S) != len(L_2) or len(S) != len(C) or len(L_2) != len(C):
            # 若输入的数据中，对应的资产种类数不匹配，则直接返回 False
            return False
        
        for assetType in range(1, len(S)):
            if S[assetType] + L_2[assetType] >= C[assetType] and \
                D[assetType] + P_1[assetType] + P_2[assetType] + L_1[assetType] >= S[assetType]:
                continue
            else: 
                return False

        return True


    def genR(self, monData: dict):
        """
        生成入库计划
        monData: 原始的月度计划的字典（到检配，以及其他状态参数）

        return: 月度每日的入库计划 list
        """
        try:
            S = monData['checkInfo']
            L_1 = monData['cargoNew']
            L_2 = monData['cargoOld']
            C = monData['depositeInfo']
            D = monData['arrivalInfo']
            P_1 = monData['whNew']
            P_2 = monData['whOld']
        except:
            return False

        R = [0] * len(S)
        
        for assetType in range(1, len(S)):
            lb = S[assetType] - L_1[assetType] if S[assetType] - L_1[assetType] >= 0 else 0
            R[assetType] = rd.randint(lb, D[assetType] + P_1[assetType] + P_2[assetType])
            if C[assetType] <= S[assetType]:
                R[assetType] = rd.randint(lb, S[assetType])
        
        return R
        
        pass


    def genCJ(self, monData: dict, R):
        """
        生成月度的每日抽检计划
        monData: 原始的月度计划的字典（到检配，以及其他状态参数）

        return: 生成的月度每日抽检计划 list
        """
        try:
            S = monData['checkInfo']
            L_1 = monData['cargoNew']
            L_2 = monData['cargoOld']
            C = monData['depositeInfo']
            D = monData['arrivalInfo']
            P_1 = monData['whNew']
            P_2 = monData['whOld']
        except:
            return False

        CJ = [0] * len(S)
        
        for assetType in range(len(S)):
            lb = R[assetType] - P_2[assetType] if R[assetType] - P_2[assetType] >=0 else 0
            CJ[assetType] = rd.randint(R[assetType] - P_2[assetType], D[assetType] + P_1[assetType])
        
        return CJ 
        
        pass


    def genPlan(self, monData):
        """
        生成月度计划
        monData: 原计划

        return: 生成的优化计划
        """
        try:
            S = monData['checkInfo']
            L_1 = monData['cargoNew']
            L_2 = monData['cargoOld']
            C = monData['depositeInfo']
            D = monData['arrivalInfo']
            P_1 = monData['whNew']
            P_2 = monData['whOld']
            R = monData['ruKu']
            CJ = monData['chouJian']
        except:
            return False
        
        d = [ [0] * (self.__typeCount+1) for i in range(30)]
        cj = [ [0] * (self.__typeCount+1) for i in range(30)]
        r = [ [0] * (self.__typeCount+1) for i in range(30)]
        s = [ [0] * (self.__typeCount+1) for i in range(30)]
        h = [ [0] * (self.__typeCount+1) for i in range(30)]
        c = [ [0] * (self.__typeCount+1) for i in range(30)]

        for dayi in range(30):  # 对计划总量进行均分
            for type in range(len(S)):
                d[dayi][type] = round(D[type] / 30)
                cj[dayi][type] = round(CJ[type] / 30)
                r[dayi][type] = round(R[type] / 30)
                s[dayi][type] = round(S[type] / 30)
                h[dayi][type] = s[dayi][type]
                c[dayi][type] = round(C[type] / 30)

                if type == 12: r[dayi][type] = 0

        return {
            'd': d,
            'cj': cj,
            'r': r,
            's': s,
            'h': h,
            'c': c
        }


        pass


    def adjustPlan(self, monPlan: dict, monData: dict):
        """
        调整生成的月度计划，保证可行性
        monPlan: 生成的月度计划
        monData: 原始的月度计划及其库存状态

        return: 调整后的 monPlan

        """
        try:
            S = monData['checkInfo']
            L_1 = monData['cargoNew']
            L_2 = monData['cargoOld']
            C = monData['depositeInfo']
            D = monData['arrivalInfo']
            P_1 = monData['whNew']
            P_2 = monData['whOld']
            R = monData['ruKu']
            CJ = monData['chouJian']
            H_0 = [0] * (self.__typeCount + 1)
        except:
            return False
        
        try:
            r = monPlan['r']
            cj = monPlan['cj']
            d =  monPlan['d']
            s = monPlan['s']
            h = monPlan['h']
            c = monPlan['c']

        except:
            return False

        for day in range(self.__days):  # 按天遍历
            for type in range(1, self.__typeCount + 1):  # 按每天的每种类型遍历
                if r[day][type] > P_2[type]:  # 如果不满足 入库<=平库已抽检
                    # print('----in if 1')
                    if day < self.__days-1:
                        r[day+1][type] += r[day][type] - P_2[type]  # 则将今天的入库不够的部分移动到后一天
                        r[day][type] = P_2[type]  # 并把今天所有的平库已抽检都入库
                    else: 
                        r[day][type] = P_2[type]

                if cj[day][type] > P_1[type] + d[day][type]:
                    # print('----in if 2')
                    if day < self.__days-1:
                        cj[day+1][type] += cj[day][type] - (P_1[type] + d[day][type])  
                        cj[day][type] = P_1[type] + d[day][type]  
                    else: 
                        cj[day][type] = P_1[type] + d[day][type]
                
                P_2[type] = P_2[type] + cj[day][type] - r[day][type]
                P_1[type] = P_1[type] + d[day][type] - cj[day][type]


                if s[day][type] > L_1[type]:
                    # print('----in if 3')
                    if day < self.__days-1:
                        s[day+1][type] += s[day][type] - (L_1[type])  
                        s[day][type] = L_1[type] 
                    else: 
                        s[day][type] = L_1[type]
                if day > 0:
                    if s[day][type] < r[day-1][type]:
                        s[day][type] = r[day][type]

                L_1[type] = L_1[type] + r[day][type] - s[day][type]


                # FIXME 这里如果调整，回库就和检定不相等，算法无法运行
                # if monPlan['h'][day][type] > H_0[type] + monPlan['s'][day][type]:
                #     print('----in if 4')
                #     monPlan['h'][day][type] = H_0[type] + monPlan['s'][day][type]
                
                # H_0[type] = H_0[type] + monPlan['s'][day][type] - monPlan['h'][day][type]
                h[day][type] = s[day][type]
                H_0[type] = H_0[type] + s[day][type] - h[day][type]


                if c[day][type] > L_2[type]:
                    # print('----in if 5')
                    if day < self.__days-1:
                        c[day+1][type] += c[day][type] - (L_2[type])  
                        c[day][type] = L_2[type] 
                    else: 
                        c[day][type] = L_2[type]
                if day > 0:
                    if c[day][type] < h[day-1][type]:
                        c[day][type] = int(h[day][type] * (rd.randint(90, 100) / 100.0))

                L_2[type] = L_2[type] + h[day][type] - c[day][type]


                # 立库库存总数约束
                if (L_1[type] + L_2[type] + r[day][type] - s[day][type] + h[day][type] - c[day][type]) > self.__L:
                    print("立库爆仓")
                    sys.exit(0)

                # TODO 检定量总数约束

            
        # print(monPlan)
        return monPlan
        pass


    def genOutput(self, monPlan):
        """
        格式化输出
        monPlan: 生成的月度计划

        return: 格式化字典输出
        """
        # print(monPlan)
        d = []
        cj = []
        r = []
        s = []
        h = []
        c = []

        for i in range(self.__days):
            dDict = {}
            dDict['14'] = monPlan['d'][i][14]
            dDict['10'] = monPlan['d'][i][10]
            dDict['12'] = monPlan['d'][i][12]
            dDict['13'] = monPlan['d'][i][13]
            dDict['11'] = monPlan['d'][i][11]
            dDict['15'] = monPlan['d'][i][15]
            dDict['16'] = monPlan['d'][i][16]
            d.append(dDict)

            cjDict = {}
            cjDict['14'] = monPlan['cj'][i][14]
            cjDict['10'] = monPlan['cj'][i][10]
            cjDict['12'] = monPlan['cj'][i][12]
            cjDict['13'] = monPlan['cj'][i][13]
            cjDict['11'] = monPlan['cj'][i][11]
            cjDict['15'] = monPlan['cj'][i][15]
            cjDict['16'] = monPlan['cj'][i][16]
            cj.append(cjDict)

            rDict = {}
            rDict['14'] = monPlan['r'][i][14]
            rDict['10'] = monPlan['r'][i][10]
            rDict['12'] = monPlan['r'][i][12]
            rDict['13'] = monPlan['r'][i][13]
            rDict['11'] = monPlan['r'][i][11]
            rDict['15'] = monPlan['r'][i][15]
            rDict['16'] = monPlan['r'][i][16]
            r.append(rDict)

            sDict = {}
            sDict['14'] = monPlan['s'][i][14]
            sDict['10'] = monPlan['s'][i][10]
            sDict['12'] = monPlan['s'][i][12]
            sDict['13'] = monPlan['s'][i][13]
            sDict['11'] = monPlan['s'][i][11]
            sDict['15'] = monPlan['s'][i][15]
            sDict['16'] = monPlan['s'][i][16]
            s.append(sDict)

            hDict = {}
            hDict['14'] = monPlan['h'][i][14]
            hDict['10'] = monPlan['h'][i][10]
            hDict['12'] = monPlan['h'][i][12]
            hDict['13'] = monPlan['h'][i][13]
            hDict['11'] = monPlan['h'][i][11]
            hDict['15'] = monPlan['h'][i][15]
            hDict['16'] = monPlan['h'][i][16]
            h.append(hDict)

            cDict = {}
            cDict['14'] = monPlan['c'][i][14]
            cDict['10'] = monPlan['c'][i][10]
            cDict['12'] = monPlan['c'][i][12]
            cDict['13'] = monPlan['c'][i][13]
            cDict['11'] = monPlan['c'][i][11]
            cDict['15'] = monPlan['c'][i][15]
            cDict['16'] = monPlan['c'][i][16]
            c.append(cDict)
        
        return {
            'd': d,
            'cj': cj,
            'r': r,
            's': s,
            'h': h,
            'c': c
        }
        pass