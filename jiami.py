# coding:utf-8
import os
import base64
import codecs
from Crypto.Cipher import AES



class WangYiYun():

    def __init__(self):
        self.first_param = ''
        self.second_param = '010001'
        self.third_param = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        self.fourth_param = '0CoJUm6Qyw8W8jud'

    def create_random_16(self):
        '''获取随机十六个字母拼接成的字符串'''
        return (''.join(map(lambda xx: (hex(ord(xx))[2:]), str(os.urandom(16)))))[0:16]

    def aesEncrypt(self, text, key):
        # 偏移量
        iv = '0102030405060708'
        # 文本
        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)
        encryptor = AES.new(key, 2, iv)
        ciphertext = encryptor.encrypt(text)
        ciphertext = base64.b64encode(ciphertext)
        return ciphertext

    def get_params(self, text):
        # print self.first_param
        params = self.aesEncrypt(self.first_param, self.fourth_param).decode('utf-8')
        params = self.aesEncrypt(params, text)
        return params

    def rsaEncrypt(self, pubKey, text, modulus):
        '''进行rsa加密'''
        text = text[::-1]
        rs = int(codecs.encode(text.encode('utf-8'), 'hex_codec'), 16) ** int(pubKey, 16) % int(modulus, 16)
        return format(rs, 'x').zfill(256)

    def get_encSEcKey(self, text):
        '''获取第二个参数'''
        pubKey = self.second_param
        moudulus = self.third_param
        encSecKey = self.rsaEncrypt(pubKey, text, moudulus)
        return encSecKey


def get_data(s):
    music = WangYiYun()
    music.first_param = "%s" % s
    text = music.create_random_16()
    params = music.get_params(text)
    encSecKey = music.get_encSEcKey(text)
    formdata = {'params': params,'encSecKey': encSecKey}
    return formdata


