```
本文阐述了QuecPython的misc模块的用法，描述了misc模块最新版本的特性。
```



# misc- 其他

模块功能:  提供关机、软件重启、PWM以及ADC相关功能。

## 分集天线配置接口功能

### `misc.antennaSecRXOffCtrl`

```python
misc.antennaSecRXOffCtrl(*args)
```

分集天线配置、查询接口。（仅1803S平台支持该接口）。

**参数描述：**

该接口为可变参形式：
  参数个数为0，查询：misc.antennaSecRXOffCtrl()；
  参数个数为1，配置：misc.antennaSecRXOffCtrl(SecRXOff_set)。

- SecRXOff_set-int类型，范围0/1, `0`:不关闭分集天线 `1`:关闭分集天线。

**返回值描述：**

查询：成功返回分集天线配置，失败返回整形值`-1`；

设置：成功返回整形0,失败返回整型值`-1`。

**示例：**

```python
import misc

misc.antennaSecRXOffCtrl()
0
misc.antennaSecRXOffCtrl(1)
0
misc.antennaSecRXOffCtrl()
1
```

## Classes

- [class PowerKey – PowerKey按键回调注册](./misc.PowerKey.md)
- [class PWM – 脉宽调制](./misc.PWM.md)
- [class ADC - 模数转换](./misc.ADC.md)
- [class USB– USB插拔检测](./misc.USB.md)

## Submodules

- [module Power – 关机以及软件重启](./misc.Power.md)

- [module USBNET – USB网卡](./misc.USBNET.md)