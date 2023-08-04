const Crypto = require('crypto-js')

var d = "B3978D054A72A7002063637CCDF6B2E5"

function sign(t) {
    for (var e in t)
        "" !== t[e] && void 0 !== t[e] || delete t[e];
    var n = d + l(t);
    return s(n)
}
function s(e) {
    return  md5(e)
}

function l(t) {
    for (var e = Object.keys(t).sort(u), n = "", a = 0; a < e.length; a++)
        if (void 0 !== t[e[a]])
            if (t[e[a]] && t[e[a]]instanceof Object || t[e[a]]instanceof Array) {
                var i = JSON.stringify(t[e[a]]);
                n += e[a] + i
            } else
                n += e[a] + t[e[a]];
    return n
}

// 创建标准md5算法
function md5(text){
    return Crypto.MD5(text).toString()
}
function u(t, e) {
    return t.toString().toUpperCase() > e.toString().toUpperCase() ? 1 : t.toString().toUpperCase() == e.toString().toUpperCase() ? 0 : -1
}

// 测试数据
data = {
    'pageNo': 1,
    'pageSize': 20,
    'total': 0,
    'AREACODE': '',
    'M_PROJECT_TYPE': '',
    'KIND': 'GCJS',
    'GGTYPE': '1',
    'PROTYPE': '',
    'timeType': '6',
    'BeginTime': '2022-07-18 00:00:00',
    'EndTime': '2023-01-18 23:59:59',
    'createTime': [],
    'ts': ts(),
}

// 生成时间戳
function ts(){
    return (new Date).getTime()
}

console.log(ts())
console.log(sign(data))

