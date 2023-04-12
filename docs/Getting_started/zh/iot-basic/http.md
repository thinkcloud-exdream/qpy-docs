# HTTP通信(待完善)

## 简介

HTTP（HyperText Transfer Protocol）即超文本传输协议，是一种详细规定了浏览器和万维网服务器之间互相通信的规则，它是万维网交换信息的基础，它允许将HTML（超文本标记语言）文档从Web服务器传送到Web浏览器。HTTP是一个基于TCP/IP通信协议来传递数据（HTML 文件, 图片文件, 查询结果等）。HTTP使用（Request）/应答（Response）模型，Web浏览器向Web服务器发送请求时，Web服务器处理请求并返回适当的应答。

## GET示例

get请求的http中最常见的请求方式，以下是示例代码

```py
import request
import checkNet


PROJECT_NAME = "request_get_exam"
PROJECT_VERSION = "1.0.0"

checknet = checkNet.CheckNetwork(PROJECT_NAME, PROJECT_VERSION)


url = "http://httpbin.org/get"

if __name__ == '__main__':
    stagecode, subcode = checknet.wait_network_connected(30)
    if stagecode == 3 and subcode == 1:
        print('Network connection successful!')
        resp = request.get(url)   # 发起http GET请求
        print(resp.json())  # 以json方式读取返回
    else:
        print('Network connection failed! stagecode = {}, subcode = {}'.format(stagecode, subcode))
```

运行结果

```py
>>> example.exec("/usr/test.py")

Network connection successful!

{'url': 'http://httpbin.org/get', 'headers': {'X-Amzn-Trace-Id': 'Root=1-6435a2ad-2d76fb8e753acad616d99a05', 'Host': 'httpbin.org'}, 'args': {}, 'origin': '39.144.15.119'}
```

## POST示例

POST常用于客户端向服务端推送消息使用

示例代码

```py
import request
import checkNet


PROJECT_NAME = "request_post_exam"
PROJECT_VERSION = "1.0.0"

checknet = checkNet.CheckNetwork(PROJECT_NAME, PROJECT_VERSION)


url = "http://httpbin.org/post"
data = {"key1": "value1", "key2": "value2", "key3": "value3"}


if __name__ == '__main__':
    stagecode, subcode = checknet.wait_network_connected(30)
    if stagecode == 3 and subcode == 1:
        print('Network connection successful!')
        resp = request.post(url, data=ujson.dumps(data))   # 发起http POST请求
        print(resp.json())  # 以json方式读取返回
    else:
        print('Network connection failed! stagecode = {}, subcode = {}'.format(stagecode, subcode))
```

运行结果

```py
>>> example.exec("/usr/test.py")

Network connection successful!

{'files': {}, 'headers': {'X-Amzn-Trace-Id': 'Root=1-6435a368-68dc753a6d709e625c35741f', 'Host': 'httpbin.org', 'Content-Length': '54'}, 'args': {}, 'form': {}, 'origin': '39.144.15.119', 'json': {'key2': 'value2', 'key3': 'value3', 'key1': 'value1'}, 'data': '{"key3": "value3", "key1": "value1", "key2": "value2"}', 'url': 'http://httpbin.org/post'}
```

## DELETE示例

delete请求用于客户端请求删除服务端数据，不常用。

示例代码

```py
import request
import checkNet


PROJECT_NAME = "request_delete_exam"
PROJECT_VERSION = "1.0.0"

checknet = checkNet.CheckNetwork(PROJECT_NAME, PROJECT_VERSION)


url = "http://httpbin.org/delete"


if __name__ == '__main__':
    stagecode, subcode = checknet.wait_network_connected(30)
    if stagecode == 3 and subcode == 1:
        print('Network connection successful!')
        resp = request.delete(url)   # 发起http DELETE请求
        print(resp.json())  # 以json方式读取返回
    else:
        print('Network connection failed! stagecode = {}, subcode = {}'.format(stagecode, subcode))
```

运行结果

```py
>>> example.exec("/usr/test.py")

Network connection successful!

{'files': {}, 'headers': {'X-Amzn-Trace-Id': 'Root=1-6435a431-08d97eb8539a76e068ea8bd9', 'Host': 'httpbin.org'}, 'args': {}, 'form': {}, 'origin': '39.144.15.119', 'json': None, 'data': '', 'url': 'http://httpbin.org/delete'}
```

## PUT示例

用于更新服务器资源，不常用



