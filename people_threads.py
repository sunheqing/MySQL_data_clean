#coding=utf-8

import threading
import requests
import redis
from time import sleep

redis_db = redis.StrictRedis(host='localhost', db=5)
prodcons_queue = 'task:people_net_url:queue'
rcon = redis_db


def process(x):
    k=((x-1)/100)+1
    x=x+20000



    j=0
    for i in range(x, x+100):
        url = "http://ldzl.people.com.cn/dfzlk/front/personPage" + str(i) + ".htm"
        resp = requests.get(url).status_code

        if resp==200:
            rcon.lpush(prodcons_queue, url)
            j+=1


    print "线程"+str(k)+"完成任务"+str(j)+"个"

##########
'''
class Thread(threading.Thread):
    def __init__(self, i):
        threading.Thread.__init__(self)
        self.name = 'spider_threading - ' + str(i+1)

    def run(self):
        print 'running --- ' + self.name
        process()
'''
##############
class Controller(threading.Thread):
    def __init__(self, threads):
        threading.Thread.__init__(self)
        self.daemon = True
        self.threadList = threads

    def run(self):
        for each in self.threadList:
            each.start()
        while True:
            for a in xrange(10):
                if not self.threadList[a].isAlive():
                    self.threadList[a] = threading.Thread(target=process, args=(a*2+1,))
                    self.threadList[a].start()
                sleep(1000)  # 每1000秒判断一下

if __name__ == '__main__':
    threads = []
    for i in xrange(10):
        t = threading.Thread(target=process, args=(i*100+1,))
        threads.append(t)
    c = Controller(threads)
    c.start()
    c.join()


