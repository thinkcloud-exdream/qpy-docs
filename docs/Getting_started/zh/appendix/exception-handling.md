# QuecPython异常处理流程

## 模组网络异常处理

使用QuecPython开发时，如遇到网络异常情况产生，如MQTT连接异常，request请求失败等

可以先检查SIM状态是否正常

```python
import sim
sim.getStatus()   # 返回1为SIM卡状态正常，具体状态枚举值参考API手册
```

如果SIM状态异常，请检查SIM卡是否插入或者状态是否正常，如果SIM卡插入但是未检测到，在模块可以正常开机并且可以正常串口通信的前提下，建议尝试以下排查操作：

1. 检查 SIM 卡有没有插反，市面上 SIM 卡座种类繁多，部分 SIM 卡座没有防呆标识，正反插都可以放置在卡座内。
2. 更换 SIM 卡，SIM 卡可能长期插拔使用过程中损坏。
3. 按压 SIM 卡座，防止 SIM 卡座弹片和 SIM 卡接触不良。
4. 把 SIM 卡电路部分电容和 ESD 器件全部去掉，防止焊接电容容值不对和 ESD 器件焊接导致模组 SIM 卡不识别，这两种类型器件模组识卡是不影响。如果器件是手动焊接的，尤其关注这两点。
5. 尤其注意部分客户是手动焊接，检查 SIM 卡座各个引脚焊接是否存在短路问题。
6. 检查 SIM 卡座封装设计，确保封装正确。
7. 发送 AT 指令：AT+QSIMDET=0,0  关闭 SIM 卡热插拔功能 ，模块重新开机尝试能否识别卡。主要由于 SIM 卡座结构可能与开启的热插拔识别电平不一致导致无法识卡。
8. 如以上方法无法解决SIM异常问题，可联系技术支持人员寻求技术支持

如果SIM卡状态正常，可以使用模组提供的 **checkNet - 网络检测** 库来检测网络状态

```
import checkNet
checkNet.waitNetworkReady(timeout)
```

等待模组网络就绪。该方法会依次检测SIM卡状态、模组网络注册状态和PDP Context激活状态；在设定的超时时间之内，如果检测到PDP Context激活成功，会立即返回，否则直到超时才会退出。

如果超时时间内一直无法成功注册网络，可检查一下SIM卡是否有欠费停机、模组天线是否插好、查询信号值等来确认原因。

## python代码报错处理流程

开发中遇到代码运行报错可根据代码报错类型来出处理，比如

```
ImportError: no module named "***"
```

ImportError为导入错误，一般是导入的库或者库文件不存在，根据后面错误提示内容也有可能是库文件代码中有语法错误等，根据错误提示信息处理即可

类如（举例常见的几种）

- TypeError：类型错误，**对象用来表示值的类型非预期类型时发生的错误**
- AttributeError：属性错误，**特性引用和赋值失败时会引发属性错误**
- NameError：**试图访问的变量名不存在**
- SyntaxError: invalid syntax，语法错，**错误使用标点符号**
- KeyError：**在读取字典中的key和value时，如果key不存在，就会触发KeyError错误**
- IndexError: list index out of range， **索引错误，列表索引超出了范围**
- IndentationError: expected an indented block，**代码缩进错误**

其他错误码参考标准python处理即可

如有错误码可参考 [QuecPython错误码汇总](error-code.md)

## 模组异常重启处理

代码运行过程中如遇到设备异常重启，可以通过API接口查询异常关机原因

```
from misc import Power
Power.powerDownReason()
```






