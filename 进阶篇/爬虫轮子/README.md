# 个人对requests库的二次封装

> 对于爬虫常见的发送请求以及日志记录和响应校验进行了二次封装。
> 
> 只需要在新的类继承CrawlBase即可，发送请求的函数使用do_request
> 
> 可以设置中间件以及发生前校验和发送后校验
> 

#### 未来设想

1. 增加用户池
2. 结构优化
3. 把请求响应都封装
4. 去重自动入库
5. 等等