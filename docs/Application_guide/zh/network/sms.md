# 短信

## 什么是短信

短信（Short Message Service）是一种通过移动通信网络传输文字信息的服务。短信可以用于发送文字、数字、符号等信息，每条短信的长度一般为160个字符。短信可以用于个人通信、商业宣传、政府通知等多种场合。短信服务通常需要用户购买短信套餐或者按条计费。 

本文档主要介绍如何使用 QuecPython 短信功能，通过本文你将了解到 QuecPython 短信的设置及使用方法。

#### 什么是PUD短信

PDU（Protocol Data Unit）短信是一种短信传输的编码格式，常用于GSM网络和3G网络中。相对于常见的文本格式短信（也称为ASCII短信），PDU短信可以在同样长度的情况下携带更多的信息。PDU短信包含多个字段，例如消息中心号码、目标号码、短信编码方式、短信内容等。

QuecPython 短信功能支持PDU短信的生成和解析。

## 怎么使用短信功能

### 硬件设计

短信功能主要是实体SIM卡通过UE来进行交互，除前提条件模块需要组网成功外无需其他外围硬件支持。

### 软件应用

#### 已实现功能

短信功能是移动通信网络中的一种基本服务，它可以实现文字、图片、音频等多种信息的快速传输和交流。

在QuecPython中短信功能的接口主要在[sms](/../../../API_reference/zh/QuecPython类库/sms.html)中。

下面是QuecPython短信功能的应用说明：

   	1. 短信发送：用户可以通过UE，向其他用户发送文字信息，支持发送TEXT类型的消息和PDU类型的消息。
   	2. 短信接收：用户可以接收来自其他用户或服务提供商发送的短信信息，包括广告信息、验证码等，支持PDU方式和TEXT方式。
   	3. 短信存储：UE可以将短信保存在本地，方便用户进行查看和管理，包括设置短信存储位置，获取短信数量；查看发送、删除和接收的短信。
   	4. 其它功能：如删除短信、PDU短信解析、短信中心号码配置、注册监听回调函数等

#### 软件实现示例

```Python
>>> import sms
# 发送TEXT短信
>>> sms.sendTextMsg('18158626517', '这是一条中文测试短信！', 'UCS2')
0
>>> sms.sendTextMsg('18158626517', 'Hello, world.', 'GSM')
0
>>> sms.sendTextMsg('18158626517', '这是一条夹杂中文与英文的测试短信,hello world!', 'UCS2')
0
# 发送PDU短信
>>> sms.sendPduMsg('18158626517', 'send pdu msg by GSM mode.', 'GSM')
0
>>> sms.sendPduMsg('18158626517', 'send pdu msg by UCS2 mode.', 'UCS2')
0
>>> sms.sendPduMsg('18158626517', '这是一条中文测试短信！通过PDU-UCS2模式', 'UCS2')  
0
# 删除短信
>>> sms.deleteMsg(2)  #删除索引号为2的那一条短信
0
>>> sms.deleteMsg(1,4)  #删除所有短信
0
# 获取短信数量
>>> sms.getMsgNums() # 执行本行前，先发送一条短信到模块
1
# 查询短信存储位置
>>> sms.getSaveLoc()
(['SM', 2, 50], ['SM', 2, 50], ['SM', 2, 50])
# 设置短信存储位置
>>> sms.setSaveLoc('SM','ME','MT')  
0
>>> sms.getSaveLoc()
(['SM', 2, 50], ['ME', 14, 180], ['MT', 2, 50])
>>> sms.sendPduMsg('+8618226172342', '123456789aa', 'GSM') # 自己给自己发送一条短信
# 以TEXT方式获取短信内容
>>> sms.searchTextMsg(0) 
('+8618226172342', '123456789aa', 22)
# 以PDU方式获取短信内容
>>> sms.searchPduMsg(0) # 下面PDU格式短信需要解码后才能正常显示短信内容
'0891683110305005F0240BA19169256015F70000022141013044230B31D98C56B3DD70B97018'
>>> sms.getPduLength(sms.searchPduMsg(0)) #注意，是获取PDU短信长度，不是上面字符串的长度
20
# 解析PDU短信内容
>>>sms.decodePdu('0891683110305005F0240BA19169256015F70000022141013044230B31D98C56B3DD70B97018',20)
('+8618226172342', '123456789aa', '2021-07-13 09:34:44', 40)
# 获取短信中心号码
>>> sms.getCenterAddr()
'+8613800551500'
# 注册监听收到短信回调函数
def cb(args):
    index = args[1]
    storage = args[2]
    print('New message! storage:{},index:{}'.format(storage, index))
sms.setCallback(cb)
```

