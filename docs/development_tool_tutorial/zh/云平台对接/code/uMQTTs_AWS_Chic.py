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
