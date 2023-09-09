# RedBook爬虫文档

## 数据库设计
见MYSQLDB文件
## 爬虫逻辑
暂时分为两个部分，获取主页帖子以及获取评论帖子
使用时需要下载feapder
需要nodejs环境
```bash
npm install jsdom
npm install touch-cookie
```
## 项目架构
支持数据库存储
支持csv存储
如果使用mysql需要配置数据库
如果使用csv需要配置csv文件名，路径已经做好
并且需要按照js代码的指示完成加密参数生成

## 之后新增
1. 更多功能
2. 用户池
3. ...