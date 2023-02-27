from usr.WLAN import ESP8266
from machine import UART
import dataCall

# 初始化esp8266网卡
esp8266 = ESP8266(UART.UART1, ESP8266.AP)
# 启动esp8266以ap模式启动
esp8266.ap('Chic_ap', '123456999')
# 获取当前网卡状态 4表示网卡已启用，可以进行下一步操作
# 0: esp8266设备不存在
# 1: esp8266 station模式已连接
# 2: esp8266 station模式未连接
# 3: esp8266 web配网模式
# 4: esp8266 ap模式
esp8266.status()
# 获取拨号信息
Info = dataCall.getInfo(1, 0)
# 设置默认网卡
esp8266.set_default_NIC(Info[2][2])
# 添加路由信息，设置网卡转发规则，默认ap的网段192.168.4.0，子网掩码255.255.255.0
esp8266.router_add('192.168.4.0', '255.255.255.0')

# esp8266.ipconfig()
# esp8266.stop()

'''
UART.UART1
'''