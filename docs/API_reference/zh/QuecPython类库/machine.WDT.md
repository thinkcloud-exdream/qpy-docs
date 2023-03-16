# class WDT – 看门狗定时器

模块功能：APP应用程序发生异常不执行时进行系统重启操作

## 构造函数

### `machine.WDT`

```python
class machine.WDT(period)
```

创建软狗对象。

**参数：**

- `period` - 设置软狗检测时间，单位(s），int类型。

**返回值：**

返回软狗对象

## 方法

### `wdt.feed`

```python
wdt.feed()
```

该方法用于喂狗。

**返回值：**

成功返回整型值`0`，失败返回其他

### `wdt.stop`

```python
wdt.stop()
```

该方法用于关闭软狗功能。

**返回值：**

成功返回整型值`0`，失败返回其他。

**使用示例：**

```python
'''
@Author: Pawn
@Date: 2020-08-12
@LastEditTime: 2020-08-12 17:06:08
@Description: example for module timer
@FilePath: example_wdt.py
'''

from machine import WDT
from machine import Timer
import utime


'''
下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值
'''
PROJECT_NAME = "QuecPython_WDT_example"
PROJECT_VERSION = "1.0.0"

timer1 = Timer(Timer.Timer1)

def feed(t):
    wdt.feed()


if __name__ == '__main__':
    wdt = WDT(20)  # 启动看门狗，间隔时长
    timer1.start(period=15000, mode=timer1.PERIODIC, callback=feed)  # 使用定时器喂狗

    # wdt.stop()

```
