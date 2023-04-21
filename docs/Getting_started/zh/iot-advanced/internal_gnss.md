# 1. 简介

QuecPython提供了`quecgnss`功能模块来获取模组内置GNSS的定位数据。当前`quecgnss`模块暂不支持像`gnss`模块那样直接完成了原始定位数据的处理解析功能，而是需要用户自己来完成原始数据的处理解析工作。为了提高用户开发效率和使用便捷性，本指导文档中会直接给出较为完整的数据处理解析例程，供用户参考使用。

> 本文档中示例代码前面有 `>>> `字符串的，表示在QuecPython的命令交互界面输入的代码。



# 2. 使用说明

quecgnss模块的接口详细说明，请参考QuecPython官网的Wiki文档中相关部分的说明。本文档中主要从整体流程上说明quecgnss模块的使用方式。



## 2.1 获取定位数据

### 2.2.1 使用步骤

步骤1：功能初始化

内置GNSS功能默认是关闭的，需要用户主动初始化并开启。直接调用quecgnss模块的init接口即可完成初始化并打开的工作。如果初始化成功，则会返回0，失败返回-1。

```python
>>> import quecgnss
>>> quecgnss.init()
0
```



步骤2：确定GNSS的状态

内置GNSS功能初始化后，应确定GNSS当前的状态是否为”定位中“，只有处于这种状态，才可以开始读取NEMA数据。使用如下接口确定状态，返回值为2说明已经处于”定位中“的状态：

```python
>>> quecgnss.get_state()
2
```



步骤3：读取NEMA数据

当GNSS状态值为”定位中“时，即可使用如下接口去读取定位数据，读取出来的是尚未处理过的原始数据：

```python
>>> data = quecgnss.read(2048)
>>> print(data)
(2048, '$GNRMC,020943.00,A,3149.30070,N,11706.93208,E,0.052,,310323,,,A,V*15\r\n$GNGGA,020943.00,3149.30070,N,11706.93208,E,1,29,0.54,101.2,M,,M,,*52\r\n$GNGSA,A,3,07,08,09,16,21,27,31,04,194,199,195,50,1.06,0.54,0.91,1*3B\r\n$GNGSA,A,3,02,03,05,10,11,25,36,,,,,,1.06,0.54,0.91,3*0A\r\n$GNGSA,A,3,78,88,67,66,76,86,87,68,,,,,1.06,0.54,0.91,2*0C\r\n$GPGSV,5,1,17,04,48,238,45,07,20,314,40,08,63,215,48,09,37,285,44,0*65\r\n$GPGSV,5,2,17,16,50,034,45,21,09,175,40,27,77,054,48,31,15,124,43,0*63\r\n$GPGSV,5,3,17,18,08,045,,26,24,068,,194,65,058,43,199,51,161,41,0*6A\r\n$GPGSV,5,4,17,195,47,127,43,41,37,232,45,42,45,141,,50,51,161,45,0*59\r\n$GPGSV,5,5,17,40,15,254,41,0*55\r\n$GAGSV,3,1,09,02,21,281,36,03,42,271,40,05,33,201,42,10,34,093,42,0*7F\r\n$GAGSV,3,2,09,11,32,127,37,25,57,330,43,36,09,172,36,08,13,317,36,0*78\r\n$GAGSV,3,3,09,12,26,065,,0*49\r\n$GLGSV,3,1,10,66,13,216,32,67,26,269,37,68,13,319,34,76,40,058,36,0*7D\r\n$GLGSV,3,2, ......')# 数据较多，仅列出部分数据
```

需要注意的是，`quecgnss.read`接口返回值是一个元组，第一个参数是读取的数据长度，第二参数才是读取的数据，调试过程中，如果想让数据看起来整洁清晰，可按如下方式打印：

```python
>>> print(data[1].decode())
$GNRMC,020943.00,A,3149.30070,N,11706.93208,E,0.052,,310323,,,A,V*15
$GNGGA,020943.00,3149.30070,N,11706.93208,E,1,29,0.54,101.2,M,,M,,*52
$GNGSA,A,3,07,08,09,16,21,27,31,04,194,199,195,50,1.06,0.54,0.91,1*3B
$GNGSA,A,3,02,03,05,10,11,25,36,,,,,,1.06,0.54,0.91,3*0A
$GNGSA,A,3,78,88,67,66,76,86,87,68,,,,,1.06,0.54,0.91,2*0C
$GPGSV,5,1,17,04,48,238,45,07,20,314,40,08,63,215,48,09,37,285,44,0*65
$GPGSV,5,2,17,16,50,034,45,21,09,175,40,27,77,054,48,31,15,124,43,0*63
$GPGSV,5,3,17,18,08,045,,26,24,068,,194,65,058,43,199,51,161,41,0*6A
$GPGSV,5,4,17,195,47,127,43,41,37,232,45,42,45,141,,50,51,161,45,0*59
...... # 数据较多，仅列出部分数据
```

我们需要的定位信息就在上述这些NEMA语句中，比如经纬度坐标、海拔等。后面我们将讲述如何对这些数据进行处理解析，提取出我们需要的信息。



### 2.1.2 示例代码

如下例程，即是按照上述流程编写的较为完整的使用例程。

```python

"""
本例程示范了如何使用quecgnss模块的方法
例程中设定10s获取一次定位信息，仅为示例，实际可由用户自行决定获取定位信息的周期
"""
import utime
import quecgnss


def main():
    if quecgnss.get_state() == 0:
        ret = quecgnss.init()
        if ret == 0:
            print('GNSS 初始化成功')
        else:
            print('GNSS 初始化失败，请检查问题')
            return -1

    while True:
        gnss_state = quecgnss.get_state()
        if gnss_state == 2:
            print('GNSS 开始定位')
            break
        elif gnss_state == 1:
            print('GNSS 固件烧录中，请稍后')
            utime.sleep(2)
            continue
        else:
            print('GNSS 初始化异常，请检查问题')
            return -1

    while True:
        try:
            data = quecgnss.read(2048)
        except Exception as e:
            print('读取NEMA数据异常：{}'.format(e))
            utime.sleep(2)
            continue
        data_len = data[0]
        nema_data = data[1]
        if data_len == 0:
            print('未读到定位数据，重试中')
            utime.sleep(2)
        else:
            print('===============================================')
            print(nema_data.decode())
            print('===============================================')
            # 用户自行决定多久获取一次定位数据，此处10s仅为示例
            utime.sleep(10)
            # 注[1]
            try:
                quecgnss.read(4096)
            except Exception as e:
                print('{}'.format(e))
            utime.sleep(2)
            continue


if __name__ == '__main__':
    main()
    
```



> 注[1]
>
> 上述示例代码中，在休眠一段时间后，读取了4K的定位数据并丢弃了。这段代码的作用如下：
>
> 实际使用中，设备可能会间隔较长一段时间才会获取一次定位数据。有的模组，串口部分底层驱动代码缓存机制是如果缓存满了，就不会再接收新的数据；这就导致如果设备在移动中，间隔较长一段时间才获取一次定位信息时，获取到的是较长时间之前缓存的定位数据，而不是当前位置实时的定位信息。所以为了确保这种情形下，每次获取的定位信息都是实时的，需要在每次获取定位数据之前，先读一次串口数据，把串口缓存中的数据读出并丢弃，休眠1~2s后再读定位数据。
>
> 如设备获取定位信息较为频繁，可去掉上述代码片段。



## 2.2 数据解析

NEMA语句都是以字符`$`开头，并且以`\r\n`作为结束。而从一堆原始数据中找到我们需要的某一条NEMA语句，本质上利用的就是NEMA语句的该特点，比如正则匹配或是判断字符串头尾。

下面以获取经纬度坐标信息为例，说明对NEMA语句的处理解析过程。经纬度坐标信息在RMC和GGA语句中都有包含，下面例程中以从RMC语句中提取经纬度信息为例进行说明。

### 2.2.1 解析步骤

步骤1：查找相关RMC语句

从读取的原始数据中找出RMC语句，这里使用的方式为——先分割再查找。

在这种先分割再查找的方式中，需要注意的是，对原始数据的分割，必须使用字符`$`来分割。理论上每一条NEMA语句都应以字符`$`开始，以`\r\n`结束。但在实际的定位数据中，会出现一些NEMA语句不完整的情况，即某一条或几条NEMA语句缺少了一部分，并且直接和下一条语句粘在了一起。比如：

```
$GPGSV,4,2,16,21,2$GNRMC,024843.00,A,3149.30313,N,11706.92780,E,0.157,,310323,,,A,V*16
```

这种情况下，使用字符`$`来分割原始字符串数据，可以将这种两条粘在一起的语句分割开，再结合”NEMA语句都应以字符`$`开始，以`\r\n`结束“的特性加以判断，基本可以避免获取到不正常的语句导致后续解析出错的情况。

下面示例中data中就是通过`quecgnss.read`接口读出的原始数据，数据如下：

```python
(2048,'*3B\r\n$GNGSA,A,3,02,11,25,30,34,36,,,,,,,1.20,0.65,$GNRMC,060154.00,A,3149.30510,N,11706.93089,E,0.016,,310323,,,A,V*17\r\n$GNGGA,0$GNRMC,062306.00,A,3149.30472,N,11706.93365,E,0.053,,310323,,,A,V*15\r\n$GNGGA,062306.00,3149.30472,N,11706.93365,E,1,28,0.59,91.9,M,,M,,*6C\r\n$GNGSA,A,3,01,03,07,14,17,21,30,194,199,195,19,06,0.99,0.59,0.80,1*3D\r\n$GNGSA,A,3,02,11,25,30,34,36,15,,,,,,0.99,0.59,0.80,3*07\r\n$GNGSA,A,3,78,80,79,88,82,81,,,,,,,0.99,0.59,0.80,2*0C\r\n$GPGSV,5,1,17,01,63,040,46,03,31,131,42,06,08,220,40,07,26,193,44,0*63\r\n$GPGSV,5,2,17,14,60,326,45,17,39,294,43,19,15,273,43,21,35,041,42,0*6E\r\n$GPGSV,5,3,17,30,43,234,45,08,14,073,,194,61,126,45,199,51,161,40,0*64\r\n$GPGSV,5,4,17,195,69,065,46,42,45,141,,50,51,161,44,40,15,254,41,0*53\r\n$GPGSV,5,5,17,41,37,232,44,0*51\r\n$GAGSV,2,1,07,02,82,078,40,11,12,040,32,15,10,223,35,25,33,129,36,0*7D\r\n$GAGSV,2,2,07,30,37,319,39,34,61,229,44,36,60,034,41,0*4D\r\n$GLGSV,2,1,07,78,52,161,45,79,68,316,41,80,15,330,34,81,61,325,38,0*79\r\n$GLGSV,2,2,07,82,34,252,33,88,26,031,33,65,04,073,,0*43\r\n$GNRMC,062307.00,A,3149.30472,N,11706.93366,E,0.023,,310323,,,A,V*10\r\n$GNGGA,062307.00,3149.30472,N,11706.93366,E,1,28,0.59,91.9,M,,M,,*6E\r\n$GNGSA,A,3,01,03,07,14,17,21,30,194,199,195,19,06,0.99,0.59,0.80,1*3D\r\n$GNGSA,A,3,02,11,25,30,34,36,15,,,,,,0.99,0.59,0.80,3*07\r\n$GNGSA,A,3,78,80,79,88,82,81,,,,,,,0.99,0.59,0.80,2*0C\r\n$GPGSV,5,1,17,01,63,040,46,03,31,131,42,06,08,220,40,07,26,193,44,0*63\r\n$GPGSV,5,2,17,14,60,326,44,17,39,294,45,19,15,273,43,21,35,041,42,0*69\r\n$GPGSV,5,3,17,30,43,234,44,08,14,073,,194,61,126,47,199,51,161,40,0*67\r\n$GPGSV,5,4,17,195,69,065,46,42,45,141,,50,51,161,43,40,15,254,42,0*57\r\n$GPGSV,5,5,17,41,37,232,44,0*51\r\n$GAGSV,2,1,07,02,82,078,40,11,12,040,32,15,10,223,34,25,33,129,36,0*7C\r\n$GAGSV,2,2,07,30,37,319,39,34,61,229,44,36,60,034,42,0*4E\r\n$GLGSV,2,1,07,78,52,161,45,79,68,316,41,80,15,330,35,81,61,325,38,0*78\r\n$GLGSV,2,2,07,82,34,252,33,88,26,031,32,65,04,073,,0*42\r\n$GNRMC,062308.00,A,3149.30473,N,11706.93366,E,0.032,,310323,,,A,V*1E\r\n$GNGGA,062308.00,3149.30473,N,11706.9336')
```

解析代码如下：

```python

rmc = ''
split_data = data[1].split('$')
for i in split_data:
    # 查找RMC语句并进行数据完整性检查
    if i.startswith('GNRMC') and i.endswith('\r\n'):
        rmc = i
        split_rmc = rmc.split(',')
        break
print(rmc)
print(split_rmc)

############执行结果如下################
GNRMC,060154.00,A,3149.30510,N,11706.93089,E,0.016,,310323,,,A,V*17
['GNRMC', '060154.00', 'A', '3149.30510', 'N', '11706.93089', 'E', '0.016', '', '310323', '', '', 'A', 'V*17\r\n']

```



步骤2：语句完整性校验

上述解析代码中，判断是否以`GNRMC`开头并且以`\r\n`结尾，本身也是一种完整性检查。如果用户希望更准确的检查某一条NEMA语句的完整性，那就需要对该条语句进行checksum计算，并将计算结果与该条语句中的checksum进行比较，如果相等，则说明该条语句是完整且正确的。

这里提供一个校验NEMA语句checksum的接口：

```python

"""
功能：checksum计算
参数说明:
dstr - 需要计算校验和的字符串，应取NEMA语句的”$“字符和”*“字符之间的部分，不包含”$“字符和”*“字符
返回值：返回十六进制字符串类型的checksum
"""
def checksum(dstr):
    lista = list(dstr)
    list_len = len(lista) - 1
    tmp = ord(lista[0])
    i = 0
    while i < list_len:
        tmp = tmp ^ ord(lista[i+1])
        i = i + 1
    strtmp = str(hex(tmp))
    return strtmp.replace('0x', '')

"""
功能：NEMA语句checksum确认
参数说明:
nema - 一条以‘$’字符开始和‘\r\n’字符结束的NEMA语句
返回值：checksum校验通过返回Ture，否则返回False
"""
def checksum_verify(nema):
    find_sck = ure.search("\*(.+?)\r\n", nema)
    if find_sck:
        sck = find_sck.group(1)
    else:
        return False
    data = ure.search("\$(.+?)\*", nema)
    if data:
        print('待计算数据：{}'.format(nema))
        ck = checksum(data.group(1))
        print('计算checksum为：{}'.format(ck))
        if ck.upper() == sck.upper():
            return True
        else:
            return False
    else:
        return False
    
```



步骤3：确认定位有效性

在获取经纬度数据之前，应先确认当前定位数据是有效的，这里是通过检查RMC语句中的`Status`位来判断是否有效，该位表示定位系统状态。当`Status`为字符`A`时，即表示有效。

RMC语句格式：

```
$<TalkerID>RMC,<UTC>,<Status>,<Lat>,<N/S>,<Lon>,<E/W>,<SOG>,<COG>,<Date>,<MagVar>,<MagVarDir>,<ModeInd>,<NavStatus>*<Checksum><CR><LF>
```

以步骤1中查找到的RMC数据为例：

```python

# 通过步骤1可知split_rmc如下
split_rmc = ['GNRMC', '060154.00', 'A', '3149.30510', 'N', '11706.93089', 'E', '0.016', '', '310323', '', '', 'A', 'V*17\r\n']

if split_rmc[2] == 'A':
    print('有效定位')
else:
    print('无效定位')
    
```



步骤4：提取经纬度坐标

确定定位数据有效后，即可提取经纬度相关信息。需注意的是，提取出的数据默认都是字符串，需要转换为浮点数：

```python

lat = float(split_rmc[3])
lon = float(split_rmc[5])
print('经度信息：{}'.format(lon))
print('纬度信息：{}'.format(lat))

############执行结果如下################
经度信息：11706.93089
纬度信息：3149.3051

```



步骤5：将经纬度数据转换为单位为”度“的坐标

查阅NEMA语句格式说明可知，NEMA语句中的经纬度格式如下：

| 字段 | 格式        | 说明                                                         |
| ---- | ----------- | ------------------------------------------------------------ |
| Lat  | ddmm.mmmmm  | 纬度<br>dd - 度（00-90）<br/>mm - 分（00-59）<br/>mmmmm - 分的十进制小数 |
| Lon  | dddmm.mmmmm | 经度<br/>ddd - 度（000-180）<br/>mm - 分（00-59）<br/>mmmmm - 分的十进制小数 |

转换计算如下：

```python

longitude = lon // 100 + (lon % 100) / 60
latitude = lat // 100 + (lat % 100) / 60
print('({}, {})'.format(longitude, latitude))

############执行结果如下################
(117.1155148333333, 31.82175166666667)

```



> 此处计算出来的是WGS-84坐标系下经纬度坐标，不可直接用于高德、腾讯、百度等地图上。



### 2.2.2 示例代码

下面示例是基于2.1.2章节中的代码基础上，增加了数据解析部分的代码。

```python

"""
本例程示范了如何使用quecgnss模块的方法
例程中设定10s获取一次定位信息，仅为示例，实际可由用户自行决定获取定位信息的周期
"""
import ure
import utime
import quecgnss

cycle = 10

def checksum(dstr):
    lista = list(dstr)
    list_len = len(lista) - 1
    tmp = ord(lista[0])
    i = 0
    while i < list_len:
        tmp = tmp ^ ord(lista[i+1])
        i = i + 1
    strtmp = str(hex(tmp))
    return strtmp.replace('0x', '')

def checksum_verify(nema):
    find_sck = ure.search("\*(.+?)\r\n", nema)
    if find_sck:
        sck = find_sck.group(1)
    else:
        return False
    data = ure.search("\$(.+?)\*", nema)
    if data:
        print('待计算数据：{}'.format(nema))
        ck = checksum(data.group(1))
        print('计算checksum为：{}'.format(ck))
        if ck.upper() == sck.upper():
            return True
        else:
            return False
    else:
        return False


def main():
    global cycle
    if quecgnss.get_state() == 0:
        ret = quecgnss.init()
        if ret == 0:
            print('GNSS 初始化成功')
        else:
            print('GNSS 初始化失败，请检查问题')
            return -1

    while True:
        gnss_state = quecgnss.get_state()
        if gnss_state == 2:
            print('GNSS 开始定位')
            break
        elif gnss_state == 1:
            print('GNSS 固件烧录中，请稍后')
            utime.sleep(2)
            continue
        else:
            print('GNSS 初始化异常，请检查问题')
            return -1

    while True:
        try:
            data = quecgnss.read(2048)
        except Exception as e:
            print('读取NEMA数据异常：{}'.format(e))
            utime.sleep(2)
            continue
        data_len = data[0]
        nema_data = data[1]
        if data_len == 0:
            print('未读到定位数据，重试中')
            utime.sleep(2)
        else:
            print('===============================================')
            print(nema_data.decode())
            print('===============================================')
            split_nema = nema_data.split('$')
            for i in split_nema:
                if i.startswith('GNRMC') and i.endswith('\r\n'):
                    split_rmc = i.split(',')
                    if split_rmc[2] == 'A':
                        print('获取到有效定位')
                        # 确认定位有效后，再计算checksum确认语句完整性，避免对无效数据进行计算
                        # 用户自行决定是否需要计算，如不需要可屏蔽checksum校验相关代码
                        rmc = i.replace('GNRMC', '$GNRMC')
                        if not checksum_verify(rmc):
                            continue
                        print('checksum 校验通过')
                        
                        lat = float(split_rmc[3])
                        lon = float(split_rmc[5])
                        longitude = lon // 100 + (lon % 100) / 60
                        latitude = lat // 100 + (lat % 100) / 60
                        print('经纬度坐标：({}, {})'.format(longitude, latitude))
                        break
                    else:
                        continue
            # 用户自行决定多久获取一次定位数据，此处10s仅为示例
            utime.sleep(cycle)
            # 下面这段代码是否需要，取决于用户获取定位的频繁程度。
            if cycle > 60:
                try:
                    quecgnss.read(4096)
                except Exception as e:
                    print('{}'.format(e))
                utime.sleep(2)
                
            continue


if __name__ == '__main__':
    main()
    
```
