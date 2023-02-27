from usr.WLAN import ESP8266
from machine import UART


# 初始化esp8266网卡
esp8266=ESP8266(UART.UART1, ESP8266.STA)
# 启动esp8266以staion模式启动
esp8266.station('iPhone 12 mini', '123456999')
# esp8266.station('QQ', '123456999')
# 获取当前网卡状态 4表示网卡已启用，可以进行下一步操作
# 0: esp8266设备不存在
# 1: esp8266 station模式已连接
# 2: esp8266 station模式未连接
# 3: esp8266 web配网模式
# 4: esp8266 ap模式
esp8266.status()
# 设置dns服务器地址
esp8266.set_dns('8.8.8.8', '114.114.114.114')
# 设置esp8266作为默认网卡，使用esp8266进行网络连接
ip = esp8266.ipconfig()[0]
esp8266.set_default_NIC(ip)

# esp8266.ipconfig()
# esp8266.stop()

'''
UART.UART1
'''
