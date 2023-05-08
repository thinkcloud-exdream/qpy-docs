# eSIM LPA

## 什么是eSIM LPA

eSIM即嵌入式SIM，也叫eUICC，支持空中写号，可远程动态切换码号；它是SIM卡技术的升级，是由GSMA开发的一个新标准。
与传统可插拔的SIM卡不同，eSIM一般没有实体SIM卡，而是通过一个嵌入到设备中的芯片（eUICC），下载运营商配置文件并激活运营商服务。详细点说，eSIM是通过使用远程SIM卡配置来激活的，即通过使用远程SIM卡配置平台，通过使用标准化、安全和远程的“空中传送”过程，来完成eSIM配置文件的下载、安装和激活。
eSIM这种虚拟化和设备集成化的特性，让用户不必来回插拔传统SIM卡，SIM卡号码的切换也将引来全新的用户体验，用户直接通过与终端交互，通过APP或者云端，即可在全球范围内将终端智能设备连接到所选择的当地网络，且可动态切换，使设备可以始终处于优质网速中。

对于终端用户而言，Quecpython eSIM方案整体架构可以理解为由DP+服务器，设备提供的LPA以及eSIM组成，我们UE在此充当的就是LPA的功能。

## 怎么使用eSIM

### 硬件设计

eSIM功能主要为DP+服务器与eSIM通过UE来进行的内部交互，除前提条件模块需要组网成功外无需其他外围硬件支持。

### 软件应用

目前GSMA制定了两套eSIM标准方案，分别是针对物联网行业的M2M方案——M2M eSIM；以及直接面向最终用户的消费者解决方案——Consumer eSIM。
M2M方案需要依赖短信功能进行profile的下载，而消费者解决方案依赖于HTTPS下载。故M2M方案的实施eSIM芯片中必须预置有种子号；消费者解决方案的实施只需要设备能连接网络即可，但目前QuecPython支持的模组型号只能通过蜂窝数据连接网络，所以使用消费者解决方案时也需要预置种子号保证能正常连接网络。

下面我们分：`eSIM空中写号流程`；`OTA`；`软件设计`三个部分来分别介绍Quecpython eSIM LPA方案。

#### eSIM空中写号流程

1、通常MCU/End user通过二维码获取activation code并提供给终端

2、模块使用esim中的种子号的网络与DP+服务器进行交互

3、从服务器下载profile到esim中（OTA）

#### OTA

1、ESIM和DP+服务器互相认证

2、从DP+ 服务器下载profile安装包

3、安装profile到eSIM并上报结果给DP+ 服务器

#### 软件设计

注意：执行该脚本之前请关闭开机自动拨号逻辑

```Python
import utime
import net
import dataCall
import sim
from sim import esim
from machine import UART
from queue import Queue

OTAResult_q = None

def check_sim():
    repeat_count = 10
    while repeat_count >= 0:
        sim_state = sim.getStatus()
        if sim_state == 1:
            print('sim is ready!')
            break;
        else:
            utime.sleep_ms(500)
            repeat_count -= 1
            
    if repeat_count < 0:
        return -1
    #else:
        #return 0
        
    iccid = sim.getIccid()
    print('iccid:{}'.format(iccid))
    
    eid = esim.getEid()
    print("eUICC id:{}".format(eid))
    if eid == '' or eid == None:
        print('get euicc id failed!')
        return -1
        
    profile_list = esim.getProfileInfo(1)
    print(profile_list)
    if profile_list[0] == 0:
        print('there is no profileinfo in this esim!')
        return -1
    return 0
	
def init_esim():
    #
    print('Please input the ipVersion of this esim:')
    ipVersion=input()
    print('Please input the APN of this esim:')
    apn=input()
    print('Please input the userName of this esim:')
    userName=input()
    print('Please input the passWord of this esim:')
    passWord=input()
    print('Please input the authType of this esim:')
    authType=input()
    net.setApn(1,int(ipVersion),apn,userName,passWord,int(authType),0)
    #
    print('Please input the net config:')
    config=input()
    net.setConfig(int(config))
    #
    net.setModemFun(0)
    repeat_count = 5
	while repeat_count >= 0:
        net_state = net.getState() #([11, 26909, 232301323, 7, 0, 466], [0, 26909, 232301323, 7, 0, 0])
        if net_state == -1 or (net_state[1][0] != 1 and net_state[1][0] != 5):
            net.setModemFun(1)
            repeat_count = 1200
            while repeat_count >= 0:
                net_state = net.getState()
                if net_state[1][0] == 1 or net_state[1][0] == 5:
                    print('success to reg network...')
                    break;
                else:
                    utime.sleep_ms(500)
                    repeat_count -= 1
                    print('wait reg network...')
                    
            if repeat_count >= 0:
                return 0
            else:
                print('failed to reg network,please check pdn info and netconfig!')
                return -1
        else:
            utime.sleep_ms(100)
            repeat_count -= 1
            if repeat_count < 0:
                return -1
    return 0
	
def cb(args):
    global OTAResult_q
    print('OTA result:{}'.format(args))
    OTAResult_q.put(args)

def esim_lpa():
    global OTAResult_q
    esim.setCallback(cb)
    print('please input the activationCode:')
    activationCode = input()
    print('please input the confirmationCode:')
    confirmationCode = input()
    ret = esim.profileOTA(activationCode, confirmationCode)
    if ret == 0:
        result = OTAResult_q.get()
        if result == 0:
            print('success to download and install the profile!')
            while True:
                print('Please select the action you want<0:enable profile 1:exit>')
                handlerType = input()
                if int(handlerType) == 1:
                    return 0
                elif int(handlerType) == 0:
                    print('please input the iccid:')
                    iccid = input()
                    ret = esim.profileHandle(int(handlerType), iccid)
                    if ret != 0:
                        print('enable profile failed!')
                        return -1
                    print('enable profile succeed!')
                    sim_state = sim.getStatus()
                    print('sim state:{}'.format(sim_state))
                    iccid = sim.getIccid()
                    print('iccid:{}'.format(iccid))
                    profile_list = esim.getProfileInfo(1)
                    print('profile_list:{}'.format(profile_list))
                    break
                else:
                    print('invalid input')
                    utime.sleep_ms(100)
        else:
            print('failed to download and install the profile!')
            return -1
    else:
        print('failed to download and install the profile!')
        return -1

if __name__ == '__main__':
    OTAResult_q = Queue(maxsize=100)
    ret = check_sim()
    if ret == 0:
        ret = init_esim()
        if ret == 0:
            pdninfo = net.getApn(1,0)
            print(pdninfo)
            dataCall.setAsynMode(0)
            ret = dataCall.start(1,int(pdninfo[0]), pdninfo[1], pdninfo[2], pdninfo[3], int(pdninfo[4]))
            if ret == 0:
                esim_lpa()
```

## eSIM OTA测试

成功执行以上脚本之后，默认已经成功从DP+服务器下载并安装profile到eSIM中，并且使能了该profile，如果该profile是可用的，我们可以重启模块，查询当前注网状态，以及iccid，验证是否写号成功
