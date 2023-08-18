const jsdom = require("jsdom");
const {JSDOM} = jsdom;
const {CookieJar} = require('tough-cookie');


delete __filename
delete __dirname
////////////////////////////////////////////////////////////////////////////////////////////////
// 代理
proxy_ = function (obj) {
    return new Proxy(obj, {
        set(target, property, value) {
            console.table([{"类型": 'set', '调用者': target, "调用属性": property, '设置值': value}])
            return Reflect.set(...arguments)
        },
        get(target, property, receiver) {
            console.table([{"类型": 'get', '调用者': target, "调用属性": property, '获取值': target[property]}])
            return target[property]
        }
    })
}
////////////////////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////////////////////
// 生成dom
// 页面cookie 'key=value'
const customCookies = [];
// 页面localStorage 'key': 'value'
const customLocalStorage = {
}
const cookieJar = new CookieJar();
// 指定cookie加入对应 url
customCookies.forEach(cookie => {
    cookieJar.setCookieSync(cookie, 'https://h5.ele.me/minisite/?spm=a2ogi.13162730.zebra-ele-login-module-9089118186&spm-pre=a2f6g.12507204.ebridge.login&latitude=28.864343&longitude=105.407142&__locPid=B0FFHNZLY4&__locAid=716978502815819&__locAt=5&__locFrom=h5&spm=a2ogi.13162730.zebra-ele-login-module-9089118186&spm=a2ogi.13162730.zebra-ele-login-module-9089118186');
});
// 声明UA
const resourceLoader = new jsdom.ResourceLoader({
    userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
});
// 生成DOM
const dom = new JSDOM('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Title</title></head<body></body><script src="etSign.js"></script></html>', {
    url: "https://h5.ele.me/minisite/?spm=a2ogi.13162730.zebra-ele-login-module-9089118186&spm-pre=a2f6g.12507204.ebridge.login&latitude=28.864343&longitude=105.407142&__locPid=B0FFHNZLY4&__locAid=716978502815819&__locAt=5&__locFrom=h5&spm=a2ogi.13162730.zebra-ele-login-module-9089118186&spm=a2ogi.13162730.zebra-ele-login-module-9089118186",
    cookieJar: cookieJar,
    pretendToBeVisual: true,
    referrer: "https://h5.ele.me/minisite/?spm=a2ogi.13162730.zebra-ele-login-module-9089118186&spm-pre=a2f6g.12507204.ebridge.login&latitude=28.864343&longitude=105.407142&__locPid=B0FFHNZLY4&__locAid=716978502815819&__locAt=5&__locFrom=h5&spm=a2ogi.13162730.zebra-ele-login-module-9089118186&spm=a2ogi.13162730.zebra-ele-login-module-9089118186",
    contentType: 'text/html',
    resources: resourceLoader
});
win = dom.window;
////////////////////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////////////////////
// 生成浏览器常见对象，window可以用jsdom的或者global, 注意delete方法以及module
window = global;
// window = win
self = global;
top = global;
// window = proxy_(window);
////////////////////////////////////////////////////////////////////////////////////////////////
document = win.document;
Object.defineProperty(document, 'hidden', {
    value: true,
})
// document = proxy_(document);

////////////////////////////////////////////////////////////////////////////////////////////////
navigator = win.navigator;
Object.defineProperty(navigator, 'appVersion', {
    value: '5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    configurable: true,
    writable: false,
});
Object.defineProperty(navigator, 'webdriver', {
    value: false,
    configurable: true,
    writable: false,
});
Object.defineProperty(navigator, 'languages', {
    value: ['zh-CN', 'zh'],
    configurable: true,
    writable: false,
});
Object.defineProperty(navigator, 'language', {
    value: 'zh-CN',
    configurable: true,
    writable: false,
});
Object.defineProperty(navigator, 'connection', {
    value: {
        downlink: 4.75,
        effectiveType: "4g",
        onchange: null,
        rtt: 200,
        saveData: false
    },
    configurable: true,
    writable: false,
});
Object.defineProperty(navigator, 'platform', {
    value: 'Win32',
    configurable: true,
    writable: false,
});
Navigator = function Navigator(){}
Navigator.prototype = navigator
getBattery = function (){
    return Promise
}
navigator.getBattery = getBattery
// navigator = proxy_(navigator);
////////////////////////////////////////////////////////////////////////////////////////
location = {
    port: '43332',
    protocol: 'http:',
    href: 'https://h5.ele.me/minisite/?spm=a2ogi.13162730.zebra-ele-login-module-9089118186&spm-pre=a2f6g.12507204.ebridge.login&latitude=28.864343&longitude=105.407142&__locPid=B0FFHNZLY4&__locAid=716978502815819&__locAt=5&__locFrom=h5&spm=a2ogi.13162730.zebra-ele-login-module-9089118186&spm=a2ogi.13162730.zebra-ele-login-module-9089118186',
    search: '?spm=a2ogi.13162730.zebra-ele-login-module-9089118186&spm-pre=a2f6g.12507204.ebridge.login&latitude=28.864343&longitude=105.407142&__locPid=B0FFHNZLY4&__locAid=716978502815819&__locAt=5&__locFrom=h5&spm=a2ogi.13162730.zebra-ele-login-module-9089118186&spm=a2ogi.13162730.zebra-ele-login-module-9089118186',
    pathname: '/minisite/',
    hostname: 'h5.ele.me',
    host:'h5.ele.me',
    origin:'https://h5.ele.me',
    reload: function reload(){debugger},
    replace: function replace(){debugger},
    assign: function assign() {debugger},


}
// location = proxy_(location);
////////////////////////////////////////////////////////////////////////////////////////
history = win.history;
// history = proxy_(history);
///////////////////////////////////////////////////////////////////////////////////////////////
screen = {
    width: 1536,
    availWidth: 1536
};
// screen = proxy_(screen);
////////////////////////////////////////////////////////////////////////////////
localStorage = win.localStorage;
localStorage = proxy_(localStorage);
//////////////////////////////////////////////////////////////////////////////////
Image = win.Image;
////////////////////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////////////////////
// 常用方法hook
// 和canvas有关, 可能需要抛出异常
canvas = {
    getContext: function (a) {
        if (a === 'webgl') {
            return webgl;
        }else if (a === '2d'){
            return CanvasRenderingContext2D
        }
        console.log(a)
        return {}
    },
    tagName: 'canvas',
    style: {},
    toDataURL: function (){
        return 'data:image/png;base64,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'
    }
}
// canvas = proxy_(canvas);

webgl = {
    canvas: canvas,
    drawingBufferColorSpace: "srgb",
    drawingBufferHeight: 150,
    drawingBufferWidth: 300,
    unpackColorSpace: "srgb",
    getExtension: function (arg) {
        return {
            'loseContext': function (){}
        }
    },
    getParameter: function (a, b, c) {

    }
}
// webgl = proxy_(webgl)
CanvasRenderingContext2D = {
    name: '2d',
    fillRect: function (a, b, c, d) {
        // console.log(a, b, c, d)
        return undefined
    },
    fillText: function (a, b, c, d) {
        // console.log(a, 'lll', b, c, d)
        return undefined
    }
}
// CanvasRenderingContext2D = proxy_(CanvasRenderingContext2D)

_a = {}
Object.defineProperty(_a, 'href', {
    value: 'https://h5.ele.me/minisite/?spm=a2ogi.13162730.zebra-ele-login-module-9089118186&spm-pre=a2f6g.12507204.ebridge.login&latitude=28.864343&longitude=105.407142&__locPid=B0FFHNZLY4&__locAid=716978502815819&__locAt=5&__locFrom=h5&spm=a2ogi.13162730.zebra-ele-login-module-9089118186&spm=a2ogi.13162730.zebra-ele-login-module-9089118186',
    writable: false,
});
// _a = proxy_(_a)
pimg_ = function (obj) {
    return new Proxy(obj, {
        set(target, property, value) {
            console.table([{"类型": 'set', '调用者': target, "调用属性": property, '设置值': value}])
            return Reflect.set(...arguments)
        },
        get(target, property, receiver) {
            if (property.constructor.name === 'Symbol') {
                throw new Error('Access to internal property Symbol(impl) is not allowed.');
            }
            return target[property]
        }
    })
}
HTMLImageElement = function HTMLImageElement() {
}
img = {
    __proto__: HTMLImageElement.prototype,
}
img = pimg_(img)
createElement = function createElement(arg) {
    if (arg === 'canvas') {
        return canvas
    } else if (arg === 'a'){
        return _a
    } else if (arg === 'img'){
        return img
    }
     console.log(arg)
    return {}
}
document.createElement = createElement;

// 和audio有关，可能会抛出异常
OfflineAudioContext = function OfflineAudioContext(a, b, c) {
    console.log("OfflineAudioContext: ", a, b, c);
    return {}
}
window.OfflineAudioContext = OfflineAudioContext;

// 两个toString方法
var Object_toString = Object.prototype.toString;
Object.prototype.toString = function () {
    let temp = Object_toString.call(this, arguments);
    if (temp === '[object global]' || temp === '[object Window]') {
        return '[object Window]'
    } else if (this.constructor.name === 'String') {
        return this.valueOf()
    } else if (this.constructor.name === 'Cookie') {
        return '[object Object]'
    } else {
        // 其他情况，输出
        // console.log(this)
        return temp
    }
}
var Function_toString = Function.prototype.toString;
Function.prototype.toString = function () {
    let temp = Function_toString.call(this, arguments);
    if (this.name === 'Window') {
        return 'function window() { [native code] }'
    } else {
        // console.log(this)
        return temp
    }
}
////////////////////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////////////////////

require('./etSign.js')


var v = '//waimai-guide.ele.me/h5/mtop.alsc.eleme.miniapp.collection.homepagev1/1.0/5.0/?jsv=2.7.2&appKey=12574478&t=1692150357236&sign=dc27b0523bacbfe08b74bf004b15c372&api=mtop.alsc.eleme.miniapp.collection.homepagev1&v=1.0&dataType=json&mainDomain=ele.me&subDomain=waimai-guide&pageDomain=ele.me&H5Request=true&ttid=h5%40Web_iphone_10.28.0&type=originaljson&SV=5.0&data=%7B%22eventAction%22%3A%22nextPage%22%2C%22sceneCode%22%3A%22MINIAPP_ELEME_HOME_LIST%22%2C%22componentCode%22%3A%22frontend_page_shop_list_recommend%22%2C%22longitude%22%3A105.407142%2C%22latitude%22%3A28.864343%2C%22needReverseGeoAddress%22%3A0%2C%22pageParams%22%3A%22%7B%5C%22offset%5C%22%3A5%2C%5C%22rankId%5C%22%3A%5C%22b05ef7568da94af1bc7885721535a53c%5C%22%2C%5C%22behavior%5C%22%3A%5C%22expose_list%2524%2524___click_list%2524%2524%5C%22%2C%5C%22queryParams%5C%22%3A%5C%22%7B%5C%5C%5C%22id%5C%5C%5C%22%3A%5C%5C%5C%22%5C%5C%5C%22%2C%5C%5C%5C%22description%5C%5C%5C%22%3A%5C%5C%5C%22%5C%5C%5C%22%2C%5C%5C%5C%22title%5C%5C%5C%22%3A%5C%5C%5C%22%E9%99%84%E8%BF%91%E6%8E%A8%E8%8D%90%5C%5C%5C%22%2C%5C%5C%5C%22tabName%5C%5C%5C%22%3A%5C%5C%5C%22%25E9%2599%2584%25E8%25BF%2591%25E6%258E%25A8%25E8%258D%2590%5C%5C%5C%22%2C%5C%5C%5C%22pageCode%5C%5C%5C%22%3A%5C%5C%5C%22MINIAPP_ELEME_HOME_LIST%5C%5C%5C%22%2C%5C%5C%5C%22pageType%5C%5C%5C%22%3A%5C%5C%5C%22%5C%5C%5C%22%2C%5C%5C%5C%22clickAfterColor%5C%5C%5C%22%3A%5C%5C%5C%22%2300a6ff%5C%5C%5C%22%2C%5C%5C%5C%22clickBeforeColor%5C%5C%5C%22%3A%5C%5C%5C%22%23333%5C%5C%5C%22%2C%5C%5C%5C%22fontWeight%5C%5C%5C%22%3A%5C%5C%5C%22bold%5C%5C%5C%22%2C%5C%5C%5C%22listType%5C%5C%5C%22%3A%5C%5C%5C%22%5C%5C%5C%22%2C%5C%5C%5C%22position%5C%5C%5C%22%3A1%2C%5C%5C%5C%22scrollTop%5C%5C%5C%22%3A0%2C%5C%5C%5C%22tabCode%5C%5C%5C%22%3A%5C%5C%5C%22recommend_tab%5C%5C%5C%22%7D%5C%22%2C%5C%22limit%5C%22%3A20%2C%5C%22scene%5C%22%3A%5C%22miniapp%3Ahomepage%5C%22%7D%22%2C%22logicPageId%22%3A%22transformerpage_987%22%7D'



console.log(window.etSign(v))

