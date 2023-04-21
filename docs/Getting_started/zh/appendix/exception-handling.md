
## QuecPython异常处理流程

### 异常重启处理

固件版本默认是业务模式，即出现底层异常错误时会自动重启，防止模块程序停止导致无法使用。当我们处于调试期时需要暴露并定位问题原因，此时需要设置三条AT指令（AT口执行）：

- at+qdumpcfg=0,0
- at+qdumpcfg=1,0
- at+log=19,1

依次执行上述三条AT指令即可进入调试模式，此时若出现底层异常错误则会进入DUMP模式，出现DUMP端口，此时您可以有两种选择：

**方法一**：提供固件版本、测试步骤及测试代码，前往QuecPython官网提交问题工单
**方法二**：使用Tera term窗口调试工具（使用方法：百度即可）抓取Dumplog，同时提供固件版本、测试步骤及测试代码，前往QuecPython官网提交问题工单，节省复现问题时间。

**需要注意此指令重启后仍然生效，如需退出调试模式，有以下三种方法。**
1、用AT指令直接关闭
2、AT+RSTSET恢复出厂设置
3、更改固件烧录时擦除nvm

## QuecPython开关机reason含义和使用

### 寄存器含义

#### power_up_reason

对应寄存器：NINGBO_PWRUP_LOG_REG
各bit的含义：

| 0x01即bit0 | onkey硬件唤醒   |
| ---------- | :-------------- |
| 0x02即bit1 | exton1硬件唤醒  |
| 0x04即bit2 | exton2硬件唤醒  |
| 0x08即bit3 | bat硬件唤醒     |
| 0x10即bit4 | rtc_alarm唤醒   |
| 0x20即bit5 | fault唤醒       |
| 0x40即bit6 | vbus_detect唤醒 |

>
> 目前使用的有：exton1硬件唤醒(powerkey硬件接的是exton1)，fault唤醒，vbus_detect唤醒。

#### power_down_reason

对应寄存器：NINGBO_POWERDOWN_LOG_REG
各bit的含义：

| 0x01即bit0 | over temperature关机               |
| ---------- | :--------------------------------- |
| 0x02即bit1 | PMIC VINLDO电压低于2.9V关机        |
| 0x04即bit2 | SW_PDOWN软件调用power_down接口关机 |
| 0x08即bit3 | 无                                 |
| 0x10即bit4 | PMIC watch dog关机                 |
| 0x20即bit5 | long press of ONKEY关机            |
| 0x40即bit6 | VINLDO电压过高关机                 |
| 0x80即bit7 | VRTC LOW关机                       |

>
> 目前long press of ONKEY关机不使用。

#### power_down_reason2

目前只关注power_down_reason寄存器，该寄存器不需要使用。

### 开机原因

#### 开关机过程

**1.长按powerkey关机**
检测到长按动作，最终调用PMIC_SW_PDOWN

**2.硬件RESET**
调用CPU RESET引脚，PMIC不掉电， PWRUP_LOG_REG和POWERDOWN_LOG_REG寄存器也不会更新

**3.软件RESET**
a.若是调用PMIC_SW_RESET先使能FAULT_WAKEUP，再调SW_PDOWN，然后会FAULT唤醒重启。
b.若是异常重启类似硬件RESET，只是CPU RESET，PMIC不掉电。

**4.按 powerkey开机**
为exton1硬件唤醒

**5.插USB开机**
为vbus_detect唤醒

#### 开机原因获取

*每次开机读取过power_down_reason之后，会将其标志清掉，power_up_reason不支持清除。*

**1.powerkey**
需满足power_up_reason==0x02，且power_down_reason!=0

**2.硬件、异常RESET**
由于PMIC不掉电， PWRUP_LOG_REG寄存器不会更新，POWERDOWN_LOG_REG寄存器被清掉，则需满足power_up_reason==0x02，且power_down_reason==0。或满足power_up_reason==0x40， 且power_down_reason==0。

**3.软件RESET**
如果是插着USB则需满足power_up_reason==0x60，且power_down_reason==0x04。

**4.Vbus**
需满足power_up_reason==0x40，且power_down_reason!=0x00。

**5.其他开机原因在前面这些原因之后按bit含义获取。**

### 关机原因

关机原因如代码中按照bit含义获取即可。

### 开关机原因接口使用

目前boot侧和kernel侧都会提供开关机原因接口，由于获取开关机原因之后需要将POWERDOWN_LOG_REG寄存器中的关机原因标志清除，所以在boot侧调用过该接口的话，在kernel侧就不能调了，否则获取的值会有异常。现在boot侧的接口默认没调用。
