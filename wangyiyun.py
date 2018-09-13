#coding:utf-8

from Netease_Spider import spider
from success_id import SUCCESS_ID
import data_write
from idpool import ID_pool



def main():

    origin_ID = input('请输入起始用户ID:')
    ID_pool.put(origin_ID)
    num = 1
    while not ID_pool.empty():
        print '正在爬取第%s个用户' % num,
        try:
            num += 1
            id = ID_pool.get()
            if id in SUCCESS_ID:
                print '该用户已爬取，跳过'
                continue
            user = spider(id)
            print id,
            check_ID = True
            while True:
                s= user.get_basic_info()
                if s == -1:
                    print '该账户已注销'
                    check_ID = False
                    break
                if s:
                    break

            if not check_ID:
                continue

            print '基本信息采集完成',

            if int(user.follows)+int(user.followeds) > 600:
                print '粉丝和关注太多，跳过'
                continue
            #print user.info
            while True:
                m = user.get_follow()
                if m:
                    break
            print '用户关系采集完成',
            while True:
                o = user.get_playlist()
                if o:
                    break
            print '用户歌单采集完成',
            while True:
                p = user.get_favor_song()
                if p:
                    break
            print '我喜欢采集完成',
        except Exception as e:
            print e, '爬取失败!'
            continue
        user.compelete_info()
        data_write.write(user.info)
        print '写入数据库成功',
        SUCCESS_ID.add(id)
        print '爬取成功!'

main()