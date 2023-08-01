const crypto = require('crypto');

const ja = [
    "ce-UA2",
    "2|5|4|",
    "getTim",
    "MQLAB",
    "edBloc",
    "UtJZN",
    "439065zRBdtO",
    "wgSle",
    "0|4|2|",
    "nViaI",
    "ioIgW",
    "clone",
    "hasOwn",
    "0|8|7|",
    "iasqk",
    "Etifr",
    "OSCTt",
    "FJsqH",
    "wVUlq",
    "ZXfms",
    "Bytes",
    "UGSeu",
    "algo",
    "NrXMe",
    "3|9|1|",
    "eHmacH",
    "GRlmF",
    "ZRCYO",
    "QnCko",
    "Yqdfq",
    "ApHQT",
    "With",
    "5|3|4",
    "lib",
    "ime",
    "get",
    "HXHVF",
    "-nonce",
    "309436mPYOpN",
    "Veixu",
    "lOJxC",
    "words",
    "RGyAD",
    "XptBF",
    "alocP",
    "update",
    "5|7",
    "CbOFV",
    "apply",
    "zKJyX",
    "concat",
    "yozQn",
    "ySMfO",
    "YiFnO",
    "FpeCd",
    "local_",
    "RWzLf",
    "_doPro",
    "JzYOH",
    "DJPqr",
    "aUwDl",
    "push",
    "WXvhS",
    "extend",
    "1nQSLld",
    "gcdRw",
    "kdnpW",
    "toStri",
    "JawPa",
    "mcBvZ",
    "aya-Ap",
    "slice",
    "tdEtv",
    "WHhAv",
    "_nData",
    "TkhRk",
    "_hash",
    "niLyl",
    "reset",
    "xrXrZ",
    "jOzJg",
    "SHA1",
    "ceil",
    "3|5|1|",
    "KFfga",
    "charCo",
    "max",
    "WordAr",
    "14|5|2",
    "rqMJn",
    "arCode",
    "gPHGC",
    "ipkcx",
    "ZvsKB",
    "paOpX",
    "uKZCA",
    "vBzqm",
    "TaXid",
    "YjNqy",
    "|4|15|",
    "KhhiH",
    "cGDrQ",
    "WElfb",
    "splice",
    "mugbu",
    "HMAC",
    "BUaZl",
    "OMpMK",
    "vfwcU",
    "set",
    "GIQDU",
    "hrGZX",
    "aPvzH",
    "173264rRNOVA",
    "bqdRG",
    "poFMK",
    "BkBhf",
    "rxuhL",
    "oReuY",
    "0|7|6|",
    "VBGQB",
    "FOZEd",
    "TOKEN",
    "Daffv",
    "min",
    "jtYgw",
    "t32",
    "yiSjK",
    "_minBu",
    "deAt",
    "GET",
    "cFEup",
    "IuVtl",
    "zUvJK",
    "tamp",
    "GSgeq",
    "pMxgJ",
    "XUUpe",
    "RytqF",
    "IdZTr",
    "QCjSi",
    "ireTok",
    "fferSi",
    "HpUdw",
    "uNuWQ",
    "NNRvA",
    "Hex",
    "elper",
    "Latin1",
    "TRPuJ",
    "bkYWe",
    "ZIWEv",
    "Base",
    "nmlab",
    "5|1|3|",
    "KEnTI",
    "F-8 da",
    "IzRlL",
    "MGrLV",
    "WKdgl",
    "VlBpk",
    "2|0",
    "MXfRd",
    "nqoxP",
    "ZWXWH",
    "YoBbW",
    "_iKey",
    "vQOUL",
    "WuRZK",
    "noRequ",
    "ukOAY",
    "EGuBb",
    "ZcsGl",
    "parse",
    "length",
    "blCuA",
    "ock",
    "-versi",
    "blockS",
    "gujNA",
    "call",
    "11|13|",
    "_data",
    "sDyIb",
    "ZTGTw",
    "XZRtE",
    "WmjSd",
    "ify",
    "pZSOm",
    "zIPlk",
    "POST",
    "GASdH",
    "GNhfQ",
    "1|3|6|",
    "TLbYP",
    "join",
    "EaDJs",
    "BeSyw",
    "tCJik",
    "GEbVF",
    "glgUF",
    "/himal",
    "mAvLH",
    "enc",
    "pexhl",
    "_init_",
    "pop",
    "fjchU",
    "TkHPM",
    "CnNwH",
    "nRdNi",
    "3|4|1|",
    "oPGrP",
    "HHMJx",
    "0|2|1|",
    "WeubD",
    "wuCTw",
    "server",
    "jbHPU",
    "BMyWF",
    "vlrrq",
    "HcBQV",
    "toaZt",
    "uvwxyz",
    "unshif",
    "012345",
    "Hasher",
    "HmacSH",
    "sAKRh",
    "RIhZj",
    "ZeemS",
    "ijklmn",
    "brScK",
    "SILVt",
    "1|3",
    "starts",
    "_doFin",
    "wMMxe",
    "QighO",
    "nHfij",
    "6789ab",
    "EJaZR",
    "JwWjN",
    "yyADE",
    "jgWIC",
    "qvHLD",
    "iFkrO",
    "abMMk",
    "XkFFx",
    "mixIn",
    "pzfXT",
    "VQrYG",
    "MFlKO",
    "3|2|6|",
    "265345NWyqyK",
    "MVkvK",
    "tEvHy",
    "kAlgor",
    "qOgeZ",
    "ithm",
    "CnhwY",
    "BoFjt",
    "SIqXg",
    "RhFvF",
    "Proper",
    "WCaOQ",
    "Utf8",
    "YsYiP",
    "_hashe",
    "jwGap",
    "_proce",
    "method",
    "sigByt",
    "scCiw",
    "oNuzg",
    "_creat",
    "split",
    "hqYiv",
    "xnkFd",
    "MAQpD",
    "QcpYD",
    "token",
    "Qjjar",
    "MCwZV",
    "BlXLr",
    "random",
    "10|12|",
    "kxrhr",
    "aOZko",
    "iVpFa",
    "header",
    "tLGyD",
    "yrJuq",
    "getUin",
    "UclBY",
    "alize",
    "cfg",
    "EFWjw",
    "oXiQW",
    "fromCh",
    "bpRrX",
    "2|4",
    "ETYrb",
    "string",
    "_doRes",
    "med UT",
    "getIte",
    "data",
    "FnIqQ",
    "nuPjo",
    "gsIvW",
    "oqYqR",
    "xbVHJ",
    "FPPdz",
    "15611srHcIn",
    "oNJUg",
    "init",
    "cvBNy",
    "Malfor",
    "ioCYh",
    "wUqlk",
    "flkuC",
    "fBJQP",
    "ize",
    "OSjPh",
    "_appen",
    "buffer",
    "1|0|2|",
    "FdaXu",
    "avSsK",
    "opqrst",
    "pqfYl",
    "fntWA",
    "NHAOV",
    "cessBl",
    "$super",
    "DJYVH",
    "floor",
    "MPHld",
    "1.0",
    "ype",
    "eHelpe",
    "QgEkr",
    "uzcDm",
    "TGMNw",
    "ZinHP",
    "init_t",
    "ray",
    "11GlEDhd",
    "finali",
    "xSSEF",
    "6|0|4|",
    "time",
    "KBFAG",
    "Buffer",
    "366083gALaRb",
    "cEMnW",
    "clamp",
    "QYJBj",
    "XpmbG",
    "-times",
    "WfQMs",
    "ITBcv",
    "_oKey",
    "3|5|4",
    "url",
    "cdefgh",
    "413274xhboSa",
    "CsaQL",
    "CjxhJ",
    "zYMwC",
    "SwNky",
    "vUtfU",
    "CKtOo",
    "0|1|4|",
    "MsoCY",
    "XCKSQ",
    "giVGQ",
    "voGLk",
    "TeSgC",
    "zhcNl",
    "substr",
    "iNtpM",
    "YDfdN",
    "iServi",
    "protot",
    "VGbFC",
    "ABpeF",
    "wOhtk",
    "x-sign",
    "map",
    "gBNke"
]

function xa(t, e) {
    t -= 369;
    var n = ja[t];
    return n
}

function La() {
    for (var t = xa, e = {
        jbHPU: t(594) + t(609) + t(735) + t(600) + t(699) + t(592),
        WuRZK: function (t, e) {
            return t < e
        },
        iasqk: function (t, e) {
            return t * e
        },
        QCjSi: function (t, e) {
            return t | e
        },
        gujNA: function (t, e) {
            return t & e
        }
    }, n = [], r = e[t(587)], o = 0; e[t(537)](o, 36); o++)
        n[o] = r[t(750)](Math[t(706)](e[t(383)](Math[t(654)](), 16)), 1);
    n[14] = "4",
        n[19] = r[t(750)](e[t(509)](e[t(548)](n[19], 3), 8), 1),
        n[8] = n[13] = n[18] = n[23] = "_";
    var a = n[t(564)]("");
    return a
}

function Ra(t) {
    var e = xa
        , n = {
        IdZTr: e(393) + e(655) + e(457) + e(468) + e(382) + e(550) + "6",
        IuVtl: function (t, e) {
            return t < e
        },
        UGSeu: function (t, e) {
            return t < e
        },
        cEMnW: function (t, e) {
            return t < e
        },
        BeSyw: function (t, e) {
            return t + e
        },
        bqdRG: function (t, e, n) {
            return t(e, n)
        },
        wMMxe: function (t, e) {
            return t ^ e
        },
        pMxgJ: function (t, e) {
            return t - e
        },
        abMMk: function (t, e) {
            return t - e
        },
        RGyAD: function (t, e) {
            return t | e
        },
        QgEkr: function (t, e) {
            return t + e
        },
        RhFvF: function (t, e) {
            return t + e
        },
        wOhtk: function (t, e, n) {
            return t(e, n)
        },
        FnIqQ: function (t, e) {
            return t | e
        },
        MXfRd: function (t, e) {
            return t / e
        },
        pqfYl: function (t, e) {
            return t | e
        },
        RWzLf: function (t, e, n) {
            return t(e, n)
        },
        giVGQ: function (t, e) {
            return t | e
        },
        XCKSQ: function (t, e) {
            return t - e
        },
        ySMfO: function (t, e) {
            return t << e
        },
        QcpYD: function (t, e) {
            return t & e
        },
        iNtpM: function (t, e) {
            return t & e
        },
        WElfb: function (t, e) {
            return t & e
        },
        TaXid: function (t, e) {
            return t << e
        },
        RIhZj: function (t, e) {
            return t >>> e
        },
        flkuC: function (t, e) {
            return t - e
        },
        kdnpW: function (t, e) {
            return t >> e
        },
        ioCYh: function (t, e) {
            return t - e
        },
        paOpX: function (t, e) {
            return t * e
        },
        MAQpD: function (t, e) {
            return t(e)
        },
        IzRlL: function (t, e) {
            return t << e
        },
        VBGQB: function (t, e) {
            return t >>> e
        }
    }
        , r = n[e(508)][e(645)]("|")
        , o = 0;
    while (1) {
        switch (r[o++]) {
            case "0":
                for (g = 0; n[e(501)](g, t[e(543)]); g += 16) {
                    var a = h[e(440)](0);
                    for (c = 0; n[e(390)](c, 80); c++)
                        s[c] = n[e(725)](c, 16) ? t[n[e(566)](g, c)] : n[e(483)](l, n[e(606)](n[e(606)](n[e(606)](s[n[e(505)](c, 3)], s[n[e(616)](c, 8)]), s[n[e(616)](c, 14)]), s[n[e(616)](c, 16)]), 1),
                            i = n[e(411)](n[e(711)](n[e(711)](n[e(632)](n[e(632)](n[e(757)](l, h[0], 5), d[n[e(677)](n[e(531)](c, 20), 0)]()), h[4]), s[c]), f[n[e(700)](n[e(531)](c, 20), 0)]), 0),
                            h[1] = n[e(425)](l, h[1], 30),
                            h[e(575)](),
                            h[e(593) + "t"](i);
                    for (c = 0; n[e(725)](c, 5); c++)
                        h[c] = n[e(746)](n[e(632)](h[c], a[c]), 0)
                }
                continue;
            case "1":
                var c, i;
                continue;
            case "2":
                t[n[e(745)](m, 1)] = n[e(421)](p[e(543)], 3);
                continue;
            case "3":
                var u = {
                    uKZCA: function (t, r) {
                        var o = e;
                        return n[o(746)](t, r)
                    },
                    GASdH: function (t, r) {
                        var o = e;
                        return n[o(649)](t, r)
                    },
                    poFMK: function (t, r) {
                        var o = e;
                        return n[o(751)](t, r)
                    },
                    GRlmF: function (t, r) {
                        var o = e;
                        return n[o(606)](t, r)
                    },
                    TeSgC: function (t, r) {
                        var o = e;
                        return n[o(746)](t, r)
                    },
                    wuCTw: function (t, r) {
                        var o = e;
                        return n[o(471)](t, r)
                    },
                    WeubD: function (t, r) {
                        var o = e;
                        return n[o(471)](t, r)
                    },
                    NrXMe: function (t, r) {
                        var o = e;
                        return n[o(606)](t, r)
                    },
                    tdEtv: function (t, r) {
                        var o = e;
                        return n[o(606)](t, r)
                    },
                    nViaI: function (t, r) {
                        var o = e;
                        return n[o(466)](t, r)
                    },
                    ABpeF: function (t, r) {
                        var o = e;
                        return n[o(598)](t, r)
                    },
                    YiFnO: function (t, r) {
                        var o = e;
                        return n[o(690)](t, r)
                    },
                    yrJuq: function (t, r) {
                        var o = e;
                        return n[o(632)](t, r)
                    },
                    EFWjw: function (t, r) {
                        var o = e;
                        return n[o(725)](t, r)
                    }
                };
                continue;
            case "4":
                var s = []
                    , d = [function () {
                    var t = e;
                    return u[t(464)](u[t(560)](h[1], h[2]), u[t(484)](~h[1], h[3]))
                }
                    , function () {
                        var t = e;
                        return u[t(395)](u[t(395)](h[1], h[2]), h[3])
                    }
                    , function () {
                        var t = e;
                        return u[t(748)](u[t(748)](u[t(585)](h[1], h[2]), u[t(584)](h[1], h[3])), u[t(584)](h[2], h[3]))
                    }
                    , function () {
                        var t = e;
                        return u[t(392)](u[t(441)](h[1], h[2]), h[3])
                    }
                ]
                    , l = function (t, n) {
                    var r = e;
                    return u[r(748)](u[r(378)](t, n), u[r(756)](t, u[r(422)](32, n)))
                }
                    , f = [1518500249, 1859775393, -1894007588, -899497514]
                    , h = [1732584193, -271733879, null, null, -1009589776];
                continue;
            case "5":
                t[n[e(435)](p[e(543)], 2)] |= n[e(466)](128, n[e(688)](24, n[e(463)](n[e(471)](p[e(543)], 3), 8)));
                continue;
            case "6":
                return v;
            case "7":
                i = new DataView(new Uint32Array(h)[e(695)]);
                continue;
            case "8":
                continue;
            case "9":
                var p = new Uint8Array(n[e(648)](Ba, t));
                continue;
            case "10":
                var m = n[e(632)](n[e(526)](n[e(489)](n[e(632)](p[e(543)], 8), 6), 4), 16);
                t = new Uint8Array(n[e(526)](m, 2));
                continue;
            case "11":
                for (var g = 0; n[e(725)](g, 5); g++)
                    h[g] = i[e(662) + e(495)](n[e(526)](g, 2));
                continue;
            case "12":
                t[e(478)](new Uint8Array(p[e(695)])),
                    t = new Uint32Array(t[e(695)]);
                continue;
            case "13":
                var v = Array[e(754) + e(709)][e(759)][e(549)](new Uint8Array(new Uint32Array(h)[e(695)]), (function (t) {
                        var n = e;
                        return u[n(661)](u[n(666)](t, 16) ? "0" : "", t[n(436) + "ng"](16))
                    }
                ))[e(564)]("");
                continue;
            case "14":
                for (i = new DataView(t[e(695)]),
                         g = 0; n[e(725)](g, m); g++)
                    t[g] = i[e(662) + e(495)](n[e(526)](g, 2));
                continue;
            case "15":
                h[2] = ~h[0],
                    h[3] = ~h[1];
                continue
        }
        break
    }
}

function Ba(t) {
    var e, n, r, o = xa, a = {
        YjNqy: function (t, e) {
            return t < e
        },
        oNJUg: function (t, e) {
            return t < e
        },
        KBFAG: function (t, e) {
            return t < e
        },
        fntWA: function (t, e) {
            return t + e
        },
        CKtOo: function (t, e) {
            return t & e
        },
        xSSEF: function (t, e) {
            return t >> e
        },
        gcdRw: function (t, e) {
            return t & e
        },
        nRdNi: function (t, e) {
            return t == e
        },
        voGLk: function (t, e) {
            return t ^ e
        },
        HHMJx: function (t, e) {
            return t + e
        },
        gPHGC: function (t, e) {
            return t << e
        },
        MFlKO: function (t, e) {
            return t ^ e
        },
        MPHld: function (t, e) {
            return t + e
        },
        ukOAY: function (t, e) {
            return t >> e
        },
        MVkvK: function (t, e) {
            return t + e
        },
        blCuA: function (t, e) {
            return t & e
        },
        FdaXu: function (t, e) {
            return t >> e
        },
        qOgeZ: function (t, e) {
            return t >> e
        }
    }, c = [];
    for (e = 0; a[o(467)](e, t[o(543)]); e++)
        a[o(684)](n = t[o(454) + o(498)](e), 128) ? c[o(430)](n) : a[o(722)](n, 2048) ? c[o(430)](a[o(701)](192, a[o(742)](a[o(719)](n, 6), 31)), a[o(701)](128, a[o(434)](n, 63))) : (a[o(579)](a[o(719)](r = a[o(747)](n, 55296), 10), 0) ? (n = a[o(582)](a[o(582)](a[o(460)](r, 10), a[o(621)](t[o(454) + o(498)](++e), 56320)), 65536),
            c[o(430)](a[o(707)](240, a[o(434)](a[o(539)](n, 18), 7)), a[o(624)](128, a[o(544)](a[o(697)](n, 12), 63)))) : c[o(430)](a[o(624)](224, a[o(544)](a[o(627)](n, 12), 15))),
            c[o(430)](a[o(624)](128, a[o(544)](a[o(627)](n, 6), 63)), a[o(624)](128, a[o(544)](n, 63))));
    return c
}

function add(a, b) {
    return a + b;
}

function HmacSha1(key, data) {
    const hmac = crypto.createHmac('sha1', key);
    hmac.update(data);
    return hmac.digest('hex');
}

function sign(i, r, d, f) {
    return HmacSha1(f, add(add(i, r), d))
}


function setHeader(method, api, data, time) {
    const nonce = La()
    const init_sign = method + api + Ra(data)
    const hmac = sign(time, nonce, init_sign, time)
    return {
        'x-sign': hmac,
        'x-sign-nonce': nonce,
        'x-sign-timestamp': time,
        'x-sign-version': '1.0',
    }
}