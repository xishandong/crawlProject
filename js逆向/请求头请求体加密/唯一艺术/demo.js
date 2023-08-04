const Crypto = require('crypto-js')

var data = 'truiLeKm7AKyuie+33QCYVOB58uNUU9k+FEIeXVsr/ztKrMa9ytcHn11hxFo6XLAe2ye5nNmVQAAZ3zKiCcZZoPPcUBuypN/3xXg6+l98m38zldv8b2wlIVuy24U1PxbPFKGrQEbJTTwnoujMCcaeZfiOdyyjSMX24EXL8o244bbHdJm6UWRWxMux1ICO9tBg10IQxFo+j8/Cc3jAdGAlg=='

window = {
    deciphering: function (t){
         {
            e = "4tBlCLWFZ3eD93CvDE2lpw==" || 32;
            var o = "ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678"
              , r = o.length;
            for (let t = 0; t < e; t++)
                o.charAt(Math.floor(Math.random() * r));
            return t
        }
    }
}

function encryptSelf(t, o) {
    var r = Crypto.enc.Base64.parse("4tBlCLWFZ3eD93CvDE2lpw==");
    let i = JSON.stringify({
        id: t.substr(0, t.length - 1),
        sum: o
    });
    var s = Crypto.enc.Utf8.parse(i);
    return Crypto.AES.encrypt(s, r, {
        mode: Crypto.mode.ECB,
        padding: Crypto.pad.Pkcs7
    }).toString()
}
function decrypt(t) {
    var e = Crypto.enc.Base64.parse("5opkytHOggKj5utjZOgszg==")
    var o = Crypto.AES.decrypt(t, e, {
        mode: Crypto.mode.ECB,
        padding: Crypto.pad.Pkcs7
    });
    return Crypto.enc.Utf8.stringify(o).toString()
}

function getSign(data){
    let dataresult = decrypt(data)
        , dataResultFun = dataresult.split(",")[0].substr(4)
        , dataResultId = dataresult.split(",")[1].split("=")[1]
        , sigresult = eval(dataResultFun);
    console.log(sigresult)
    return encryptSelf(dataResultId, sigresult)
    // return sigresult
}

function design(data){
    return encodeURIComponent(data)
}

