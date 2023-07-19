const crypto = require('crypto-js')

function md5(text){
    text = String(text)
    return crypto.MD5(text).toString()
}

var e = '/footballapi/core/matchlist/v2/immediate'
var t = {
    "appType": "3",
    "channelNumber": "GF1001",
    "comId": "8",
    "lang": "zh",
    "platform": "pc",
    "st": 1678167676726,
    "timeZone": "8",
    "version": "671",
    "versionCode": "671"
}

function l() {
            return e
        }
function Z(e, t) {
    var n = {}
      , o = e;
    for (var r in Object.keys(t).sort().map((function(e) {
        n[e] = t[e]
    }
    )),
    n)
        o = o + r + n[r];
    return o += md5("wjj"),
    md5(o).toLowerCase() + "99"
}

console.log(Z(e, t));