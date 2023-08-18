const crypto = require('crypto');

function w(hexString) {
    const buffer = Buffer.from(hexString, 'hex');
    return buffer.toString('base64');
}

function md5(data) {
    return crypto.createHash('md5').update(data).digest('hex');
}

function rsa(data, key) {
    const publicKey = `-----BEGIN PUBLIC KEY-----\n${key}\n-----END PUBLIC KEY-----`;
    const buffer = Buffer.from(data, 'utf-8');
    const publicKeyBuffer = Buffer.from(publicKey, 'utf-8');
    const encryptedData = crypto.publicEncrypt({
        key: publicKeyBuffer,
        padding: crypto.constants.RSA_PKCS1_PADDING
    }, buffer);
    return encryptedData.toString('hex')
}


function getParams(data, key) {
    let a = JSON.stringify({
        ...data,
        ...{
            sign: md5(JSON.stringify(data)),
            timeStamp: +new Date
        }
    })
    var r = '';
    n = a.match(/.{1,50}/g);
    n.forEach((function (A) {
        var t = rsa(A, key);
        r += t
    }))
    return w(r)
}

