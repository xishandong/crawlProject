import random
from binascii import hexlify
import base64
from Crypto.Cipher import AES

e = "010001"
g = "0CoJUm6Qyw8W8jud"
f = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
i3x = '{"csrf_token":"","cursor":"1672939386847","offset":"0","orderType":"1","pageNo":"3","pageSize":"20","rid":"R_SO_4_1835283134","threadId":"R_SO_4_1835283134"}'


# 生成随机的16位字符传
def RandomString(a):
    string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    randomStr = random.sample(string, a)
    return ''.join(randomStr)


# AES加密算法
def AESEncrypto(text, key):
    BS = 16
    pad = lambda s: s + (BS - len(s) % BS) * bytes([BS - len(s) % BS])
    c = key.encode("utf-8")
    d = "0102030405060708".encode("utf-8")
    e = text.encode("utf-8")
    aes = AES.new(c, AES.MODE_CBC, d)
    enc = base64.b64encode(aes.encrypt(pad(e))).decode("utf-8")
    return enc


# RSA加密
def RSAEncrypto(text):
    text = text[::-1]  # 表示文本倒序
    result = pow(int(hexlify(text.encode('utf-8')), 16), int(e, 16), int(f, 16))
    return format(result, 'x').zfill(131)


def d(text):
    i = RandomString(16)
    encText = AESEncrypto(text, g)
    encText = AESEncrypto(encText, i)
    encSecKey = RSAEncrypto(i)
    h = {
        "encText": encText,
        "encSecKey": encSecKey
    }
    return h



