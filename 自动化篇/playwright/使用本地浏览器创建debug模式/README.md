## 说明

此方法是playwright与本地浏览器以ws方式通信

可以绕过基本上大部分浏览器检测，因为这就是一个真正的浏览器

两种使用方式:

1. 每次运行程序之后先打开浏览器

> 1. 找到自己桌面chrome的快捷方式键
> 2. 点击属性
> 3. 在目标一栏的最后添加 --remote-debugging-port=9999 端口可自定义
> 4. ```
>    with sync_playwright() as p:
>    # 创建一个连接
>    browser = p.chromium.connect_over_cdp("http://localhost:9999")
>    content = browser.contexts[0]
>    page = content.new_page()
>    ```
> 5. 在上述page下进行浏览器操作即可

2. 不打开浏览器，自行打开
> 在程序中添加下面的代码即可
>```
>import subprocess
># 这个路径可以是Google浏览器的exe路径，也可以是快捷方式的路径
>chrome_path = r'"C:\Program Files\Google\Chrome\Application\chrome.exe"'
>debugging_port = "--remote-debugging-port=9999"
>
>command = f"{chrome_path} {debugging_port}"
>subprocess.Popen(command, shell=True)
>```
>之后就是
> ```
>    with sync_playwright() as p:
>    # 创建一个连接
>    browser = p.chromium.connect_over_cdp("http://localhost:9999")
>    content = browser.contexts[0]
>    page = content.new_page()
>    ```
> 在上述page下进行浏览器操作即可
> 
> __注意__:
> 此方法不可以在打开了普通版(非第一种情况)的浏览器使用