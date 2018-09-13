#coding:utf-8

import requests
from useragent import USER_AGENTS
from webapi import webapi
import json
from jiami import get_data
import random
from lxml import etree
import time
import math
import re
from idpool import ID_pool


s = requests.session()
s.keep_alive = False

class spider():
    def __init__(self,id):#个人信息初始化
        self.userId = id
        self.nickname = ''
        self.lv = 0
        self.dynamic = 0
        self.gender = "None"
        self.follows = 0
        self.followeds = 0
        self.signature = ''
        self.createdplaylistCount = 0
        self.collectplaylistCount = 0
        self.location = ''
        self.birthday = ''
        self.totallistened = 0
        self.favorsonglist = {}
        self.createdplaylistDict = []
        self.collectplaylistDict = []
        self.followsList = []
        self.followedsList = []
        self.info = {}



    def timefomat(self,s):
        timeStamp = s
        timeStamp /= 1000.0
        timeArray = time.localtime(timeStamp)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return otherStyleTime

    def get_proxy(self,n):
        #print '2'
        url = "http://127.0.0.1:8000/?count=1&protocol=2"
        result = requests.get(url).text
        #print '2'
        ip_ports = json.loads(result)
        #print ip_ports
        ip = "1.1.1.1"
        port = -1
        while ip == "1.1.1.1" and port == -1:
            try:
                ip = ip_ports[0][0]
                port = ip_ports[0][1]
            except:
                print 'ip池已空，填充中',
                time.sleep(30)
        #proxy = {"https":"%s" % ip,"http":"%s" % ip}
        return ip, port

    def delete_ip(self,ip):
        requests.get("http://127.0.0.1:8000/delete?ip=%s" % ip)



    def get_json(self, data, url, header,proxy):# post请求
        #proxy = self.get_proxy()
        jsons = requests.post(url, data=data, headers=header, proxies=proxy, timeout=5)

        return jsons

    def get_useragent(self):
        useragent = random.choice(USER_AGENTS)
        return useragent

    def get_basic_info(self):
        pattern = re.compile(r'\d+')
        #print '1'

        headers = {"User-Agent":self.get_useragent(),"Connection":'close'}
        url = webapi(7)+"?id=%s" % self.userId
        while True:
            ip, port = self.get_proxy(1)
            proxy = {
                'http': 'http://%s:%s' % (ip, port),
                'https': 'http://%s:%s' % (ip, port)
            }

            try:
                home = requests.get(url,headers = headers,proxies = proxy, timeout=5)
                #print home.status_code
                if home.status_code == 200:
                    break
            except Exception as e:
                #print e,
                self.delete_ip(ip)
            #print home.content



        html = etree.HTML(home.content)
        check_ID = False
        try:
            check_account = html.xpath("//div[@class = 'g-bd g-bd-full']/div/div/p/text()")
            #check_account = str(check_account)
            if check_account:
                check_ID = True

            nickname = html.xpath("//dd/div[@class ='name f-cb']/div/h2/span[1]/text()")
            if nickname:
                self.nickname = nickname[0]

            lv = html.xpath("//dd/div[@class ='name f-cb']/div/h2/span[3]/text()")
            if lv:
                self.lv = lv

            gender = html.xpath("//dd/div[@class ='name f-cb']/div[@class = 'f-cb']/h2/i/@class")
            if gender:
                self.gender = "男" if gender[0] == 'icn u-icn u-icn-01' else "女"

            dynamic = html.xpath("//dd/ul/li[1]/a/strong/text()")
            if dynamic:
                self.dynamic = dynamic[0]

            follows = html.xpath("//dd/ul/li[2]/a/strong/text()")
            if follows:
                self.follows = follows[0]

            followeds = html.xpath("//dd/ul/li[3]/a/strong/text()")
            if followeds:
                self.followeds = followeds[0]

            try:
                self.location = html.xpath("//dd/div[@class = 'inf s-fc3']/span[1]/text()")[0]
            except:
                self.location = ''

            try:
                self.birthday = self.timefomat(int(html.xpath("//dd/div[@class = 'inf s-fc3']/span[2]/@data-age")[0]))
            except:
                self.birthday = ''

            try:
                self.signature = html.xpath("//div[@class='inf s-fc3 f-brk']/text()")[0]
            except:
                self.signature = ''

            try:
                self.totallistened = html.xpath("//div[@id = 'rHeader']/h4/text()")[0]
            except:
                self.totallistened = ''

            try:
                s = html.xpath("//div[@id='cHeader']/h3/span/text()")[0]
                temp = pattern.findall(s)[-1]
                self.createdplaylistCount = int(temp)
            except:
                #print 'e'
                self.createdplaylistCount = 0

            try:
                s = html.xpath("//div[@id='sHeader']/h3/span/text()")[0]
                temp = pattern.findall(s)[-1]
                self.collectplaylistCount = int(temp)
            except:
                self.collectplaylistCount = 0

        except Exception as e:
            #print e
            pass

        if check_ID == True:
            return -1
        if self.gender == "None":
            return False
        return True

    def get_follow(self):#获取粉丝与关注者
        followeds = int(self.followeds)
        follows = int(self.follows)
        page = int(math.ceil(followeds / 20.0))

        followed = []
        for i in range(page):
            #print "正在爬取第%s页粉丝" % (i + 1)
            canshu = get_data('{"userId":"%s","offset":"%s","total":"%s","limit":"20","csrf_token":""}' % (self.userId, 20 * i, 'true' if i == 0 else 'false'))
            headers = {"User-Agent":self.get_useragent(),"Referer":"https://music.163.com/user/fans?id=%s"%self.userId,"Host":'music.163.com',"Connection":'close'}
            while True:
                ip, port = self.get_proxy(0)
                proxy = {
                    'http':'%s:%s' % (ip, port)
                }
                try:
                    #print '1'
                    result = self.get_json(canshu, webapi(3), headers, proxy)
                    #print result.status_code
                    if result.status_code == requests.codes.ok:
                        result = result.content
                        result = json.loads(result)
                        break
                except Exception as e:
                    #print e
                    self.delete_ip(ip)

            #print result
            #num = 20 if i < (page - 1) else (followeds - i *20)
            for j in result['followeds']:
                s = {'name':j["nickname"],'id':j["userId"]}
                followed.append(s)
                ID_pool.put(s['id'])

        self.followedsList = followed
        page = int(math.ceil(follows / 20.0))

        follow = []
        for i in range(page):
            #print "正在爬取第%s页关注" % (i + 1)
            canshu = get_data('{"uid":"%s","offset":"%s","total":"%s","limit":"20","csrf_token":""}' % (
            self.userId, 20 * i, 'true' if i == 0 else 'false'))
            headers = {"User-Agent": self.get_useragent(),
                       "Referer": "https://music.163.com/user/fans?id=%s" % self.userId,
                       "Host": 'music.163.com',
                       "Connection":'close'
                       }
            while True:
                ip, port = self.get_proxy(0)
                proxy = {
                    'http': 'http://%s:%s' % (ip, port),
                    'https': 'http://%s:%s' % (ip, port)
                }
                try:
                    result = self.get_json(canshu, webapi(4)%self.userId, headers, proxy)
                    #print result.status_code
                    if result.status_code == 200:
                        result = result.content
                        result = json.loads(result)
                        break
                except Exception as e:
                    #print e,
                    self.delete_ip(ip)

            #num = 20 if i < (page - 1) else (follows - i * 20)
            for j in result['follow']:
                s = {'name': j["nickname"], 'id': j["userId"]}
                #ID_pool.put(s['id'])
                follow.append(s)

        self.followsList = follow

        if (followeds != 0 and not followed) or (follows != 0 and not follow):
            return False
        return True

    def get_playlist(self):#获取歌单信息
        create_playlist_count = self.createdplaylistCount
        #print create_playlist_count
        collect_playlist_count = self.collectplaylistCount
        #print collect_playlist_count
        total_playlist_count = create_playlist_count + collect_playlist_count
        #print total_playlist_count
        page = int(math.ceil(total_playlist_count / 36.0))
        total_playlist = []
        for i in range(page):
            #print page
            #url = webapi(5)
            data = '{"uid":"%s","wordwrap":"7","offset":"%s","total":"%s","limit":"36","csrf_token":""}' % (self.userId,i*36,'true' if i == 0 else 'false')
            form_data = get_data(data)
            header = {"User-Agent":self.get_useragent(),"Referer":"https://music.163.com/user/home?id=%s"%self.userId,"Host":"music.163.com","Connection":'close'}
            while True:
                #print '1'
                ip, port = self.get_proxy(1)
                proxy = {
                    'http': 'http://%s:%s' % (ip, port),
                    'https': 'http://%s:%s' % (ip, port)
                }
                try:
                    #print 2
                    result = self.get_json(form_data, webapi(5), header, proxy)
                    if result.status_code == requests.codes.ok:
                        result = result.content
                        result = json.loads(result)
                        break
                except Exception as e:
                    #print e,
                    self.delete_ip(ip)


            #print json.dumps(result, encoding='UTF-8', ensure_ascii=False)
            #num = (37 if i == 0 else 36) if i < (page - 1) else (total_playlist_count - i * (37 if i == 1 else 36))
            #print num
            #num = len(result['playlist'])
            for j in result['playlist']:
                #print j
                title = j['name']
                id = j['id']
                total_playlist.append({"name":title,"id":id})

        self.createdplaylistDict = total_playlist[0:self.createdplaylistCount]
        self.collectplaylistDict = total_playlist[(-1 * self.collectplaylistCount-1):-1]

        if (create_playlist_count != 0 and not self.createdplaylistDict) or (collect_playlist_count != 0 and not self.collectplaylistDict):
            return False
        return True

    def get_favor_song(self):
        url = "http://music.163.com/api/playlist/detail?id=%s" % self.createdplaylistDict[0]["id"]
        headers = {
            'Host': 'music.163.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'Referer': 'https://music.163.com/user/fans?id=86215323',
            "Connection":'close'
        }
        #print '1'
        headers['User-Agent'] = self.get_useragent()
        while True:
            ip,port = self.get_proxy(0)
            proxy = {
                'http': '%s:%s' % (ip, port),
                'https': '%s:%s' % (ip, port)
            }
            #print '1'
            try:
                s = requests.get(url,headers = headers,proxies = proxy, timeout=5)
                if s.status_code == requests.codes.ok:
                    s = s.content
                    s = json.loads(s)
                    break
            except Exception as e:
                #print e,
                self.delete_ip(ip)
        s = s['result']
        songCount = s['trackCount']
        createTime = self.timefomat(s['createTime'])
        updateTime = self.timefomat(s['updateTime'])
        playCount = s['playCount']
        name = s['name']
        songlist = []
        for i in s['tracks']:
            songname = i['name']
            #print songname.encode('utf-8')
            songartist = i['artists'][0]['name']
            songlist.append("%s-%s"%(songname,songartist))

        self.favorsonglist={'songCount':songCount,'createTime':createTime,'updateTime':updateTime,'playCount':playCount,'name':name,'songlist':songlist}
        if songCount != 0 and not songlist:
            return False
        return True

    def compelete_info(self):
        self.info = {
            "userId": self.userId, #用户id
            "nickname": self.nickname, #用户昵称
            "lv": self.lv, #用户等级
            "dynamic": self.dynamic, #用户动态
            "gender": self.gender, #用户性别
            "follows": self.follows,#关注人数
            "followeds": self.followeds,#粉丝人数
            "signature": self.signature,#个性签名
            "createdplaylistCount": self.createdplaylistCount,#创建歌单数
            "collectplaylistCount":self.collectplaylistCount,#收集歌单数
            "location": self.location,#用户所在地
            "birthday": self.birthday,#用户生日
            "totallistened": self.totallistened,#听歌总数
            "favorsonglist": self.favorsonglist,
            "createdplaylistDict":self.createdplaylistDict,#创建歌单信息
            "collectplaylistDict":self.collectplaylistDict,#收藏歌单信息
            "followsList":self.followsList,#关注列表
            "followedsList":self.followedsList#粉丝列表
        }