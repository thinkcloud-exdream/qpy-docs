# 1. 简介

QuecPython提供了`gnss`功能模块来获取外置GNSS模块的定位数据。该功能模块直接在内部完成了原始定位数据的处理解析工作，将用户关心的一些定位参数提取出来并提供对应接口让用户可直接获取。避免了用户自己通过串口去读取原始的定位数据，并进行复杂的正则匹配查找和解析的情况，提高了用户开发效率。

目前该模块自动解析的NEMA语句包括：GGA、RMC和GSV。

> 本文档中示例代码前面有 `>>> `字符串的，表示在QuecPython的命令交互界面输入的代码。



# 2. 使用说明

`gnss`模块接口的详细说明，请参考QuecPython官网的Wiki文档中相关部分的说明。下面以L76K定位芯片为例，说明如何使用`gnss`模块的相关功能。

## 2.1 获取定位数据

下面将详细描述使用gnss模块接口获取定位数据的步骤，同时说明在使用过程中一些注意事项。

### 2.1.1 使用步骤

步骤1：确定串口信息

即确定L76K定位芯片接到模组哪个串口，以及使用的波特率等信息，本示例中将L76K接到了模组的UART2，波特率默认为9600bps（可在L76K使用手册中查询到）。



步骤2：实例化一个对象

```python
>>> from gnss import GnssGetData
>>> gnss_obj = GnssGetData(2, 9600, 8, 0, 1, 0)
```



步骤3：读取数据并解析

用户只需要调用如下接口，该接口直接完成定位数据的读取和解析工作：

```python
>>> gnss_obj.read_gnss_data()
822
```

上述接口将读取原始数据、以及复杂的解析操作都放在接口内部实现，只返回了通过串口读取的数据长度。如用户想看本次读取解析的原始数据，可调用如下接口：

```python
>>> data = gnss_obj.getOriginalData()
>>> print(data)
$GNGGA,063957.000,3802.01852,N,11437.92027,E,1,13,1.2,129.2,M,-15.7,M,,*62
$GNGLL,3802.01852,N,11437.92027,E,063957.000,A,A*40
$GNGSA,A,3,01,03,06,14,30,194,,,,,,,1.8,1.2,1.4,1*00
$GNGSA,A,3,13,23,33,38,40,43,59,,,,,,1.8,1.2,1.4,4*3C
$GPGSV,3,1,11,01,38,044,12,03,44,101,24,06,30,233,31,14,79,184,34,0*6F
$GPGSV,3,2,11,17,58,319,,19,40,296,04,21,11,051,,30,14,202,34,0*67
$GPGSV,3,3,11,194,44,156,27,195,68,074,,199,44,160,25,0*6F
$BDGSV,3,1,11,03,44,186,,07,83,121,05,10,65,309,,13,37,206,31,0*79
$BDGSV,3,2,11,23,21,181,31,28,69,354,14,33,24,115,27,38,65,190,30,0*7A
$BDGSV,3,3,11,40,70,093,18,43,28,065,15,59,38,143,29,0*44
$GNRMC,063957.000,A,3802.01852,N,11437.92027,E,0.69,168.35,260422,,,A,V*0B
$GNVTG,168.35,T,,M,0.69,N,1.29,K,A*2F
$GNZDA,063957.000,26,04,2022,00,00*44
$GPTXT,01,01,01,ANTENNA OPEN*25
```



步骤4：确认是否定位成功

如用户只关心是否定位到经纬度坐标以及坐标是否有效，可使用如下接口，返回1即表示定位成功且有效：

```python
>>> gnss_obj.isFix()
1
```



步骤5：获取坐标信息

调用如下接口即可获取到定位坐标：

```python
>>> gnss_obj.getLocation()
(114.6320045, 'E', 38.033642, 'N')
```



> 上述接口获取的坐标是WGS-84坐标系下的经纬度数据，不可直接用于高德地图、腾讯地图以及百度地图等地图上拾取位置信息，必须先转换为对应地图参考坐标系下的坐标。



### 2.1.2 示例代码

如下代码是一个完整的使用`gnss`模块方法来获取定位坐标的例程：

```python

import utime
from gnss import GnssGetData


def main():
    gnss_obj = GnssGetData(2, 9600, 8, 0, 1, 0)
    while True:
        try:
            read_size = gnss_obj.read_gnss_data()
        except Exception:
            print('数据异常，解析出错！')
            data = gnss_obj.getOriginalData()
            print('===============================================')
            print(data)
            print('===============================================')
            utime.sleep(2)
            continue

        if read_size > 0:
            if gnss_obj.isFix():
                coordinate = gnss_obj.getLocation()
                longitude = coordinate[0]
                latitude = coordinate[2]
                print('定位成功，当前经纬度：({}, {})'.format(longitude, latitude))
                utime.sleep(10)
            else:
                print('定位中，请稍后...')
                utime.sleep(2)
        else:
            print('未读取到定位数据...')
            utime.sleep(2)


if __name__ == '__main__':
    main()            
```



## 2.2 配置NEMA串口波特率

查阅L76K的使用手册，确定默认使用的波特率为9600bps，如用户需要修改波特率，则需要使用PCAS语句来发送一条修改波特率的指令给L76K芯片。

### 2.2.1 PCAS01指令格式

PCAS01语句即用来配置L76K的NEMA串口波特率。格式如下：

```
$PCAS01,<CMD>*<Checksum><CR><LF>
```

参数说明：

| 字段     | 描述                                                         |
| -------- | ------------------------------------------------------------ |
| CMD      | 支持如下波特率：<br>0 - 4800<br/>1 - 9600<br/>2 - 19200<br/>3 - 38400<br/>4 - 57600<br/>5 - 115200 |
| Checksum | 校验和，校验和是对语句中所有字符的 8 位（不包括起始和结束位）进行异或运算，所有字符是指在定界符“$”与“*”之间，但不包括这些定界符的全部字符，包括“,”在内。 |
| CR和LF   | NEMA语句的结束字符，即`\r\n`                                 |



### 2.2.2 步骤说明

步骤1：确定波特率

即确定需要配置的波特率，以确定CMD的值。假如需要配置L76K NEMA串口波特率为115200，即CMD为5。则PCAS01语句为：

```
$PCAS01,5*<Checksum>\r\n
```

步骤2：checksum计算

确定波特率后，PCAS01语句就只差checksum待计算，可按照如下算法计算：

```python

"""
参数说明
dstr - 需要计算校验和的字符串,对NEMA语句而言，即“$”与“*”之间的字符串
返回值：返回十进制的校验和
"""
def get_checksum(dstr):
    lista = list(dstr)
    list_len = len(lista) - 1
    checksum = ord(lista[0])
    i = 0
    while i < list_len:
        checksum = checksum ^ ord(lista[i+1])
        i = i + 1
    return checksum

# 取“$”与“*”之间的字符串
dstr = 'PCAS01,5'
checksum = get_checksum(dstr)
print('checksum={},{}'.format(checksum, hex(checksum)))

#计算结果
checksum=25,0x19
```

得到对应的checksum之后，可确定完整的PCAS01语句如下：

```
$PCAS01,5*19\r\n
```

步骤3：发送指令

使用machine类下的UART功能模块来发送该指令到L76K，本示例中将L76K接到了模组的UART2，具体如下：

```python

from machine import UART
from gnss import GnssGetData

# L76K默认波特率是9600，故先需要配置9600波特率来打开串口
uart2 = UART(UART.UART2, 9600, 8, 0, 1, 0)
# 发送波特率配置指令
uart2.write('$PCAS01,5*19\r\n')
# 配置成功后须先关闭当前串口
uart2.close()
# 按照115200波特率来示例话一个gnss对象
gnss_obj = GnssGetData(2, 115200, 8, 0, 1, 0)
```







