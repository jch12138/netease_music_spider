#coding:utf-8

def webapi(no):  # api列表
    url = [
        "https://music.163.com/weapi/cloudsearch/get/web?csrf_token=",  # 搜索api
        "https://music.163.com/weapi/v1/play/record?csrf_token=",  # 听歌记录api
        "https://music.163.com/weapi/user/playlist?csrf_token=",  # 歌单api
        "http://music.163.com/weapi/user/getfolloweds?csrf_token=",  # 获取粉丝api
        "http://music.163.com/weapi/user/getfollows/%s?csrf_token=",  # 获取关注api
        "https://music.163.com/weapi/user/playlist?csrf_token=",  # 获取个人歌单api
        "http://music.163.com/api/playlist/detail?id=98323058",  # 获取歌单歌曲api(GET)
        "https://music.163.com/user/home"  # 个人详细信息(GET)
    ]

    return url[no]