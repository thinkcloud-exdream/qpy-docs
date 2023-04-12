# 7.2阿里云

本章节内容将介绍QuecPython开发接入阿里云实验。

## 7.2.1云平台设置

阿里云首页：[https://www.aliyun.com](https://www.aliyun.com/)

进入首页后点击【产品】---【物联网】---【物联网平台】

![](E:\QuecPython网站搬移\V3\teedoc_with_qpydoc_1\docs\Getting_started\zh\media\coulds\iot_aliyun\iot_aliyun_1.jpg)

点击【进入控制台】

![](E:\QuecPython网站搬移\V3\teedoc_with_qpydoc_1\docs\Getting_started\zh\media\coulds\iot_aliyun\iot_aliyun_2.jpg)

登录阿里云账号之后选择【地区】，点击【公共实例】

![](E:\QuecPython网站搬移\V3\teedoc_with_qpydoc_1\docs\Getting_started\zh\media\coulds\iot_aliyun\iot_aliyun_3.jpg)

点击【产品】---【创建产品】

![](E:\QuecPython网站搬移\V3\teedoc_with_qpydoc_1\docs\Getting_started\zh\media\coulds\iot_aliyun\iot_aliyun_4.jpg)

点击【设备】---【添加设备】

![](E:\QuecPython网站搬移\V3\teedoc_with_qpydoc_1\docs\Getting_started\zh\media\coulds\iot_aliyun\iot_aliyun_5.jpg)

获取阿里云连接的三元组，ProductKey、DeviceName、DeviceSecret

![](E:\QuecPython网站搬移\V3\teedoc_with_qpydoc_1\docs\Getting_started\zh\media\coulds\iot_aliyun\iot_aliyun_6.jpg)

查看云端Topic，点击【产品】---【查看】---【Topic类列表】，这里有基础通信Topic、物模型通信Topic和自定义Topic，可自行选择对应的Topic

![](E:\QuecPython网站搬移\V3\teedoc_with_qpydoc_1\docs\Getting_started\zh\media\coulds\iot_aliyun\iot_aliyun_7.jpg)

![](E:\QuecPython网站搬移\V3\teedoc_with_qpydoc_1\docs\Getting_started\zh\media\coulds\iot_aliyun\iot_aliyun_8.jpg)

## 7.2.2软件编写

软件编程可参考官网wiki上面阿里云这一章节，有相关的API介绍，下面是示例代码:

```python
import log
import utime
import checkNet
from aLiYun import aLiYun

PROJECT_NAME = "QuecPython_AliYin_example"
PROJECT_VERSION = "1.0.0"
checknet = checkNet.CheckNetwork(PROJECT_NAME, PROJECT_VERSION)

# 设置日志输出级别
log.basicConfig(level=log.INFO)
aliYun_log = log.getLogger("AliYun")

class aliyunObject(object):
    def __init__(self,productKey, productSecret, DeviceName, DeviceSecret):
        self.productKey = productKey
        self.productSecret = productSecret
        self.DeviceName = DeviceName
        self.DeviceSecret = DeviceSecret
        self.sub_cb
        self.topic = '/sys/he6c0ZOSXJ3/{}/thing/event/property/post'.format(self.DeviceName)  # 云端自定义或自拥有的Topic 
  
        
    def ali_connect(self):
        ali = aLiYun(self.productKey, self.productSecret, self.DeviceName, self.DeviceSecret)
        print("------")
        clientID = "111111"  # 自定义字符（不超过64）
        ali.setMqtt(clientID, clean_session=False, keepAlive=300)

        # 设置回调函数
        ali.setCallback(self.sub_cb)
        
        # 订阅主题
        ali.subscribe(self.topic)
        data = "hello world"
        ali.publish(self.topic, data)
        ali.start()
        

    def sub_cb(self,topic, msg):
        aliYun_log.info("Subscribe Recv: Topic={},Msg={}".format(topic.decode(), msg.decode()))
if __name__ == "__main__":
    stagecode, subcode = checknet.wait_network_connected(30)
    if stagecode == 3 and subcode == 1:
        try:
            aliYun_log.info('Network connection successful!')
            aliyun = aliyunObject("he6c0ZOSXJ3",None,"oIagpQK7IR9SAbfjRmUy","121168c0b39e4df49ade5147671ff440")
            aliyun.ali_connect()
        except Exception as e:
            aliYun_log.info(e)
    else:
        aliYun_log.info('Network connection failed! stagecode = {}, subcode = {}'.format(stagecode, subcode))


```



## 7.2.3下载验证

![](E:\QuecPython网站搬移\V3\teedoc_with_qpydoc_1\docs\Getting_started\zh\media\coulds\iot_aliyun\iot_aliyun_9.jpg)