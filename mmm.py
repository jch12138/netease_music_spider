#coding:utf-8

import json
import pandas as pd
import datetime
import re

def calage(birthday):
    birthday = pd.to_datetime(birthday)
    year = datetime.datetime.today().year
    return str(year - birthday.year)

def locate(location):
    location = location[5:]
    #print (type(location))
    m = re.match('^[\u4e00-\u9fa5]+', location)
    return m.group(0)


gender = {'男':0,'女':0}
location = {"福建省": 0, "台湾省": 0, "香港": 0, "新疆": 0, "广东省": 0, "重庆市": 0, "甘肃省": 0, "四川省": 0, "河南省": 0, "安徽省": 0, "海外": 0, "澳门": 0, "江苏省": 0, "北京市": 0, "湖南省": 0, "浙江省": 0, "广西": 0, "贵州省": 0, "陕西省": 0, "山西省": 0, "宁夏": 0, "海南省": 0, "青海省": 0, "天津市": 0, "内蒙古": 0, "辽宁省": 0, "江西省": 0, "黑龙江省": 0, "吉林省": 0, "河北省": 0, "云南省": 0, "山东省": 0, "西藏": 0, "上海市": 0, "湖北省": 0}
age = {}

with open ('user.json','r',encoding='utf-8') as f:
    User = f.readlines()
    n = 0

    for line in User:
        user = json.loads(line)
        try:
            age[calage(user['birthday'])] += 1
        except:
            age[calage(user['birthday'])] = 1
        gender[user['gender']] += 1
        vv = user['location']
        #print(type(vv))
        oo = locate(vv)
        print(type(oo))
        location[oo] += 1
    print (gender)
    print (location)
    print (age)


'''
fp = codecs.open('newdata.json', 'a', encoding='utf-8')
        json.dump(user, fp,ensure_ascii=False)
        fp.write(',\n')
        f.close()
        
        '''



