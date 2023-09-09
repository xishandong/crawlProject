const {JSDOM} = require('jsdom');
const {CookieJar} = require('tough-cookie');

delete __filename
delete __dirname


const customCookies = [
    // 注意此处是列表，之前那里是数组，这里每一个值是a=b的形式
];
const customLocalStorage = {

}
const cookieJar = new CookieJar();
customCookies.forEach(cookie => {
    cookieJar.setCookieSync(cookie, 'https://www.xiaohongshu.com/explore');
});
_xl = function () {
    debugger
}
const dom = new JSDOM('<!DOCTYPE html><html lang="zh"><body></body></html>', {
    url: 'https://www.xiaohongshu.com/explore',
    cookieJar: cookieJar,
    pretendToBeVisual: true,
    referrer: 'https://www.xiaohongshu.com',
    contentType: 'text/html',
});


proxy_ = function (obj) {
    return new Proxy(obj, {
        set(target, property, value) {
            console.table([{"类型": 'set', '调用者': target, "调用属性": property, '设置值': value}])
            return Reflect.set(...arguments)
        },
        get(target, property, receiver) {
            if (property.constructor.name === 'Symbol') {
                throw new Error('Access to internal property Symbol(impl) is not allowed.');
            }
            console.table([{"类型": 'get', '调用者': target, "调用属性": property, '获取值': target[property]}])
            return target[property]
        }
    })
}

window = dom.window;
document = window.document;
navigator = window.navigator;
location = window.location;
screen = {
    availHeight: 824,
    availLeft: 0,
    availTop: 0,
    availWidth: 1536,
    colorDepth: 24,
    height: 864,
    isExtended: false,
    onchange: null,
    orientation: {
        angle: 0,
        onchange: null,
        type: 'landscape-primary'
    },
    pixelDepth: 24,
    width: 1536
};


window.devicePixelRatio = 1.25
window.AudioContext = _xl
window.openDatabase = _xl
window.CanvasRenderingContext2D = _xl
window.HTMLCanvasElement = _xl
Object.keys(customLocalStorage).forEach(key => {
    dom.window.localStorage.setItem(key, customLocalStorage[key]);
});


Object.defineProperty(navigator, 'platform', {
    value: 'Win32',
    configurable: true,
    writable: false,
});
Object.defineProperty(navigator, 'userAgent', {
    value: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    configurable: true,
    writable: false,
});
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


canvas = {
    getContext: function (arg) {
        if (arg === 'webgl') {
            return webgl
        }
        return null
    },
}

webgl = {
    canvas: canvas,
    drawingBufferColorSpace: "srgb",
    drawingBufferHeight: 150,
    drawingBufferWidth: 300,
    unpackColorSpace: "srgb",
    getExtension: function (arg) {
        return {}
    },
    getParameter: function (arg) {
        if (arg === undefined) {
            throw new Error("Uncaught TypeError: Failed to execute 'getParameter' on 'WebGLRenderingContext': 1 argument required, but only 0 present.")
        }
    }
}

HTMLImageElement = function HTMLImageElement() {
}

img = {
    tagName: 'IMG',
    __proto__: HTMLImageElement.prototype,
}

var img = proxy_(img)

var createElement = function createElement(arg) {
    if (arg === 'div') {
        return {
    tagName: 'DIV',
    appendChild: function (arg) {
        if (arg.tagName === 'DIV') {
            throw new Error("Uncaught")
        }
    },
    style: {},
    offsetHeight: 0
}
    } else if (arg === 'img') {
        return img
    } else if (arg === 'canvas') {
        return canvas
    } else if (arg === 'a') {
        return {
            tagName: 'A'
        }
    } else if (arg === 'p') {
        return {
            tagName: 'P'
        }
    } else if (arg === 'h1') {
        return {
            tagName: 'H1'
        }
    } else if (arg === 'h2') {
        return {
            tagName: 'H2'
        }
    } else if (arg === 'h3') {
        return {
            tagName: 'H3'
        }
    } else if (arg === 'h4') {
        return {
            tagName: 'H4'
        }
    } else if (arg === 'span') {
        return {
            tagName: 'SPAN',
        }
    } else if (arg === 'ul') {
        return {
            tagName: 'UL',
        }
    } else if (arg === 'li') {
        return {
            tagName: 'LI',
        }
    } else {
        throw new Error('Uncaught DOMException: Failed to execute \'createElement\' on \'Document\': The tag name provided (\'[object HTMLDocument]\') is not a valid name.');
    }
}
document.createElement = createElement


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
        return temp
    }
}

var Function_toString = Function.prototype.toString;
Function.prototype.toString = function () {
    let temp = Function_toString.call(this, arguments);
    if (this.name === 'Window') {
        return 'function window() { [native code] }'
    } else {
        return temp
    }
}

;
// 此处自行下载关键加密代码


var a = XsXt('/api/sns/web/v1/feed', {source_note_id: '64bf47e3000000001201a95c'})
console.log(a)

function XsXt(e, t) {
    return window._webmsxyw(e, t)
}