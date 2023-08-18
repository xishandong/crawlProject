const crypto = require('crypto')
const Py = "zxcvbnmlkjhgfdsaqwertyuiop0987654321QWERTYUIOPLKJHGFDSAZXCVBNM" , jq = Py + "-@#$%^&*+!";
function Nonce(e) {
    return [...Array(e)].map(()=>Py[Vq(0, 61)]).join("")
}
function Vq(e, t) {
    switch (arguments.length) {
    case 1:
        return parseInt(Math.random() * e + 1, 10);
    case 2:
        return parseInt(Math.random() * (t - e + 1) + e, 10);
    default:
        return 0
    }
}
function lr(e=[]) {
    return e.map(t=>jq[t]).join("")
}
function Rg(e={}) {
    const {p: t, t: n, n: u, k: o} = e
      , r = zq(t);
    console.log(r)
    const hash = crypto.createHash('sha256')
    return hash.update(u + o + decodeURIComponent(r) + n).digest('hex')
}
function zq(e) {
    let t = "";
    return typeof e == "object" ? t = Object.keys(e).map(n=>`${n}=${e[n]}`).sort().join("&") : typeof e == "string" && (t = e.split("&").sort().join("&")),
    t
}
function hash256(datas){
    let c = lr([8, 28, 20, 42, 21, 53, 65, 6])
    a = Date.now()
    let l = Nonce(16)
    let Signature = Rg({
        p: JSON.stringify(datas).replace(/:/g, "=").replace(/["{}]/g, '').replace(/,/g, '&'),
        t: a,
        n: l,
        k: c
    })
    text = {
        App: lr([11, 11, 0, 21, 62, 25, 24, 19, 20, 15, 7]),
        Nonce: l,
        Signature: Signature,
        Timestamp: a,
    }
    return text
}

data = {
    'type': "trading-type",
    "publishStartTime": "",
    "publishEndTime": "",
    "siteCode": "44",
    "secondType": "A",
    "projectType": "",
    "thirdType": "",
    "dateType": "",
    "total": 189352,
    "pageNo": 5,
    "pageSize": 10,
    "openConvert": false
}

console.log(hash256(data))