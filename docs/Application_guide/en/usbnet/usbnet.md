# 1. 简介

QuecPython提供了`USBNET`功能模块来为用户提供USB网卡功能。该功能模块使得用户只需调用几个接口即可开启USBNET功能，提高了开发效率。

目前支持USBNET功能的模组系列：EC600S/EC600N/EC800N/EC200U/EC600U/EC600M。

> 本文档中示例代码前面有 `>>> `字符串的，表示在QuecPython的命令交互界面输入的代码。



# 2. 使用说明

`USBNET`模块接口的详细说明，请参考QuecPython官网的Wiki文档中相关部分的说明。下面将说明如何使用`USBNET`模块的相关功能。

## 2.1 USB网卡相关设置

下面将详细描述使用USBNET模块接口的步骤，同时说明在使用过程中一些注意事项。

### 2.1.1 使用步骤

步骤1：从misc中导入USBNET包

```python
>>> from misc import USBNET
```


步骤2：获取USB网卡工作模式

对于一块全新的模组，使用USBNET功能之前要先获取其工作模式，确认是用户想要使用的模式。

```python
>>> USBNET.get_worktype()
1
```



步骤3：设置USB网卡工作模式

用户需要调用如下接口，设置自己需要的网卡工作模式(以RNDIS模式为例)：

```python
>>> USBNET.set_worktype(USBNET.Type_RNDIS)
0
```


步骤4：重启模组

设置完USB网卡工作模式，需要重启模组使其生效：

```python
>>> from misc import Power
>>> Power.powerRestart()
```



步骤5：打开USBNET功能

重启后之前设置的工作模式已生效，直接打开USBNET即可：

```python
>>> from misc import USBNET
>>> USBNET.open()
```



### 2.1.2 示例代码

如下代码是一个完整的使用`USBNET`模块的例程：

```python

from misc import USBNET
from misc import Power

#work on ECM mode default
USBNET.open()

USBNET.set_worktype(USBNET.Type_RNDIS)

#reset the module
Power.powerRestart()

#after restart
from misc import USBNET

#work on RNDIS mode
USBNET.open()
```



## 2.2 NAT相关设置

`USBNET.set_worktype()`接口调用的时候会使对应的`nat`值变为`1`，使得该`pid`无法`IPV6`拨号，所以在`close USBnet`后，可以使用该接口关闭`NAT`，使`IPV6`功能正常。

> 目前仅EC200U/EC600U系列支持此功能

### 2.2.1 获取NAT使能情况

获取某一路网卡的NAT使能情况（是否支持ipv6拨号）。命令如下：

```python
USBNET.getNat(simid, pid)
```

参数说明：

- `imid` - 整型值，范围0/1，目前仅支持`0`。
- `pid` - 整型值，PDP索引，范围`1-7`。

返回值说明：

成功：返回NAT使能情况，整型0/1，`0`：使能，支持ipv6拨号；`1`：未使能，不支持ipv6拨号。
失败：返回整型`-1`。

### 2.2.2 NAT设置

NAT设置，设置成功后重启生效。命令为：

```python
USBNET.setNat(simid, pid, nat)
```

参数说明：

- `simid` - 整型值，范围0/1,目前仅支持0。
- `pid` - 整型值，PDP索引, 范围1-7。
- `Nat` - 整型值，范围：0/1,0：支持ipv6拨号；1：不支持ipv6拨号。

返回值说明：

`0`表示设置成功，`-1`表示设置失败。

```python
USBNET.setNat(0, 1, 0)
0
```



