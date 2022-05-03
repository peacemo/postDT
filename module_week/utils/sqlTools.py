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


def getCargoOld(): 
    """
    查询立库中陈品的数量，并按照类型统计数量
    """
    sql = "SELECT type, count(*) FROM `goods_locations_info` WHERE s1=1 and s2=1 and sign=(select max(sign) from `goods_locations_info`) GROUP BY type"
    cursor.execute(sql)
    fetchall = cursor.fetchall()
    db.close()
    return fetchall


def getCargoNew():  
    """
    查询立库中新品的数量，并按照类型统计数量
    """
    sql = "SELECT type, count(*) FROM `goods_locations_info` WHERE s1=0 and s2=1 and sign=(select max(sign) from `goods_locations_info`) GROUP BY type"
    cursor.execute(sql)
    fetchall = cursor.fetchall()
    db.close()
    return fetchall
    
    
def getCargoEmpty():  
    """
    查询立库中空货位的数量
    """
    sql = "SELECT type, count(*) FROM `goods_locations_info` WHERE s1=0 and s2=0 and sign=(select max(sign) from `goods_locations_info`) GROUP BY type"
    cursor.execute(sql)
    fetchall = cursor.fetchall()
    db.close()
    return fetchall
