import string
import pymysql

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


# if __name__ == '__main__':
#     queryAll()
