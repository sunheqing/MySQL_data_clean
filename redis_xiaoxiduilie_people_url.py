#coding=utf-8
import pymysql
import redis
redis_db = redis.StrictRedis(host='localhost', db=5)
prodcons_queue = 'task:people_net_url:queue'
rcon = redis_db

db = pymysql.connect(host="localhost", user="root", password="123456", db="sun", port=3306, charset='utf8')
cursor = db.cursor()
def sql(url):
    sql_talk = "INSERT into sun.user set email='{0}';".format(url)
    try:
        row = cursor.execute(sql_talk)
        db.commit()
        print sql_talk
        print u"受影响的行数：" + str(row) + u" 行  （检查人民网隐藏数据）"
    except:
        db.rollback()
        print u"执行错误，已经回滚，请检查数据库！"


while True:
    task_url = rcon.blpop(prodcons_queue, 0)[1]
    sql(task_url)
