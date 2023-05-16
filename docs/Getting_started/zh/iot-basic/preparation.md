# 天线、SIM 卡和网络注册

## 天线简介

天线是一种变换器，它把传输线上传播的导行波，变换成在无界媒介（通常是自由空间）中传播的电磁波，或者进行相反的变换。在无线电设备中用来发射或接收电磁波的部件。无线电通信、广播、电视、雷达、导航、电子对抗、遥感、射电天文等工程系统，凡是利用电磁波来传递信息的，都依靠天线来进行工作。此外，在用电磁波传送能量方面，非信号的能量辐射也需要天线。一般天线都具有可逆性，即同一副天线既可用作发射天线，也可用作接收天线。

简单来说天线是一种用于发送或接收电波的设备，它可以把电器信号转换为无线电波，同时也可以将无线电波转换成电器信号。

QuecPython模块通常使用不同类型的天线以支持其无线通信功能，以下是QuecPython模块中常见的几种天线：

1. GPS天线：QuecPython模块通常配备GPS天线，以支持全球定位系统（GPS）功能。该天线通常是带有SMA线性（LNA）增益放大器或充电帽的陶瓷贴片天线。由于其较小的尺寸，通常可以安装在设备的外壳或露出在外。

2. GSM天线：GSM天线是用于支持2G / 3G无线通信的天线。它们通常是单向天线，可用于发送和接收来自GSM基站的广播，以便将设备连接到移动网络。它们通常是双频（850MHz和1900MHz）带（GSM800 / 1900）。

3. 4G / LTE天线：Quectel模块还可以配备4G / LTE天线，以支持高速无线通信。这些天线通常是单向天线，其工作频段通常包括多个LTE频段，用于覆盖不同的地理区域和服务商。

4. WIFI / Bluetooth天线：这些天线通常用于支持设备之间的无线通信，例如蓝牙和Wi-Fi。它们可以是内置式PCB天线或外置式“小螺旋天线”，为移动设备提供更好的无线连接范围和信号强度。

天线是QuecPython模块无线通信功能的重要组成部分，它们的选择和设计对于设备的无线通信性能和工作效率都具有重要的影响。因此，在进行设备设计和开发时，需要根据应用需求和实际情况，选择和配置合适的天线。

所以在使用QuecPython模块前请检查天线是否正常。

## SIM卡

### SIM卡基本概述

Subscriber Identity Module（简称SIM卡）是一种智能卡，主要用于存储移动用户的身份信息和相关密钥，并实现对移动通信网络的认证和授权。SIM卡通常由芯片、封装材料和金属接点等组成，可以插入手机或其他移动终端中使用。 SIM卡的主要功能是存储移动用户的身份信息和相关密钥，包括手机号码、用户身份标识、IMSI号码、PIN码、PUK码、加密密钥等。通过这些信息，SIM卡可以向移动通信网络提供用户身份认证和授权，以保证通信网络的安全性。 此外，SIM卡还可以存储联系人信息、短信、通话记录、语音信箱号码、网络参数等相关信息，为用户提供各种通信和管理功能，方便用户的日常生活和工作。 

SIM 分为手机卡和物联网卡。区别就是物联网卡没有电话号码不能收发短信，手机可以发短信。 常见的是手机卡。

第二代标准的Mini卡，国内用户俗称的大卡。

第三代标准的Micro卡，俗称小卡。

第四代标准的Nano卡。

![iot-basic-sim-type](F:\teedoc_with_qpydoc\docs\Getting_started\zh\media\iot-basic\preparation\iot-basic-sim-type.png)

QuecPython模块需要的是第四代标准的 Nano 卡。 

### 常见SIM术语解释

#### IMSI 

IMSI全称为 Internation Mobile Subscriber Identity，即国际移动用户识别码。

-  前三位数字代表移动国家代码（MCC）。
-  接下来的两位或三位数字代表移动网络代码（MNC）。E.212允许使用三位数的MNC代码，但主要在美国和加拿大使用。
-  接下来的数字代表移动用户识别号（MSIN）。

####  ICCID

ICCID全称为Integrated Circuit Card Identifier，即集成电路卡识别码。

- 可以简单理解为SIM卡的卡号（身份证号）。

- 编码格式为：XXXXXX 0MFSS YYGXX XXXX。

- 前六位运营商代码：

  中国移动的为：898600；898602；898604；898607 ，

  中国联通的为：898601、898606、898609，

  中国电信898603、898611。

### 功能实现

QuecPython模块支持SIM卡相关功能实现，具体见`SIM`模块接口的详细说明，请参考QuecPython官网的Wiki文档中相关部分的说明。下面是简单介绍如何使用`SIM`模块的相关功能。

#### 交互实验

```python
>>> import sim
>>> sim.getImsi()   # 获取sim卡的IMSI
'460105466870381'
>>> sim.getIccid()   # 获取sim卡的ICCID
'89860390845513443049' 
>>> sim.getPhoneNumber()    # 获取sim卡的电话号码
'+8618166328752'

# 查询当前SIM卡状态  0：SIM卡不存在/被移除，1：SIM已经准备好，2：SIM卡已锁定
>>> sim.getStatus()   
1             
>>> sim.writePhonebook(9, 1, 'Tom', '18144786859')   # 写电话簿
0
>>> sim.readPhonebook(9, 1, 4, "")    # 读电话簿
(4,[(1,'Tom','15544272539'),(2,'Pony','15544272539'),(3,'Jay','18144786859'),(4,'Pondy','15544282538')])
```



## 网络注册

网络注册是指移动设备连接到移动网络时的过程。这个过程包括设备发出网络寻呼，网络返回网络确认响应，设备和网络进行通信等多个步骤。以下是常见的网络注册过程的步骤：

1. 扫描可用网络：在设备上电时，设备会扫描周围所有可用的无线网络。一般情况下，设备会首先尝试连接已经预先设置好的首选网络。

2. 发送注册请求：如果未能连接到已预设网络，设备会向每一个可用网络发送“注册请求”（Registration Request）以表示设备的存在，并和网络进行通信。

3. 接收注册回复：网络接收到设备的注册请求后，会对它进行确认响应。如果响应成功，将返回包括设备所需通信参数的注册成功信息（Registration Accept）。设备可以使用这些参数进行后续通信。

4. 检查网络质量：接收到注册回复后，设备会检查网络质量和信号强度，判断是否可以与该网络建立连接。

5. 建立连接：如果网络质量良好，设备会向网络发送连接请求（Attach Request），并请求分配网络地址。网络将响应连接请求并分配网络地址，设备和网络之间建立起连接。

以上是网络注册的主要步骤。当设备和网络之间建立了连接后，设备可以使用相应技术（如2G、3G、4G等）进行实时通信和数据传输。

#### 注网确认

我们可以通过QuecPython模块`net`模块接口查看网络注册状态，请参考QuecPython官网的Wiki文档中相关部分的说明。下面是简单介绍网络注册相关功能。

```python
>>> import net
>>> net.getState()   # 查看网络注册状态，具体结果含义间QuecPython官网的Wiki文档
([0, 0, 0, 0, 0, 0], [1, 21771, 254626386, 7, 0, 0]) 
# 第一个列表代表电话注册状态，0 代表电话注网失败
# 第二个列表代表网络注册状态，1 代表网络注册成功  

>>> net.csqQueryPoll()  # 查询当前网络信号强度
31

```

#### 注网失败排查

模组一直没有注网成功（net.getState查询网络注册状态不为1），这时请按如下步骤排查问题：

（1）首先确认天线是否正常的，是否和模块匹配；

（2）如果天线正常，确认SIM卡状态是正常的，通过 sim 模块的sim.getState()接口获取，为1说明正常；

（3）如果SIM卡状态正常，确认当前信号强度，通过net模块的net.csqQueryPoll()接口获取，如果信号强度比较弱，那么可能是因为当前信号强度较弱导致短时间内注网不成功，可以增加超时时间或者换个信号比较好的位置再尝试；

（4）如果SIM卡状态正常，信号强度也较好，请确认使用的SIM卡是否已经欠费或流量不足；

（5）如果SIM卡没有欠费也没有流量不足，请确认使用的是否是物联网卡，如果是，请确认该SIM卡是否存在机卡绑定的情况；

（6）如果按照前述步骤依然没有发现解决问题，请联系我们的FAE反馈问题；最好将相应SIM卡信息，比如哪个运营商的卡、什么类型的卡、卡的IMSI等信息也一并提供，必要时可以将SIM卡寄给我们来排查问题。



## 总结

在 QuecPython 中进行网络通信之前，需要网络注册完成，网络注册涉及到天线、SIM卡，以及可能会出现各种异常情况，这里提供简介和常见的异常情况及其处理方法，希望对您有所帮助。
