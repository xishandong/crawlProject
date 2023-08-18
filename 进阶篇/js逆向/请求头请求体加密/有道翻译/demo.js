// const Crypto = require('crypto-js逆向')
//
//
// var data = 'Z21kD9ZK1ke6ugku2ccWuz4Ip5f4PLCoxWstZf_6UUyBoy8dpWc3NOXFRrnPMya7chcEL7e2Yz1xjFqcfdncOW4vOoJ66RTmRa8-dGZla_ExpWOUP0G1QJFtJ6Gj0ngir07R0ETWttaGO185v5rccLlZKqOCmJuChZSA-Dw9U6B2AOK4-RqYjAQEQ5vF7ph71eC5ZEvV6dm_xv0ywEOKi58R9xWx7fiJytxxlsz-oprAHdRXnI6kWszLLJJpr45DMBjoeArZfVssgWXzX_IlNUvTtj_1o95BpERVvV1FxGEeN-_TLgLaK9j7rjT4O-yPHpbuCk9q1BpLVSh3B4CPWCZPMIHwJiFtfQAC8_t-HWs45DWbW54DEny_doBItZ6v'
// var key = 'ydsecret://query/key/B*RGygVywfNBwpmBaZg*WT7SIOUP2T0C9WHMZN39j^DAdaZhAnxvGcCY6VYFwnHl'
// var iv = 'ydsecret://query/iv/C@lZe2YzHtZ2CYgaXKSVfsb7Y4QWHjITPPZ0nQp87fBeJ!Iv6v^6fvi2WN@bYpJ4'
//
// var ax = [8, 20, 157, 167, 60, 89, 206, 98, 85, 91, 1, 233, 47, 52, 232, 56]
// var b = [210, 187, 27, 253, 232, 59, 56, 195, 68, 54, 99, 87, 183, 156, 174, 28]

let data01 = '08149da73c59ce62555b01e92f34e838'//十六进制

 let newdata = Buffer.from(data01,'hex');//先把数据存在buf里面

 console.log("newdata ",newdata);

 console.log(newdata.toString("utf-8"));//使用toString函数就能转换成字符串
