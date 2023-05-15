# APN与数据拨号

数据拨号是指通过调用通信模块的拨号接口，实现将嵌入式设备连接到互联网的过程。在进行数据拨号之前，需要先配置通信模块的网络参数，如APN、用户名、密码等，以便建立连接时使用。

## APN介绍

### 什么是APN

APN指一种网络接入技术，是终端入网时必须配置的一个参数，它决定了终端通过哪种接入方式来访问网络。

对于用户来说，可以访问的外部网络类型有很多，例如：[Internet](https://baike.baidu.com/item/Internet/272794)、[WAP网站](https://baike.baidu.com/item/WAP网站/3419865)、集团企业内部网络、行业内部专用网络。而不同的接入点所能访问的范围以及接入的方式是不同的，网络侧如何知道终端激活以后要访问哪个网络从而分配哪个网段的IP呢？这就要靠APN来区分了，即APN决定了用户的终端通过哪种接入方式来访问什么样的网络。

所有运营商都使用特定的APN（Access Point Name，接入点名称）。这通常是您的SIM卡预先配置的，但必要时，您需手动进行调整。

### APN的含义

APN决定了终端通过哪种接入方式来访问网络，用来标识[GPRS](https://baike.baidu.com/item/GPRS/107439)的业务种类。

APN分为两大类：

- [WAP](https://baike.baidu.com/item/WAP/207452)业务。
- [WAP](https://baike.baidu.com/item/WAP/207452)以外的服务，比如：连接因特网。

从运营商角度看，APN就是一个逻辑名字，APN一般都部署在GGSN设备上或者逻辑连接到GGSN上，用户使用GPRS上网时，都通过[GGSN](https://baike.baidu.com/item/GGSN/6041769)代理出去到外部网络，因此，APN设置、过滤、统计等，就成为一个对GPRS计费、GPRS资费有重要参考价值的参数之一（因为APN可以区分一个业务或者外部网络）。

APN的完整说明在3GPP规范中进行了详细定义。

### APN的构成

APN接入点名称由两部分组成：

- 网络标识符

- 运营商标识符

运营商标识符又由其他两个部分组成：  

- 移动网络代码（MNC）

- 移动国家代码（MCC）

### APN的类型

我们可以根据APN是连接到公共网络还是专用网络以及IP地址的分配方式来划分APN，有以下四种不同的类型：

- **公用的APN-**通常简称为“ APN”。使用公用APN连接到网关的设备会动态获得IP地址，以便大部分访问互联网；

- **具有静态IP的公用APN-**网关根据公共网络的可用IP池为设备分配静态IP地址；

- **专用APN-**这也被认为是“带有VPN的APN”。具有专用APN配置的设备可以通过网关连接到自己的内部网络；

- **具有静态IP的专用APN-**网关根据专用网络的可用IP池为设备分配静态IP地址。

当我们比较公用APN和专用APN时，我们可以看到后者甚至不需要互联网连接。专用APN永远不允许其访问公共互联网，而同时又保持其在蜂窝网络基础架构上，从而确保了安全的数据处理。

对于QuecPython，可使用SIM卡默认APN或者手动配置APN，也可以调用API函数配置APN，具体配置APN见下一章数据拨号。



## 数据拨号

本章主要描述QuecPython模块无线数据业务的建立过程，即数据拨号的过程。主要介绍了数据拨号功能的实际应用，包含开机自动拨号、拨号重连以及手动拨号的基础的用法和注意事项。同时介绍了拨号功能在常见场景中的使用。

### 设备检查

本章介绍的内容是基于Python SDK中包含的API来实现的，请参考QuecPython官网的Wiki文档中相关部分的说明。

拨号之前需做一系列基本检查，判断模块是否处于基本的正常工作状态，具体步骤如下：

1. 通过USB转串口线连接PC至模块的主串口或者USB端口。

2. 插入(U)SIM卡和天线，并上电。

3. 通过如下API函数，检查设备状态。

   a)   检测(U)SIM卡：sim.getStatus()

   b)   检测信号强度：net.getSignal()

   c)   检测模块注网：net.getState()

   d)   查询第一路拨号服务状态：dataCall.getInfo(1,0)

4. 使用QPYcom工具和模组进行交互，检查如下操作：

![network.dataCall-qpy](F:\teedoc_with_qpydoc\docs\Getting_started\zh\media\iot-basic\apn-datacall\network.dataCall-qpy.png)



### 开机自动拨号与重连

所谓开机自动拨号，是指模组上电运行时，自动进行拨号的行为，无需用户再去执行拨号。用户只需要在模组开机后确认已经拨号成功，即可开始正常使用网络功能。

自动重连功能是指，因网络异常、信号差等异常场景导致模组与网络断开连接，当异常场景恢复正常后，模组自动进行拨号重连的行为。

```python
# 根据profileID来设置对应那一路是否开机自动拨号。profileID为1的那一路初始默认使能开机自动拨号。
# 1.查询是否拨号成功。
import dataCall      
dataCall.getInfo(1,0)  #查看第一路是否拨号成功    
#返回结果 (1, 0, [1, 0, '10.146.83.168', '211.138.180.2', '211.138.180.3'])      
dataCall.getInfo(2,0)  #查看第二路是否拨号成功    
dataCall.getInfo(3,0)  #查看第三路是否拨号成功 

# 2.设置为自动拨号。
# 第一路默认为自动拨号  
dataCall.setAutoActivate(2, 1)  #设置第二路自动拨号      
dataCall.setAutoActivate(3, 1)  #设置第三路自动拨号 

# 3.取消自动拨号。
dataCall.setAutoActivate(1, 0)  #取消第一路自动拨号  
dataCall.setAutoActivate(2, 0)  #取消第二路自动拨号  
dataCall.setAutoActivate(3, 0)  #取消第三路自动拨号

# 根据profileID来设置对应那一路是否使能自动重连。profileID为1的那一路默认使能自动重连功能。
# 4.设置开启自动重连。
# 第一路默认开启自动重连  
dataCall.setAutoConnect(2, 1)   #开启二路为自动重连 
dataCall.setAutoConnect(3, 1)   #开启三路为自动重连

# 5.关闭自动重连，如用户关闭了自动重连功能，网络状态发生变化时，如网络断开等情况下，则需要用户进行手动拨号。
dataCall.setAutoConnect(1, 0)   #关闭第一路自动重连
dataCall.setAutoConnect(2, 0)   #关闭第二路自动重连
dataCall.setAutoConnect(3, 0)   #关闭第三路自动重连
```

注意事项

> 1. 第一路（profileID为1）初始默认开机自动拨号和自动重连。  
> 2. 拨号前请先通过  setPDPContext配置APN相关信息。  
> 3. 如没有配置对应profileID的APN相关信息，默认使用空字符串进行拨号。  
> 4. 当设置多路自动拨号时，会依照profileID从小到大依次进行拨号。 
> 5. 如全部取消自动拨号，则模组上电运行时不会进行拨号，需要进行手动拨号。  
> 6. 如用户关闭了自动重连功能，则在网路断开恢复时需要用户进行手动拨号。

### 手动拨号

拨号，指的是PDP Context的激活操作，激活成功后，核心网的PDN网关才会分配一个IP地址给模组。手动拨号是指用户自己使用拨号接口去进行拨号，手动拨号前需要先配置PDP Context相关信息（APN，用户名，密码以及鉴权参数等信息）。

#### 配置APN

配置APN相关信息，拨号时使用该方法配置的相关信息进行PDP Context激活。

```python
# 1.配置PDP Context信息。
import dataCall    
#配置第一路PDP Context相关信息    
dataCall.setPDPContext(1, 0, "3gnet", "", "", 0)     
#配置第二路PDP Context相关信息  
dataCall.setPDPContext(2, 0, "3gnet.mnc001.mcc460.gprs", "", "", 0)     
#配置第三路PDP Context相关信息  
dataCall.setPDPContext(3, 0, "3gnet.mnc001.mcc460.gprs", "", "", 0)  

# 2.查询PDP Context信息。
dataCall.getPDPContext(1)    #查询第一路PDP Context相关信息  
#返回结果 (0, '3gnet', '', '', 0)  
dataCall.getPDPContext(2)    #查询第一路PDP Context相关信息  
#返回结果 (0, '3gnet.mnc001.mcc460.gprs', '', '', 0)  
dataCall.getPDPContext(3)    #查询第一路PDP Context相关信息
```

#### 拨号实现

手动拨号，激活profileID指定的那一路PDP Context。

```Python
# 1.手动激活，进行拨号。
import dataCall  
# 激活之前，应先配置APN  
dataCall.setPDPContext(1, 0, '3gnet', '', '', 0)  # 这里配置第一路的APN  
dataCall.setPDPContext(2, 0, '3gnet', '', '', 0)  # 这里配置第二路的APN  
dataCall.setPDPContext(3, 0, '3gnet', '', '', 0)  # 这里配置第三路的APN  
dataCall.activate(1)   # 激活第一路  
dataCall.activate(2)   # 激活第二路  
dataCall.activate(3)   # 激活第三路 

# 2.去激活，取消拨号。
dataCall.deactivate(1)    # 去激活第一路  
dataCall.deactivate(2)    # 去激活第二路  
dataCall.deactivate(3)    # 去激活第三路 
```

注意事项

> 1. 模组会在开机时自动拨号，一般不需要用户执行激活操作。 
> 2. 如用户关闭了开机自动拨号功能，则需要用户调用此方法来进行手动拨号。  
> 3. 手动拨号之前，应该先配置对应profileID的APN相关信息。  
> 4. 如没有配置对应profileID的APN相关信息，默认使用空字符串进行拨号。

### 代码实验与注册回调函数

当网络状态发生变化时，如网络断开、拨号重连成功时，会触发注册的回调函数，告知用户网络状态。

```python
import dataCall
import net
import utime as time

def callback(args):  
    #回调函数
    if args[1] == 1:
        print("*** network %d connected! ***" % args[0])
    else:
        print("*** network %d not connected! ***" % args[1])
       
def set_datacall_apn():
    # 获取第一路的APN信息，确认当前使用的是否是用户指定的APN  
    pdpCtx = dataCall.getPDPContext(1)  
    if pdpCtx != -1:  
        if pdpCtx[1] != pdpConfig['apn']:  
            # 如果不是用户需要的APN，使用如下方式配置  
            ret = dataCall.setPDPContext(1, 0, "3gnet", '', 'password', 0)  
            if ret == 0:  
                print('APN 配置成功。')  
                # 重启后按照配置的信息进行拨号  
                Power.powerRestart()    
            else:  
                print('APN 配置失败。')  
        else:  
            print('APN 已经配置过了。')  
    else:  
        print('获取PDP Context失败。')  
        

def test_datacall_callback():
    # 注册回调中断,当注册了回调函数后，在网络断开、拨号重连成功时，会触发注册的回调函数的运行。
    ret = dataCall.setCallback(callback)
    if ret == 0x00:
        print("set Callback has success")
    net.setModemFun(4)  # 进入飞行模式
    time.sleep_ms(1000)
    net.setModemFun(1)  # 重新进入正常模式
    print("test_datacall_callback funcation has exited")

if __name__ == "__main__":
    set_datacall_apn()
    test_datacall_callback()
    
    
```

##  数据拨号在不同场景下的使用

###  场景一：第一次使用

第一次插入sim卡，之前没有配置过PDP Context相关信息，文件系统也没有保存过PDP Context相关信息。

模组烧录QuecPython的固件，开机后，默认会自动执行第一路拨号，使用默认APN进行拨号。可以直接查询拨号信息。

1. 拨号成功--能够查询到拨号信息

   对于大部分公网卡和可以连上公网的专网卡而言，一般利用核心网下发的APN，进行拨号，并保存在文件系统里面，可以通过dataCall.getPDPContext(1)查询PDP Context相关信息。

```python
import dataCall  
dataCall.getInfo(1, 0)     #查询拨号结果信息     
#返回结果 (1, 0, [1, 0, '10.91.44.177', '58.242.2.2', '218.104.78.2'])  
dataCall.getPDPContext(1)  #查询第一路PDP Context信息  
#返回结果 (0, '3gnet', '', '', 0) 
```

2. 拨号失败--查询不到拨号信息

对于少部分公网卡，不是所有核心网都支持不设置APN；大部分专网卡必须提前设置APN，导致拨号失败。需要进行正常单路拨号，见场景二。

```python
import dataCall  
dataCall.getInfo(1, 0)    #查询拨号结果信息     
#返回结果 (1, 0, [0, 0, '', '', ''])  
dataCall.getPDPContext(1)    #查询第一路PDP Context信息  
#返回结果 (0, '', '', '', 0) 
```

### 场景二：正常单路拨号

在场景一和场景三拨号失败或不使用默认APN拨号的情况下，使用用户自己配置对应运营商的APN信息的进行拨号。

示例一如下：

```python
import dataCall  
from misc import Power  
# 用户需要配置的APN信息，根据实际情况修改  
usrConfig = {'apn': '3gnet', 'username': '', 'password': ''}  
# 获取第一路的APN信息，确认当前使用的是否是用户指定的APN  
pdpCtx = dataCall.getPDPContext(1)  
if pdpCtx != -1:  
    if pdpCtx[1] != pdpConfig['apn']:  
        # 如果不是用户需要的APN，使用如下方式配置  
        ret = dataCall.setPDPContext(1, 0, usrConfig['apn'], usrConfig['username'], usrConfig['password'], 0)  
        if ret == 0:  
            print('APN 配置成功。')  
            # 重启后按照配置的信息进行拨号  
            Power.powerRestart()    
        else:  
            print('APN 配置失败。')  
    else:  
        print('APN 已经配置过了。')  
else:  
    print('获取PDP Context失败。')  

```

示例二 如下:

```python
>>> import dataCall 
>>> dataCall.getPDPContext(1)  #查询APN
(0, 'cmnet.mnc001.mcc460.gprs', '', '', 0)
 #设置成用户指定的APN
>>>  dataCall.setPDPContext(1, 0, '3gnet', '', '', 0) 
0
>>> dataCall.getPDPContext(1)  #查询是否配置成功
(0, '3gnet', '', '', 0)

>>> from misc import Power  
>>> Power.powerDown()   #重启
```

重启后：

1. 拨号成功--能够查询到正确的拨号信息

正常情况下使用正确的APN进行拨号，都能够拨号成功，并保存在文件系统里面，可以通过dataCall.getPDPContext(1)查询PDP Context相关信息。

```python
import dataCall  
dataCall.getInfo(1, 0)    #查询第一路拨号信息     
#返回结果 (1, 0, [1, 0, '10.91.44.177', '58.242.2.2', '218.104.78.2'])  
dataCall.getPDPContext(1)  
#返回结果(0, '3gnet', '', '', 0)  
```

2. 拨号失败--查询不到拨号信息

部分为APN配置错误造成的，如没有配置对应运营商的APN，配置错专网卡特有的APN。需要先确认APN的正确性。

部分为网络、SIM卡或模块自身问题造成的，如SIM卡欠费、限制，网络断开，信号质量差等其它原因，需要和运营商或研发人员确认。

### 场景三：中途换卡

非第一次插入卡，中途换卡(公网换公网、公网换专网、专网换专网，专网换公网)，因为之前卡拨号成功过，所以无论有没有配置过PDP Context，文件系统都保存过PDP Context相关信息。

如删除过文件系统的PDP Context相关信息，拨号场景见场景一。

开机后，默认会自动执行第一路拨号，使用文件系统中配置的APN进行拨号。可以直接查询拨号信息。

1. 拨号成功--能够查询到拨号信息

对于部分同运营商内换卡或部分公网换公网，APN信息是一样的能够拨号成功；

对于部分公网换公网或专网换公网，因为核心网支持APN纠错，能够拨号成功，但是不建议使用，不是所有核心网都支持这个纠错功能。

2. 拨号失败--查询不到拨号信息

对于中途换卡场景拨号失败情况基本上都是APN错误导致的，需要进行正常单路拨号，见场景二。

### 场景四：多路拨号

用户除了使用第一路数据拨号外还需要使用其它路进行数据拨号。

1. 由于除了第一路外，其他路没有自带自动拨号，自动重连功能，可以使用手动拨号。

```python
import dataCall  
#查询第二路拨号信息；由于没有拨号，返回空  
dataCall.getInfo(2, 0)     
#返回结果 (2, 0, [0, 0, '', '', ''])  
#设置第二路拨号的PDP Context相关信息，如不设置，拨号时使用空字符串进行拨号  
dataCall.setPDPContext(2, 0, '3gnet', '', '', 0)   
# 开启第二路开机自动拨号功能 
dataCall.setAutoActivate(2, 1)  
# 开启第二路自动重连功能  
dataCall.setAutoConnect(2, 1)   
#手动激活第二路PDP Context  
dataCall.activate(2)  
#返回结果 0 拨号成功  
dataCall.getInfo(2, 0)  #查询第二路拨号信息  
#返回结果 (2, 0, [1, 0, '10.91.44.177', '58.242.2.2', '218.104.78.2'])  
dataCall.getPDPContext(2)  
#返回结果(0, '3gwap', '', '', 0)  
```

2. 注意事项

   在配置其它路为自动拨号，自动重连后，拨号场景同场景一、场景二、场景三。

   多路手动拨号成功与失败原因，同场景一、场景二、场景三。

   如设置第一路为取消自动拨号，取消自动重连，同场景四。



## 总结

在数据拨号完成（dataCall.getInfo能够拿到ip）后，就可以进行正常的网络通信了。本文介绍了APN、数据拨号和常见使用场景，希望对您有所帮助。
