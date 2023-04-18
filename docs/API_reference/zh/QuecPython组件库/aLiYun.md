# aLiYun - 阿里云服务

## 初始化阿里云

### `aLiYun`

```python
aliyun = aLiYun(productKey, productSecret, DeviceName, DeviceSecret, MqttServer)
```

配置阿里云物联网套件的产品信息和设备信息

模块功能：阿里云物联网套件客户端功能,目前的产品节点类型仅支持“设备”，设备认证方式支持“一机一密和“一型一密”。

注意：BC25PA系列不支持模块功能。

* 参数

| 参数          | 类型   | 说明                                                         |
| ------------ | ----- | ------------------------------------------------------------ |
| productKey    | string | 产品标识                                                     |
| productSecret | string | 可选参数，默认为None，productSecret，产品密钥<br />一机一密认证方案时，此参数传入None<br/>一型一密认证方案时，此参数传入真实的产品密钥 |
| DeviceName    | string | 设备名称                                                     |
| DeviceSecret  | string | 可选参数,默认为Non，设备密钥（一型一密认证方案时此参数传入None） |
| MqttServer    | string | 可选参数,需要连接的服务器名称,默认为"{productKey}.iot-as-mqtt.cn-shanghai.aliyuncs.com" |

* 返回值

返回aLiYun连接对象。


## 设置相关功能和回调

### `aLiYun.setMqtt`

```python
aLiYun.setMqtt(clientID, clean_session, keepAlive=300,reconn=True)
```

设置MQTT数据通道的参数

**需要注意的是，当进行阿里云的一型一密连接的时候，会在本地生成secret.json的文件用以保存设备的设备密钥，如果重刷固件或者删除，再进行连接的时候会因为没有secret.json而报错，所以重刷固件或者删除了secert.json文件，需要手动新建secret.json文件，下面secret.json文件的模板**

```json
{
  "Test01": "9facf9aba414ec9eea7c10d8a4cb69a0"
}
# Test01 : 设备名
# "9facf9aba414ec9eea7c10d8a4cb69a0" 设备密钥
```

* 参数

| 参数          | 类型   | 说明                                                         |
| ------------ | ----- | ------------------------------------------------------------ |
| clientID      | string | 自定义阿里云连接id                                           |
| clean_session | bool   | 可选参数，一个决定客户端类型的布尔值。 如果为True，那么代理将在其断开连接时删除有关此客户端的所有信息。 如果为False，则客户端是持久客户端，当客户端断开连接时，订阅信息和排队消息将被保留。默认为False |
| keepAlive     | int    | 通信之间允许的最长时间段（以秒为单位）,默认为300，范围（60-1200） |
| reconn        | bool   | （可选）控制是否使用内部重连的标志，默认开启为True           |

* 返回值

成功返回整型值0，失败返回整型值-1。

### `aLiYun.setCallback`

```python
aLiYun.setCallback(sub_cb)
```

注册回调函数。

* 参数

| 参数   | 类型     | 说明     |
| -----  | -------  | -------- |
| sub_cb | function | 回调函数 |

* 返回值

无



### `aLiYun.error_register_cb`

```python
aLiYun.error_register_cb(callback)
```

设置异常回调函数，aliyun以及umqtt内部线程异常时通过回调返回error信息，该方法在设置不使用内部重连的情况下才可触发回调

* 参数 

| 参数     | 参数类型 | 说明         |
| -------- | -------- | ------------ |
| callback | function | 异常回调函数 |

* 返回值

无

异常回调函数示例

```python
from aLiYun import aLiYun

def err_cb(err):
    print("thread err:")
    print(err)

ali = aLiYun(productKey, productSecret, DeviceName, DeviceSecret)
ali.error_register_cb(err_cb)
```


## 订阅发布功能

### `aLiYun.subscribe`

```python
aLiYun.subscribe(topic,qos)
```

订阅mqtt主题。

* 参数

| 参数  | 类型   | 说明                                                         |
| :---- | :----- | ------------------------------------------------------------ |
| topic | string | topic                                                        |
| qos   | int    | MQTT消息服务质量（默认0，可选择0或1）0：发送者只发送一次消息，不进行重试  1：发送者最少发送一次消息，确保消息到达Broker |

* 返回值

成功返回整型值0，失败返回整型值-1。



### `aLiYun.publish`

```python
aLiYun.publish(topic,msg, qos=0)
```

发布消息。

* 参数

| 参数  | 类型   | 说明                                                         |
| :---- | :----- | ------------------------------------------------------------ |
| topic | string | topic                                                        |
| msg   | string | 需要发送的数据                                               |
| qos   | int    | MQTT消息服务质量（默认0，可选择0或1）0：发送者只发送一次消息，不进行重试  1：发送者最少发送一次消息，确保消息到达Broker |

* 返回值 

成功返回整型值0，失败返回整型值-1。

## 启停服务相关功能

### `aLiYun.start`

```python
aLiYun.start()
```

运行连接。

* 参数

无

* 返回值

无



### `aLiYun.disconnect`

```python
aLiYun.disconnect()
```

关闭连接。

* 参数

无

* 返回值

无



### `aLiYun.ping`

```python
aLiYun.ping()
```

发送心跳包

* 参数

无

* 返回值

无



### `aLiYun.getAliyunSta`

```python
aLiYun.getAliyunSta()
```

获取阿里云连接状态

注意：BG95平台不支持该API。

* 参数

无

* 返回值

0 ：连接成功

1：连接中

2：服务端连接关闭

-1：连接异常



**使用示例**

```python

import log
import utime
import checkNet
from aLiYun import aLiYun

'''
下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值
'''
PROJECT_NAME = "QuecPython_AliYin_example"
PROJECT_VERSION = "1.0.0"
checknet = checkNet.CheckNetwork(PROJECT_NAME, PROJECT_VERSION)


# 设置日志输出级别
log.basicConfig(level=log.INFO)
aliYun_log = log.getLogger("ALiYun")

productKey = ""  # 产品标识(参照阿里云应用开发指导)
productSecret = None  # 产品密钥（使用一机一密认证时此参数传入None，参照阿里云应用开发指导)
DeviceName = ""  # 设备名称(参照阿里云应用开发指导)
DeviceSecret = ""  # 设备密钥（使用一型一密认证此参数传入None，免预注册暂不支持，需先在云端创建设备，参照阿里云应用开发指导)

state = 5

# 回调函数
def sub_cb(topic, msg):
    global state
    aliYun_log.info("Subscribe Recv: Topic={},Msg={}".format(topic.decode(), msg.decode()))
    state -= 1


if __name__ == '__main__':
    stagecode, subcode = checknet.wait_network_connected(30)
    if stagecode == 3 and subcode == 1:
        aliYun_log.info('Network connection successful!')
        # 创建aliyun连接对象
        ali = aLiYun(productKey, productSecret, DeviceName, DeviceSecret)

        # 设置mqtt连接属性
        clientID = ""  # 自定义字符（不超过64）
        ali.setMqtt(clientID, clean_session=False, keepAlive=300)

        # 设置回调函数
        ali.setCallback(sub_cb)
        topic = ""  # 云端自定义或自拥有的Topic
        # 订阅主题
        ali.subscribe(topic)
        # 发布消息
        ali.publish(topic, "hello world")
        # 运行
        ali.start()

        while 1:
            if state:
                pass
            else:
                ali.disconnect()
                break
    else:
        aliYun_log.info('Network connection failed! stagecode = {}, subcode = {}'.format(stagecode, subcode))

```