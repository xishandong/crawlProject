const Crypto = require('crypto-js')

var c = 'EB444973714E4A40876CE66BE45D5930'
var b = 'B5A8904209931867'
function decrypt(t) {
    var e = Crypto.enc.Utf8.parse(c)
      , n = Crypto.enc.Utf8.parse(b)
      , a = Crypto.AES.decrypt(t, e, {
        iv: n,
        mode: Crypto.mode.CBC,
        padding: Crypto.pad.Pkcs7
    });
    return a.toString(Crypto.enc.Utf8)
}
