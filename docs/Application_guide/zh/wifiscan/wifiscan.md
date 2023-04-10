# 1. 简介

QuecPython提供了`wifiScan`功能模块来扫描周边的WiFi热点信息，包括WiFi热点的MAC地址和RSSI信号强度。

> 本文档中示例代码前面有 `>>> `字符串的，表示在QuecPython的命令交互界面输入的代码。



# 2. 使用说明

`wifiScan`有同步扫描和异步扫描两种扫描方式。同步扫描是一直等待扫描结束才返回扫描结果，因此扫描接口会阻塞一段时间；而异步扫描则是将扫描结果通过回调来返回给用户，因此扫描接口本身并不会阻塞。具体使用哪一种扫描方式，取决于用户的实际需求。下面分别说明这两种扫描方式的用法。

## 2.1 同步扫描

如前述所，同步扫描接口会阻塞一段时间，具体阻塞时间的长短取决于扫描配置参数，因此并没有一个固定的时间值。如果用户允许相关线程中使用阻塞性质接口，则可按照如下步骤来使用`wifiScan`的同步扫描功能。

### 2.1.1 使用步骤

步骤1：确认状态

先通过如下接口获取`wifiScan`的状态，确认是否已开启。返回值为`True`表示功能已开启，为`False`表示功能未开启。

```python
>>> wifiScan.getState()
False
```

步骤2：打开`wifiScan`功能

如果`wifiScan.getState()`返回`False`，则使用如下接口来开启`wifiScan`功能。

```python
>>> wifiScan.control(1)
0
```

步骤3：扫描参数设置

`wifiScan`模块提供了配置接口来设置扫描的相关参数，比如超时时间、扫描轮数、最大扫描热点数量以及扫描优先级。用户可根据需要来设置对应参数。这里设置超时时间为10s、扫描1次、最大扫描数量20个。由于优先级参数是可选参数，对于不支持的模组，我们可以不写该参数。

```python
>>> wifiScan.getCfgParam()
(5, 1, 10, 0)
>>> wifiScan.setCfgParam(10, 1, 20)
0
>>> wifiScan.getCfgParam()
(10, 1, 20, 0)
```



> * 并不是所有的模组都支持优先级参数，上述示例是基于EC600U系列模组，不支持优先级参数，因此没有配置。不支持优先级参数的模组有：EC200U/EC600U/EG912U/EG915U/EC600G/EC800G系列。
>
> * 设置的扫描参数掉电不保存。



步骤4：开始扫描

```python
>>> wifiScan.start()
(8, [('34:CE:00:09:E5:A8', -38), ('50:D2:F5:B4:70:BF', -40), ('00:60:92:57:0A:F4', -47), ('00:03:7F:12:06:06', -53), ('F0:2F:74:2A:41:78', -54), ('00:03:7F:12:15:15', -68), ('08:4F:0A:05:22:8B', -73), ('08:4F:0A:05:22:8F', -76)])
```



### 2.1.2 示例代码

```python
"""
本例程示范了如何使用wifiScan模块的同步扫描功能
"""
import utime
import wifiScan


def main():
    isOpen = wifiScan.getState()
    if not isOpen:
        ret = wifiScan.control(1)
        if ret == 0:
            print('wifi scan 打开成功')
        else:
            print('wifi scan 打开失败')
            return -1
    else:
        print('wifi scan 已经开启')

    ret = wifiScan.setCfgParam(5, 1, 20, 0)
    if ret == 0:
        print('扫描参数设置成功')
    else:
        print('扫描参数配置出错')
        return -1
    curCfg = wifiScan.getCfgParam()
    if curCfg != -1:
        print('当前扫描参数为：')
        print('超时时间：{}'.format(curCfg[0]))
        print('扫描轮数：{}'.format(curCfg[1]))
        print('最大扫描数量：{}'.format(curCfg[2]))
    else:
        print('获取扫描配置出错')
        return -1
    count = 0
    while True:
        count += 1
        scanInfo = wifiScan.start()
        if scanInfo != -1:
            scanNums = scanInfo[0]
            wifiInfo = scanInfo[1]
            print('扫描到{}个热点：'.format(scanNums))
            for i in wifiInfo:
                print(i)
            utime.sleep(2)
            if count >= 3:
                break
        else:
            print('扫描出错')
            return -1

    ret = wifiScan.control(0)
    if ret == 0:
        print('wifi scan 关闭成功')
        return 0
    else:
        print('wifi scan 关闭失败')
        return -1


if __name__ == '__main__':
    main()
    
```



## 2.2 异步扫描

异步扫描方式在使用上和同步扫描区别不大，大部分步骤和同步扫描一致。

### 2.2.1 使用步骤

步骤1：确认状态

步骤2：打开`wifiScan`功能

步骤3：扫描参数设置

步骤4：注册异步扫描回调函数

步骤5：开始扫描



### 2.2.2 示例代码

关于如下例程有两点需要说明：

* 例程中，`wifiscanCallback`回调中使用消息队列将扫描数据发到`main`中显示处理了。这是因为，在回调中，尽量只做一些耗时短的操作，一些耗时较长、处理较为复杂的操作一般放到其他任务中进行处理，不一定是放到主任务`main`中处理，也可以是其他子任务中。

* 消息队列的`get`方法，在没有消息时，会一直阻塞。如果应用代码中某个线程中不能阻塞，则不应该在其中使用该方法。

```python
"""
本例程示范了如何使用wifiScan模块的异步扫描功能
"""
import utime
import wifiScan
from queue import Queue

msgq = Queue(5)


def wifiscanCallback(args):
    global msgq
    msgq.put(args)


def main():
    global msgq
    isOpen = wifiScan.getState()
    if not isOpen:
        ret = wifiScan.control(1)
        if ret == 0:
            print('wifi scan 打开成功')
        else:
            print('wifi scan 打开失败')
            return -1
    else:
        print('wifi scan 已经开启')

    ret = wifiScan.setCfgParam(5, 1, 20, 0)
    if ret == 0:
        print('扫描参数设置成功')
    else:
        print('扫描参数配置出错')
        return -1
    curCfg = wifiScan.getCfgParam()
    if curCfg != -1:
        print('当前扫描参数为：')
        print('超时时间：{}'.format(curCfg[0]))
        print('扫描轮数：{}'.format(curCfg[1]))
        print('最大扫描数量：{}'.format(curCfg[2]))
    else:
        print('获取扫描配置出错')
        return -1
    # 注册回调函数
    wifiScan.setCallback(wifiscanCallback)

    count = 0
    while True:
        count += 1
        if wifiScan.asyncStart() == 0:
            scanInfo = msgq.get() # 没有消息时会阻塞在这里
            scanNums = scanInfo[0]
            wifiInfo = scanInfo[1]
            print('扫描到{}个热点：'.format(scanNums))
            for i in wifiInfo:
                print(i)
            utime.sleep(2)
            if count >= 3:
                break
        else:
            print('扫描出错')
            return -1

    ret = wifiScan.control(0)
    if ret == 0:
        print('wifi scan 关闭成功')
        return 0
    else:
        print('wifi scan 关闭失败')
        return -1


if __name__ == '__main__':
    main()

```

