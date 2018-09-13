#coding:utf-8

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient['netease_music']
mycol = mydb['users']

dblist = myclient.list_database_names()
if 'netease_music' in dblist:
    print "数据库已存在！"

def write(result):
    mycol.insert_one(result)
