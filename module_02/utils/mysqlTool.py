import string
import ast
import pymysql
import json

myHost = '101.43.47.172'
myPort = 3306
userName = 'root'
pwd = '0920'
database = 'whpu'
charset = 'utf8'

db = pymysql.connect(host=myHost, port=myPort, user=userName, password=pwd, database=database, charset=charset)
cursor = db.cursor()


def queryAll():  # 查询全部
    sql = "select * from szls"
    cursor.execute(sql)
    fetchall = cursor.fetchall()
    for i in range(len(fetchall)):
        print(fetchall[i])
    db.close()


def insertData(data):  # 插入
    sql = "INSERT INTO szls (R,S,H,C,RH1,S1,C1,RH2,S2,C2,RH3,S3,C3,RH4,S4,C4,RH5,S5,C5,RH6,S6,C6,fitness) " \
          "VALUES( %d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%lf)" \
          % (
              data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10],
              data[11], data[12], data[13], data[14], data[15], data[16], data[17], data[18], data[19], data[20],
              data[21], data[22])
    cursor.execute(sql)
    db.commit()
    print("插入成功！！！")
    db.close()


def findFitness(data):  # 根据R,S,H,C查找第一个匹配的fitness
    sql = "select fitness from szls where R = %d and S = %d and H = %d and C = %d" % (
        data[0], data[1], data[2], data[3])
    cursor.execute(sql)
    fetchall = cursor.fetchall()
    db.close()
    return fetchall[0][0]


def deleteByMinId(limit):
    return


def selectCrossPoints(type: int):
    """
    type: 0 for coordinate and 1 for id
    """
    if type == 0:
        sql = "SELECT A.x as start_x, A.y as start_y, A.z as start_z, B.x as end_x, B.y as end_y, B.z as end_z, B.runtime as runtime FROM likuInfos_crossPoints as A, likuInfos_crossPoints_downPoint as B WHERE A.id = B.belongCpID;"
    if type == 1:
        sql = "SELECT A.vice_id as start, B.vice_id, B.runtime as end FROM likuInfos_crossPoints as A, likuInfos_crossPoints_downPoint as B WHERE A.id = B.belongCpID;"
    cursor.execute(sql)
    data = cursor.fetchall()
    db.close()
    return data


def readJSON():
    f = open("C:\\Users\\A\\Desktop\\产线数据.json", encoding="utf-8")
    file = json.load(f)
    return file


## 0426
def insertProductionLineData():
    flag = getMaxFlag() + 1
    i = 1
    f = readJSON()
    info = f["info"]
    for data in info:
        innerId = data["id"]
        data = str(data)
        print(data)
        sql = "insert into production_line_data (data, sign, inner_id, flag) VALUES " \
              "('%s', '产线数据', '%s', %d)" % (pymysql.converters.escape_string(data), innerId, flag)
        cursor.execute(sql)
        if i % 10 == 0:
            print(i)
        i = i + 1
    db.commit()
    print("插入成功！")


def getProductionLineData():
    flag = getMaxFlag()
    res = []
    sql = "select data from production_line_data where sign = '产线数据' and flag = %d" % flag
    cursor.execute(sql)
    fetchall = cursor.fetchall()
    for data in fetchall:
        tmp = ast.literal_eval(data[0])
        # print(tmp)
        res.append(tmp)
    return res


def getStacks():
    flag = getMaxFlag()
    res = []
    sql = "select data from production_line_data where inner_id like '%堆垛机' and flag = %d" % flag
    cursor.execute(sql)
    fetchall = cursor.fetchall()
    for data in fetchall:
        tmp = ast.literal_eval(data[0])
        # print(tmp)
        res.append(tmp)
    return res


def getMaxFlag():
    sql = "select max(flag) from production_line_data"
    cursor.execute(sql)
    fetchAll = cursor.fetchall()
    if fetchAll[0][0] is None:
        return 0
    sign = fetchAll[0][0]
    return sign


# if __name__ == '__main__':
#     queryAll()
