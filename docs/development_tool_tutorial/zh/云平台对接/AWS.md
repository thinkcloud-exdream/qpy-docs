# 云平台对接-AWS应用开发

## 什么是云平台AWS

AWS 全称Amazon web service(亚马逊网络服务),是亚马逊公司旗下云计算服务平台,为全世界各个国家和地区的客户提供一整套基础设施和云解决方案。 AWS面向用户提供包括弹性计算、存储、数据库、物联网在内的一整套云计算服务,帮助企业降低IT投入和维护成本,轻松上云 从概念是来看,AWS提供了一系列的托管产品,帮助我们在没有物理服务器的情况下,照样可以正常完成软件开发中的各种需求,也就是我们常说的云服务。

## 怎么使用云平台AWS

#### 【进入平台】

[亚马逊云首页](https://amazonaws-china.com/cn/)点击【产品】---【物联网】---【AWS IoT Core】

![image-20230301153819079](../media/云平台对接/AWS/云平台对接AWS_01.png)

![image-20230301154126556](../media/云平台对接/AWS/云平台对接AWS_02.png)

![image-20230301154323459](../media/云平台对接/AWS/云平台对接AWS_03.png)

#### 【创建策略】

![image-20230301154602272](../media/云平台对接/AWS/云平台对接AWS_04.png)

![image-20230301155516253](../media/云平台对接/AWS/云平台对接AWS_05.png)

#### 【创建物品】

![image-20230301161042093](../media/云平台对接/AWS/云平台对接AWS_06.png)

![image-20230301161125928](../media/云平台对接/AWS/云平台对接AWS_07.png)

![image-20230301161323026](../media/云平台对接/AWS/云平台对接AWS_08.png)

![image-20230301161410209](../media/云平台对接/AWS/云平台对接AWS_09.png)

![image-20230301161505534](../media/云平台对接/AWS/云平台对接AWS_10.png)

![image-20230301161743688](../media/云平台对接/AWS/云平台对接AWS_11.png)

![image-20230301161854690](../media/云平台对接/AWS/云平台对接AWS_12.png)

至此完成“创建物品”。用证书连接AWS IoT平台，同一个证书可以用于多个设备，不同设备的Client ID保持唯一。



#### 【设备通信】

获取AWS服务器的MQTT连接地址、端口：

![image-20230301163235249](../media/云平台对接/AWS/云平台对接AWS_13.png)

使用MQTT.fx工具测试通信，在订阅主题栏填写“#”，表示接收所有主题。

![13](../media/云平台对接/AWS/云平台对接AWS_14.png)

![12](../media/云平台对接/AWS/云平台对接AWS_15.png)

 



### 软件应用

看到代码在创建MQTTClient的时间，设置了ssl=True，"cert": certificate_content，"key": private_content 等关键参数，其中证书是在AWS平台下载获取。

```python
from umqtt import MQTTClient
import modem
import _thread
import checkNet
import utime
from misc import Power

CLIENT_ID = b'Chic_001'
SERVER = b'ambzd54j67b7h-ats.iot.us-west-2.amazonaws.com'
PORT = 8883
USER = None  # b''
PASSWORD = None  # b''

# 1. 数字证书 (certificate.crt)
# 2. 私钥	(private.pem)

certificate_content = """
-----BEGIN CERTIFICATE-----
MIIDWjCCAkKgAwIBAgIVAKxYi7zakXXKtbz5k2T72amn9k0GMA0GCSqGSIb3DQEB
CwUAME0xSzBJBgNVBAsMQkFtYXpvbiBXZWIgU2VydmljZXMgTz1BbWF6b24uY29t
IEluYy4gTD1TZWF0dGxlIFNUPVdhc2hpbmd0b24gQz1VUzAeFw0yMjA2MDYwNzU1
MzNaFw00OTEyMzEyMzU5NTlaMB4xHDAaBgNVBAMME0FXUyBJb1QgQ2VydGlmaWNh
dGUwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDW9JpDiRLvYBt/62o7
1fGfXG+MH9fC4+AnjPT1Kn4l1jKulEyix6ICGXL2+Ms77GXJrB+uIpMb4NgxG2D1
qeA/xDKkh2QHXWvXsVf2KqWjRekprHLLNDWjZuig14cOhaDrIRlQfPoMMFsnehBZ
BUwyZZferg9u/GXor5hKAkLSpmCLsMAex6tn1f/ZpNwrrXABumLD+GX64L0XUla9
kzj7b7qc2bSLirQVCmS44tk3Jvu2B3eS8Xf05CNkTLvdlHWhjepLtyDbukj9/HIJ
+CC0uYk7OYmfz85RhfVM0jbmFd2ebFS9yLnTsM0MZ/9weV/1NbEbQwwNnajKy3Q9
LcsHAgMBAAGjYDBeMB8GA1UdIwQYMBaAFBruG06tF4R5Jac0d3Vq+WPmtW8hMB0G
A1UdDgQWBBSzpZijfWVvj/e9yy/+mYFP46lPgjAMBgNVHRMBAf8EAjAAMA4GA1Ud
DwEB/wQEAwIHgDANBgkqhkiG9w0BAQsFAAOCAQEAIxfbQzXNn8wnSOd/O1mEKdpu
nqw1FScwBSrKAx5IMb4LouOwl2OiLvPRNyCvKF5vVRsLHlCVFC2F4epJ2GgUhkid
rE0aiIACPgmtjF1vzHRU8nMOLKMsqE0gehw5zlqWaVKICIBe8ZrzTspipONeJL/B
MUWc5Jc1LoR37CmUKe2M//b3dh1Q4/aaSYEWG1J1cAk0mpKogBhJzK/JIsnzoW8D
Ho9pMvj8hdd5/PVx4Euj02IkG/uoxLqAcUu7TPotu5kTa5SWPhk7PANv84rlN5Xn
FyqMdt3hj3kHutTAv+MjAvjp/nmoi80NVEHhNlXYb2Cs4b877xxHMv/uzmZI7A==
-----END CERTIFICATE-----
"""

private_content = """
-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEA1vSaQ4kS72Abf+tqO9Xxn1xvjB/XwuPgJ4z09Sp+JdYyrpRM
oseiAhly9vjLO+xlyawfriKTG+DYMRtg9angP8QypIdkB11r17FX9iqlo0XpKaxy
yzQ1o2booNeHDoWg6yEZUHz6DDBbJ3oQWQVMMmWX3q4Pbvxl6K+YSgJC0qZgi7DA
HserZ9X/2aTcK61wAbpiw/hl+uC9F1JWvZM4+2+6nNm0i4q0FQpkuOLZNyb7tgd3
kvF39OQjZEy73ZR1oY3qS7cg27pI/fxyCfggtLmJOzmJn8/OUYX1TNI25hXdnmxU
vci507DNDGf/cHlf9TWxG0MMDZ2oyst0PS3LBwIDAQABAoIBAEqP7FbS3HOWRdO4
iFAbJUYfHT5g6UncG6v8dBf61mkvhMMUBAVO9D6AL2XF5VFy7dfn0dFogtjfxH48
PgTZGUVlPB/gKu13FWprRNTJ9EzPelKPU/5yrMxybO0l9d4usiP9hjdqMp45w9TM
vZDzinvMy8JdZFMeUAdHqa66XA2PL99kaRbptzWx3nX60auDMIIvzO7mORdl+TwU
AFX5VA7ixkIWl55gH45exU6U1Px93WeUaG05QtECtj69MjQevgcT+xJ8bk7qZYjD
nHsyuf3MRdt5mASNG29dA3/WIbBPfn+65RdZFNm2KdGV78pDsoLQEZJU+iGqPq2E
QNcZeBECgYEA9845Qo4O0adLxStNwBszSROWp2zmitF1dAEBb8Ycjdngy/XplwLO
0+1xJAyek2Vjam8oHEmvGNr3QUqlIIP8xKBZs2zZyxiYYo/E4h4J5QIV1uQL/Zqe
wE+2wfVCgfMhjOnXDPjuSyV9NkwQxYYsHQv4X6RKN3QrYysyqDVoDFkCgYEA3hBK
F2C9jm7OOO0M77EQGwAb4aSIlSfJFXcl6ef18Rgido2oiA3GssckorssxorGdnhj
0lIgFK84SPokGYFVc5xh93zL9hskSEyrHDceeVAfsnp/xTmwk4Z+ngJrfCpP6mrx
I8DGVxc2MgurXYsVS8Gx7zqmqe9Uvchf0qAcJl8CgYAifd/WdbN2VxTi0s41qROQ
Xluf3jaQp+rzRJiQmECtNeBmQ0pKLKfhM7GF1QPVfE1EKUip90+Z5BB6VAt75SMv
syoJIWOHM1syjNRYrNmvuISVrpRErlreZboIcTzanZ7T4FCAi72PVB6Dij7jX3OQ
b3QYy+NQqKjJWt/oLdbXsQKBgFO1rkhrxmkn6gNZkPPWOm0DOH9x567aZZn65Ubs
kzDEWVF5ixtmng2MtonFp1Zcv/2u2mpRXRiPCNexu+QFdjHztJZ36+clSiMbC7HC
MXGnu5srRHkTizXBkH9+CAixZpjGoYpJxDrWXC63aW0E3g1Fwg6dfHA48Sftnfmn
M5VfAoGAUUBGEbg7kImiSx1r357EMB2Vt4UwgWdY5idiaajYEJNSPIlrsBbi5WZH
X6R85MWT+UD9Y7FSiZo2acf/rO4CUWZcqSI22KgErBB4boBpwtVLMpF+MGFR9b5G
as/T8DAMikugyGkzogMGMZEK7DLfXwSA7VuiQ/uiSA3kMCLHesM=
-----END RSA PRIVATE KEY-----
"""


IMEI = None  # modem.getDevImei()
SUB_TOPIC = '{}'
PUB_TOPIC = SUB_TOPIC

def sub_cb(topic, msg):
    global c
    print(
        "Subscribe Recv: Topic={},Msg={}".format(
            topic.decode(),
            msg.decode()))


def wait_msg():
    global c
    while True:
        if c is not None:
            c.wait_msg()
            # ret = c.get_mqttsta()
            # print('wait_msg get_mqttsta:', ret)
            utime.sleep_ms(100)


def MQTT_PUB():
    global c
    while True:
        try:
            if c is not None:
                c.publish(PUB_TOPIC.format(IMEI), "Hello World!")
                # c.publish(PUB_TOPIC.format(IMEI), bytearray(b'\x30\x31\x32\x33\x00\x01\x02\x03'))
                utime.sleep_ms(3000)
                # ret = c.get_mqttsta()
                # print('MQTT_PUB get_mqttsta:', ret)
        except BaseException as e:
            print('BaseException, Resatrting...', e)


def MQTT_Init():
    global c

    # 创建一个mqtt实例
    c = MQTTClient(
        client_id=CLIENT_ID,
        server=SERVER,
        port=PORT,
        user=USER,
        password=PASSWORD,
        keepalive=30,
        ssl=True,
        ssl_params={
            "cert": certificate_content,
            "key": private_content})
    # 设置消息回调
    c.set_callback(sub_cb)
    # 设置遗嘱消息
    c.set_last_will(
        topic='set_last_will',
        msg='set_last_will',
        retain=False,
        qos=1)
    # 建立连接
    c.connect()
    # 订阅主题
    c.subscribe(SUB_TOPIC.format(IMEI))
    # 发布消息
    c.publish(PUB_TOPIC.format(IMEI), "Hello World!")

    # 关闭连接
    # c.disconnect()


def GetDevImei():
    global IMEI
    IMEI = modem.getDevImei()
    print(IMEI)


def main():
    GetDevImei()
    MQTT_Init()
    _thread.start_new_thread(MQTT_PUB, ())
    _thread.start_new_thread(wait_msg, ())


if __name__ == '__main__':
    stagecode, subcode = checkNet.wait_network_connected(30)
    print('stagecode = {}, subcode = {}'.format(stagecode, subcode))
    if stagecode == 3 and subcode == 1:
        print('Network connection successful!')
    else:
        print('Not Net, Resatrting...')
        utime.sleep_ms(200)
        Power.powerRestart()
        
    main()

```

## 云平台AWS功能测试

使用QPYcom运行代码，下面实例是基于uMQTT执行连接云平台的效果。

![image-20230301165904773](../media/云平台对接/AWS/云平台对接AWS_16.png)

## 云平台AWS功能应用实例

[uMQTTs_AWS_Chic.py](./code/uMQTTs_AWS_Chic.py)

