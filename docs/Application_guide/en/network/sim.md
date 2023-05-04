# SIM卡

## 什么是SIM卡

Subscriber Identity Module（简称SIM卡）是一种智能卡，主要用于存储移动用户的身份信息和相关密钥，并实现对移动通信网络的认证和授权。SIM卡通常由芯片、封装材料和金属接点等组成，可以插入手机或其他移动终端中使用。 SIM卡的主要功能是存储移动用户的身份信息和相关密钥，包括手机号码、用户身份标识、IMSI号码、PIN码、PUK码、加密密钥等。通过这些信息，SIM卡可以向移动通信网络提供用户身份认证和授权，以保证通信网络的安全性。 此外，SIM卡还可以存储联系人信息、短信、通话记录、语音信箱号码、网络参数等相关信息，为用户提供各种通信和管理功能，方便用户的日常生活和工作。 

本文档主要介绍如何使用 QuecPython SIM卡功能，通过本文你将了解到 QuecPython SIM卡的设置及使用方法。

## 怎么使用SIM卡功能

### 硬件设计

SIM卡功能主要是实体SIM卡通过UE来进行交互，除前提条件模块需要组网成功外无需其他外围硬件支持。

### 软件应用

#### 已实现功能

SIM卡是具有以下功能和应用：

1. 身份认证：SIM卡中存储了用户的身份信息和网络访问权限，可以对用户进行身份认证和授权，以保证通信网络的安全性。
2. 存储联系人：SIM卡可以存储联系人信息，包括姓名、电话号码等，方便用户进行通信和联系。
3. 短信功能：SIM卡可以接收和发送短信，方便用户进行信息交流和通信。
4. 存储通话记录：SIM卡可以存储用户的通话记录，包括通话时间、通话时长等，方便用户进行通话管理和统计。
5. 存储语音信箱号码：SIM卡可以存储语音信箱号码，方便用户使用语音信箱服务。
6. 存储网络参数：SIM卡可以存储网络参数，包括APN、用户名、密码等，方便用户进行数据拨号和网络连接。
7. 存储安全信息：SIM卡可以存储加密密钥、PIN码等安全信息，以保证通信网络的安全性。

在QuecPython中这些功能的接口主要在[sim](/../../../API_reference/zh/QuecPython类库/sim.html)，[sms](/../../../API_reference/zh/QuecPython类库/sms.html)和[ voiceCall](/../../../API_reference/zh/QuecPython类库/ voiceCall.html)中。

      	1. SIM卡信息和状态查询：包括获取sim卡的IMSI，ICCID，电话号码和SIM当前状态。
      	2. 电话簿功能：可以存储联系人信息，包括姓名、电话号码等。
      	3. 短信功能：具体见[sms](./sms.md)短信应用指导。
      	4. 电话功能：具体见[ voiceCall](./sms.md)电话应用指导。
      	5. 存储安全信息功能：包括PIN码验证，解锁等。
      	6. 其它功能：如切卡、热插拔和注册回调功能。

#### 软件实现示例

```python
>>> import sim
>>> sim.getImsi()   # 获取sim卡的IMSI
'460105466870381'
>>> sim.getIccid()   # 获取sim卡的ICCID
'89860390845513443049' 
>>> sim.getPhoneNumber()    # 获取sim卡的电话号码
'+8618166328752'
>>> sim.getStatus()    # 查询当前SIM卡状态  0：SIM卡不存在/被移除，1：SIM已经准备好，2：SIM卡已锁定
1             
>>> sim.writePhonebook(9, 1, 'Tom', '18144786859')   # 写电话簿
0
>>> sim.readPhonebook(9, 1, 4, "")    # 读电话簿
(4,[(1,'Tom','15544272539'),(2,'Pony','15544272539'),(3,'Jay','18144786859'),(4,'Pondy','15544282538')])
>>> sim.readPhonebook(9, 0, 0, "Tom")
(1, [(1, 'Tom', '18144786859')])
>>> sim.readPhonebook(9, 0, 0, "Pony")
(1, [(2, 'Pony', '17744444444')])
>>> sim.readPhonebook(9, 0, 0, "Pon")   # 关键字查询电话簿
(2, [(2, 'Pony', '17744444444'),(4,'Pondy','15544282538')])
>>> sim.enablePin("1234")    # 开启PIN码验证
0
>>> sim.verifyPin("1234")    # PIN码验证
0
>>> sim.disablePin("1234")    # 取消PIN码验证。
0
>>> sim.changePin("1234", "4321")  # 于更改sim卡PIN码。  
0
>>> sim.unblockPin("12345678", "0000")  # SIM卡解锁：当多次输入PIN码错误需要用PUK码解锁
0
>>> sim.setSimDet(1, 0)  # 开启SIM卡热插拔， 1表示开启
0
>>> sim.getSimDet()  # 查询热插拔相关配置
(1, 0)
>>> sim.getCurSimid()  # 获取当前卡，当前是卡1
0
>>> sim.switchCard(1)  # 切到卡2
0
>>> sim.getCurSimid()  # 获取当前卡，成功切到卡2
1
# 热插拔 注册监听回调函数
def usrCallback(args):
    simstates = args
    print('sim states:{}'.format(simstates))
sim.setCallback(usrCallback)

# SIM卡切卡状态 注册监听回调函数
def usrCallback(args):
    switchcard_state = args
    print('sim switchcard states:{}'.format(switchcard_state))
sim.setSwitchcardCallback(usrCallback)
```

