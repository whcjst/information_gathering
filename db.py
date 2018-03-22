# -*- coding: utf-8 -*-
# @Time    : 2017/12/27 13:27
# @Author  : ha1g0
# @Site    : http://whc.dropsec.xyz
# @File    : db.py


from pymongo import MongoClient

class db():
    '''
    Mongodb操作
    '''
    def __init__(self,db_name,db_set):
        #连接数据库，并指定库和集合
        self._con = MongoClient('localhost',27017) #_con 连接数据库的句柄 私有变量不允许访问
        # self.db = self._con.test #库
        # self.set = self.db.test1 #集合
        self.db = self._con[db_name]
        self.set = self.db[db_set]

    def insert(self,text):
        #把信息插入test.test1中
        self.set.insert(text)

    def save(self,text):
        #save 跟insert的区别就是当插入已有数据时insert会报错
        self.set.save(text)

    def find(self):
        return self.set.find()

    def find_one(self,top_domain):
        return self.set.find_one({"top_domain":top_domain})


class selectDB(db):
    '''
    继承 db.db
    从数据库中select所有数据
    '''
    def __init__(self,db_name,db_set):
        super(selectDB,self).__init__(db_name,db_set)
        self.information = []

    def find(self):
        cursor = super(selectDB,self).find()
        for item in cursor:
            self.information.append(item)
        return self.information

    def find_one(self,json):
        return self.set.find_one(json)
