import base64
import binascii
import hashlib
import json
import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5


def w(hex_string):
    byte_data = binascii.unhexlify(hex_string)  # 将十六进制字符串转换为字节数组
    base64_data = base64.b64encode(byte_data)  # 将字节数组转换为Base64编码
    return base64_data.decode('utf-8')


def md5(data):
    return hashlib.md5(data.encode('utf-8')).hexdigest()


def rsa(plaintext, key):
    publicKey = f'-----BEGIN PUBLIC KEY-----\n{key}\n-----END PUBLIC KEY-----'
    public_key = RSA.import_key(publicKey)
    cipher_rsa = PKCS1_v1_5.new(public_key)
    return cipher_rsa.encrypt(plaintext.encode('utf-8')).hex()


def getParams(data, key):
    a = json.dumps({
        **data,
        **{
            'sign': md5(json.dumps(data, separators=(',', ':'), ensure_ascii=False)),
            'timeStamp': int(time.time() * 1000)
        }
    }, ensure_ascii=False, separators=(',', ':'))
    n = [rsa(a[i:i + 50], key) for i in range(0, len(a), 50)]
    return w(''.join(n))

