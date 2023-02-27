from usr.WLAN import ESP8266
from machine import UART

# 初始化esp8266网卡	
#若使用web配置ap模式，需把以下模式ESP8266设置为ESP8266.AP
esp8266=ESP8266(UART.UART1, ESP8266.STA)
# 使esp8266以web配网模式启动
esp8266.web_config('Chic_web','123456999')  # 配网网址：192.168.4.1
# 获取当前网卡状态 返回4表示已连接，可以使用esp8266进行下一步操作
# 0: esp8266设备不存在
# 1: esp8266 station模式已连接
# 2: esp8266 station模式未连接
# 3: esp8266 web配网模式
# 4: esp8266 ap模式
esp8266.status()
# 获取当前网卡状态 返回3表示web配网已启用，可以使用web配网模式

#使用手机等设备连接热点，使用浏览器进入网址192.168.4.1，进行配网

# esp8266.ipconfig()
# esp8266.stop()
