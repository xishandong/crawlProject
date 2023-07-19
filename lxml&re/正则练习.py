import re
# 提取出python
key = "java python c++ php"
s = re.findall('python', key)[0]
print(s)
# key = 'https://scpic.chinaz.net/files/default/imgs/2023-01-04/610de886ffc6b37d_s.jpg'
# s = re.sub('_s', '', key)
# print(s)
# 提取出hello world
# key = "<html><h1>hello world<h1><html>"
# s = re.findall('<h1>(.*)<h1>', key)[0]
# print(s)
# 提取出170
# string = '我喜欢身高为170的女生'
# s = re.findall('\d+', string)[0]
# print(s)
# 提取出http:// 和 https://
# key = 'http://www.baidu.com and https://dong.com'
# s = re.findall('https?://', key)
# print(s)
# 提取出hello
# key = 'lalala<hTml>hello</HTMl>hahaha'
# s = re.findall('<[Hh][Tt][mM][lL]>(.*)</[Hh][Tt][mM][Ll]>', key)
# print(s)
# 提取出hit.
# key = 'bobo@hit.edu.cn'
# s = re.findall('h.*?\.', key)[0]
# print(s)
# 提取出saas 和 sas
# key = 'saas and sas and saaas'
# s = re.findall('sa{1,2}s', key)
# print(s)
