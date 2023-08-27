const Module = require('./ddd.js')

var k = [121, 96, 7, 103, 57, 95, 61, 124, 121, 96, 7, 103, 57, 95, 61, 124]
function getCookie(arg1) {
    var _0x5e8b26 = '3000176000856006061501533003690027800375'
    String['prototype']['hexXor'] = function (_0x4e08d8) {
        var _0x5a5d3b = '';
        for (var _0xe89588 = 0x0; _0xe89588 < this['length'] && _0xe89588 < _0x4e08d8['length']; _0xe89588 += 0x2) {
            var _0x401af1 = parseInt(this['slice'](_0xe89588, _0xe89588 + 0x2), 0x10);
            var _0x105f59 = parseInt(_0x4e08d8['slice'](_0xe89588, _0xe89588 + 0x2), 0x10);
            var _0x189e2c = (_0x401af1 ^ _0x105f59)['toString'](0x10);
            if (_0x189e2c['length'] === 0x1) {
                _0x189e2c = '\x30' + _0x189e2c;
            }
            _0x5a5d3b += _0x189e2c;
        }
        return _0x5a5d3b;
    }

    String['prototype']['unsbox'] = function () {
        var _0x4b082b = [0xf, 0x23, 0x1d, 0x18, 0x21, 0x10, 0x1, 0x26, 0xa, 0x9, 0x13, 0x1f, 0x28, 0x1b, 0x16, 0x17, 0x19, 0xd, 0x6, 0xb, 0x27, 0x12, 0x14, 0x8, 0xe, 0x15, 0x20, 0x1a, 0x2, 0x1e, 0x7, 0x4, 0x11, 0x5, 0x3, 0x1c, 0x22, 0x25, 0xc, 0x24];
        var _0x4da0dc = [];
        var _0x12605e = '';
        for (var _0x20a7bf = 0x0; _0x20a7bf < this['\x6c\x65\x6e\x67\x74\x68']; _0x20a7bf++) {
            var _0x385ee3 = this[_0x20a7bf];
            for (var _0x217721 = 0x0; _0x217721 < _0x4b082b['length']; _0x217721++) {
                if (_0x4b082b[_0x217721] === _0x20a7bf + 0x1) {
                    _0x4da0dc[_0x217721] = _0x385ee3;
                }
            }
        }
        _0x12605e = _0x4da0dc['\x6a\x6f\x69\x6e']('');
        return _0x12605e;
    };
    var _0x23a392 = arg1['unsbox']();
    arg2 = _0x23a392['hexXor'](_0x5e8b26);
    return arg2
}
function decrypto(data) {
    var sss = wbsk_AES_cbc_decrypt_base64(data, k)
    a = JSON.parse(sss)
    return sss
}
function encrypt(data) {
    return wbsk_AES_cbc_encrypt_base64(data, k)
}
function wbsk_AES_cbc_decrypt_base64(input, iv) {
    var tmp_input = base64ToArrayBuffer(input)
    var result = wbsk_AES_cbc_decrypt(tmp_input, tmp_input.length, iv, iv.length);
    return byteToString(result);
}

function wbsk_AES_cbc_decrypt(input, inlen, iv, ivlen) {
    var tt = [];

    var len = inlen;
    var outadd = Module._malloc(len);
    var output = Module.HEAP8.subarray(outadd, outadd + len);

    var lenadd = Module._malloc(4);
    var lenput = Module.HEAP32.subarray(lenadd / 4, lenadd / 4 + 1);
    lenput[0] = len;


    var CBCDecrypt = Module.cwrap('wbsk_AES_cbc_decrypt', 'number', ['array', 'number', 'number', 'number', 'array', 'number'])
    var r = CBCDecrypt(new Uint8Array(input), inlen, outadd, lenadd, new Uint8Array(iv), ivlen);
    var olen = lenput[0];

    for (var key in output) {
        tt.push(output[key]);
    }

    Module._free(outadd);
    Module._free(lenadd);

    return (tt.slice(0, olen));

}

function wbsk_AES_cbc_encrypt_base64(input, iv) {
    var tmp_input = stringToByte(input);
    var result = wbsk_AES_cbc_encrypt(tmp_input, tmp_input.length, iv, iv.length);
    return arrayBufferToBase64(result);
}

function wbsk_AES_cbc_encrypt(input, inlen, iv, ivlen) {
    var tt = [];

    var len = (Math.floor(inlen / 16) + 1) * 16;
    var outadd = Module._malloc(len);
    var output = Module.HEAP8.subarray(outadd, outadd + len);

    var lenadd = Module._malloc(4);
    var lenput = Module.HEAP32.subarray(lenadd / 4, lenadd / 4 + 1);
    lenput[0] = len;


    var CBCEncrypt = Module.cwrap('wbsk_AES_cbc_encrypt', 'number', ['array', 'number', 'number', 'number', 'array', 'number'])
    var r = CBCEncrypt(new Uint8Array(input), inlen, outadd, lenadd, new Uint8Array(iv), ivlen);
    var olen = lenput[0];

    for (var key in output) {
        tt.push(output[key]);
    }

    Module._free(outadd);
    Module._free(lenadd);

    return (tt.slice(0, olen));

}

function stringToByte(str) {
    var bytes = new Array();
    var len, c;
    len = str.length;
    for (var i = 0; i < len; i++) {
        c = str.charCodeAt(i);
        if (c >= 0x010000 && c <= 0x10FFFF) {
            bytes.push(((c >> 18) & 0x07) | 0xF0);
            bytes.push(((c >> 12) & 0x3F) | 0x80);
            bytes.push(((c >> 6) & 0x3F) | 0x80);
            bytes.push((c & 0x3F) | 0x80);
        } else if (c >= 0x000800 && c <= 0x00FFFF) {
            bytes.push(((c >> 12) & 0x0F) | 0xE0);
            bytes.push(((c >> 6) & 0x3F) | 0x80);
            bytes.push((c & 0x3F) | 0x80);
        } else if (c >= 0x000080 && c <= 0x0007FF) {
            bytes.push(((c >> 6) & 0x1F) | 0xC0);
            bytes.push((c & 0x3F) | 0x80);
        } else {
            bytes.push(c & 0xFF);
        }
    }
    return bytes;
}

function byteToString(arr) {
    if (typeof arr === 'string') {
        return arr;
    }
    var str = '',
        _arr = arr;
    for (var i = 0; i < _arr.length; i++) {
        var one = (_arr[i] & 0xff).toString(2),
            v = one.match(/^1+?(?=0)/);
        if (v && one.length == 8) {
            var bytesLength = v[0].length;
            var store = (_arr[i] & 0xff).toString(2).slice(7 - bytesLength);
            for (var st = 1; st < bytesLength; st++) {
                store += (_arr[st + i] & 0xff).toString(2).slice(2);
            }
            str += String.fromCharCode(parseInt(store, 2));
            i += bytesLength - 1;
        } else {
            str += String.fromCharCode(_arr[i]);
        }
    }
    return str;
}

function arrayBufferToBase64(buffer) {
    var binary = '';
    var bytes = new Uint8Array(buffer);
    var len = bytes.byteLength;
    for (var i = 0; i < len; i++) {
        binary += String.fromCharCode(bytes[i]);
    }
    return btoa(binary);
}

function base64ToArrayBuffer(base64) {
    var binary_string = atob(base64);
    var len = binary_string.length;
    var bytes = new Uint8Array(len);
    for (var i = 0; i < len; i++) {
        bytes[i] = binary_string.charCodeAt(i);
    }
    return bytes;
}