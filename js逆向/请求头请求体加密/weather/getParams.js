const CryptoJS = require('crypto-js')


const askEgGnDlalR = "ajmEmqsokwfpfWv8";//AESkey，可自定义
const asi5jI3cvFQI = "bH7Ppp3nOF5k5PCt";//密钥偏移量IV，可自定义
const ackbiFPNKGDI = "dE1E6BPpAF5gwUEN";//AESkey，可自定义
const aci1c2jlP3KO = "fOf1MjRiLdsmtenp";//密钥偏移量IV，可自定义
const dsk80WzdMTMv = "h8ByxcqtKbzeqa3q";//DESkey，可自定义
const dsiCs366A1HA = "xJqk2s8ZDjgDHbBN";//密钥偏移量IV，可自定义
const dcku3b1jsXMn = "oHwOHptKV6TukKXJ";//DESkey，可自定义
const dciQs6k7qfCc = "prKerE8BHOzo9jvI";//密钥偏移量IV，可自定义


function md5(text) {
    text = String(text)
    return CryptoJS.MD5(text).toString()
}

var BASE64 = {
    encrypt: function (text) {
        return CryptoJS.enc.Base64.stringify(CryptoJS.enc.Utf8.parse(text));
    },
    decrypt: function (text) {
        return CryptoJS.enc.Base64.parse(text).toString(CryptoJS.enc.Utf8);
    }
};

var DES = {
    encrypt: function (text, key, iv) {
        var secretkey = (CryptoJS.MD5(key).toString()).substr(0, 16);
        var secretiv = (CryptoJS.MD5(iv).toString()).substr(24, 8);
        secretkey = CryptoJS.enc.Utf8.parse(secretkey);
        secretiv = CryptoJS.enc.Utf8.parse(secretiv);
        var result = CryptoJS.DES.encrypt(text, secretkey, {
            iv: secretiv,
            mode: CryptoJS.mode.CBC,
            padding: CryptoJS.pad.Pkcs7
        });
        return result.toString();
    },
    decrypt: function (text, key, iv) {
        var secretkey = (CryptoJS.MD5(key).toString()).substr(0, 16);
        var secretiv = (CryptoJS.MD5(iv).toString()).substr(24, 8);
        secretkey = CryptoJS.enc.Utf8.parse(secretkey);
        secretiv = CryptoJS.enc.Utf8.parse(secretiv);
        var result = CryptoJS.DES.decrypt(text, secretkey, {
            iv: secretiv,
            mode: CryptoJS.mode.CBC,
            padding: CryptoJS.pad.Pkcs7
        });
        return result.toString(CryptoJS.enc.Utf8);
    }
};

var AES = {
    encrypt: function (text, key, iv) {
        var secretkey = (CryptoJS.MD5(key).toString()).substr(16, 16);
        var secretiv = (CryptoJS.MD5(iv).toString()).substr(0, 16);
        secretkey = CryptoJS.enc.Utf8.parse(secretkey);
        secretiv = CryptoJS.enc.Utf8.parse(secretiv);
        var result = CryptoJS.AES.encrypt(text, secretkey, {
            iv: secretiv,
            mode: CryptoJS.mode.CBC,
            padding: CryptoJS.pad.Pkcs7
        });
        return result.toString();
    },
    decrypt: function (text, key, iv) {
        var secretkey = (CryptoJS.MD5(key).toString()).substr(16, 16);
        var secretiv = (CryptoJS.MD5(iv).toString()).substr(0, 16);
        secretkey = CryptoJS.enc.Utf8.parse(secretkey);
        secretiv = CryptoJS.enc.Utf8.parse(secretiv);
        var result = CryptoJS.AES.decrypt(text, secretkey, {
            iv: secretiv,
            mode: CryptoJS.mode.CBC,
            padding: CryptoJS.pad.Pkcs7
        });
        return result.toString(CryptoJS.enc.Utf8);
    }
};


function osmThj4lKY(obj) {
    var newObject = {};
    Object.keys(obj).sort().map(function (key) {
        newObject[key] = obj[key];
    });
    return newObject;
}

function getParams(city, salt, a7, a8) {
    var _city = {city: city}
    var mP227jOOD = "GETMONTHDATA"
    var a6Eh = salt;
    var cT4un = 'WEB';
    var tfTWU9k = new Date().getTime();

    var peqbJNB = {
        appId: a6Eh,
        method: mP227jOOD,
        timestamp: tfTWU9k,
        clienttype: cT4un,
        object: _city,
        secret: md5(a6Eh + mP227jOOD + tfTWU9k + cT4un + JSON.stringify(osmThj4lKY(_city)))
    };
    peqbJNB = BASE64.encrypt(JSON.stringify(peqbJNB));
    peqbJNB = DES.encrypt(peqbJNB, a7, a8);
    return peqbJNB;
}

function type1(city, salt) {
    var _city = {city: city}
    var mP227jOOD = "GETMONTHDATA"
    var a6Eh = salt;
    var cT4un = 'WEB';
    var tfTWU9k = new Date().getTime();

    var peqbJNB = {
        appId: a6Eh,
        method: mP227jOOD,
        timestamp: tfTWU9k,
        clienttype: cT4un,
        object: _city,
        secret: md5(a6Eh + mP227jOOD + tfTWU9k + cT4un + JSON.stringify(osmThj4lKY(_city)))
    };
    peqbJNB = BASE64.encrypt(JSON.stringify(peqbJNB));
    return peqbJNB;
}

function type2(city, salt, a7, a8) {
    var _city = {city: city}
    var mP227jOOD = "GETMONTHDATA"
    var a6Eh = salt;
    var cT4un = 'WEB';
    var tfTWU9k = new Date().getTime();

    var peqbJNB = {
        appId: a6Eh,
        method: mP227jOOD,
        timestamp: tfTWU9k,
        clienttype: cT4un,
        object: _city,
        secret: md5(a6Eh + mP227jOOD + tfTWU9k + cT4un + JSON.stringify(osmThj4lKY(_city)))
    };
    peqbJNB = BASE64.encrypt(JSON.stringify(peqbJNB));
    peqbJNB = DES.encrypt(peqbJNB, a7, a8);
    return peqbJNB;
}
function type3(city, salt, a1, a2) {
    var _city = {city: city}
    var mP227jOOD = "GETMONTHDATA"
    var a6Eh = salt;
    var cT4un = 'WEB';
    var tfTWU9k = new Date().getTime();

    var peqbJNB = {
        appId: a6Eh,
        method: mP227jOOD,
        timestamp: tfTWU9k,
        clienttype: cT4un,
        object: _city,
        secret: md5(a6Eh + mP227jOOD + tfTWU9k + cT4un + JSON.stringify(osmThj4lKY(_city)))
    };
    peqbJNB = BASE64.encrypt(JSON.stringify(peqbJNB));
    peqbJNB = AES.encrypt(peqbJNB, a1, a2);
    return peqbJNB;
}

function decrypt(data, a1, a2, a5, a6) {
    data = BASE64.decrypt(data);
    data = DES.decrypt(data, a5, a6);
    data = AES.decrypt(data, a1, a2);
    data = BASE64.decrypt(data);
    return JSON.parse(data)
}

function file(p, a, c, k, e, d) {
    e = function (c) {
        return (c < a ? '' : e(parseInt(c / a))) + ((c = c % a) > 35 ? String.fromCharCode(c + 29) : c.toString(36))
    }
    ;
    if (!''.replace(/^/, String)) {
        while (c--) {
            d[e(c)] = k[c] || e(c)
        }
        k = [function (e) {
            return d[e]
        }
        ];
        e = function () {
            return '\\w+'
        }
        ;
        c = 1
    }
    ;
    while (c--) {
        if (k[c]) {
            p = p.replace(new RegExp('\\b' + e(c) + '\\b', 'g'), k[c])
        }
    }
    return p
}


function get_enc(data) {
    return eval('file(' + data + ')')
}

