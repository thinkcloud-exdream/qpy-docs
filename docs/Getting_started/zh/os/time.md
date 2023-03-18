# 时间功能

在使用 QuecPython 开发物联网应用程序时，时间功能对于一些用户来说是非常重要的一部分。本文将介绍如何在 QuecPython 中使用时间功能。

主要围绕以下几个功能展开介绍：

[ntptime - NTP 对时](../../../API_reference/zh/QuecPython组件库/ntptime.html)

[class RTC – 实时时钟](../../../API_reference/zh/QuecPython类库/machine.RTC.html)

[utime - 时间相关功能](../../../API_reference/zh/QuecPython标准库/utime.html)

[machine.Timer - 硬件定时器](../../../API_reference/zh/QuecPython类库/machine.Timer.html)

## 时间同步

在一些需要准确时间的应用中，可以通过与网络时间服务器进行同步来保证时间的准确性，虽然不主动对时我们也可以在模块联网的时候从网络获取到时间，但是这个时间出现过不准确的情况，所以建议先进行时间同步。在 QuecPython 中，可以使用 `ntptime` 模块与 NTP 服务器进行时间同步，但是此功能依赖于网络，在使用此功能前务必确保我们的网络已经正常，可以参见 [天线、SIM 卡和网络注册](./../iot-basic/preparation.html) 章节。并且确保您的卡没有被限制 ip 访问范围，如有限制需要联系运营商将 NTP 服务器加入白名单，或者自己实现对时功能确保时间能够被校准。

当前我们的 `ntptime` 模块默认支持五个常用服务器域名："ntp.aliyun.com", "pool.ntp.org", "asia.pool.ntp.org", "cn.ntp.org.cn", "cn.pool.ntp.org"，当其中任何一个异常时，都将自动切换下一个域名，如仍不能满足您的需求，您可以选择设置自己更为可靠的服务器。

```python
import utime
import ntptime

# 设置 NTP 服务器
ntptime.host = "pool.ntp.org"

# 同步时间（以同步东八区时间为例）
ntptime.settime(timezone=8)

# 获取同步后的时间戳
current_timestamp = utime.time()

# 将时间戳转换为本地时间
local_time = utime.localtime(current_timestamp)

# 打印本地时间
print(local_time)
```

在上面的代码中，`ntptime.host` 变量设置了 NTP 服务器的地址，`ntptime.settime()` 函数与 NTP 服务器进行时间同步，`utime.time()` 函数获取同步后的时间戳。

<font color="red"> 需要注意的是，并不能过于频繁的进行 NTP 对时，下面的文章将会继续介绍原因。</font>

## 获取当前时间

获取当前时间是最基本的时间操作。在 QuecPython 中，可以使用 `utime` 模块获取当前时间上一部分也有实际用到，但是实际上可以更简单，并且 `utime` 模块还有其他更加实用的时间功能，具体查看 API 介绍，这里介绍用的较多的。

```python
import utime

# 直接获取本地时间
local_time = utime.localtime()

# 打印本地时间
print(local_time)

# 设置时区，不建议使用，建议使用 ntptime
utime.setTimeZone(offset)

# 休眠即延时
utime.sleep(1)
utime.sleep_ms(1)
utime.sleep_us(1)
```

在上面的代码中，`utime.localtime()` 函数可以直接获取本地时间，十分方便，但是前提是 RTC 时间已经是正确的，因为这里的时间实际来源于 RTC 时间，关于 RTC 的介绍详见下文。

`utime` 模块中的设置时区实际并不好用，不如使用 ntptime 对时的同时设置时区。

`utime` 模块中的 sleep 延时功能有着很多的用处，同时也有一些使用建议。

1. 首先从其字面含义来说，在我们想让模块处于睡眠状态时（依赖其他前提条件，详见 [低功耗](./../hardware-advanced/pm.html) 章节），需要正在执行这个函数。

2. 之所以调用这个函数时模块可以处于睡眠，是因为调用这个函数时，模块主动让出了 CPU 执行权限，基于这个特性，当我们在使用多线程时每个死循环里也必须使用这个函数，来主动让出 CPU 执行权限，使得各个线程均能够正常得到调度，sleep 时间无特殊要求，详见 [多线程](./threads.html) 章节。

3. 使用 sleep 函数来进行软件延时。需要注意 sleep 的软件延时并不精准，无法作为高精度延时来使用，并且虽然具有 sleep_us 这个函数，但是并不能进行微秒级的延时，延时的最小时间需要实测确认。

4.`utime.sleep`、`utime.sleep_ms` 及 `utime.sleep_us` 函数的调用会导致程序休眠阻塞。

`utime` 模块除了这些功能，还有一个比较实用的功能，可以测量两段脚本之间的执行时间，详见 API 介绍文档，不过多赘述。

## RTC 实时时钟

RTC(Real Time Clock) 实时时钟是一种硬件设备，它可以提供独立于操作系统的时间计时服务，即使设备关机（不断电）也能保持时间的准确性。在 QuecPython 中，可以使用 `machine` 模块访问 RTC 实时时钟。对于 RTC 的所有用法参见 [class RTC – 实时时钟](../../../API_reference/zh/QuecPython类库/machine.RTC.html) 章节，下面主要介绍常用操作与注意事项。

```python
from machine import RTC

# 初始化 RTC 实时时钟
rtc = RTC()

# 设置 RTC 时间
rtc.datetime([2020, 3, 12, 1, 12, 12, 12, 0])

# 获取 RTC 时间
rtc_time = rtc.datetime()

# 打印 RTC 时间
print(rtc_time)
```

在上面的代码中，主要介绍了如何使用 RTC 获取和设置模块的时间，至此，我们可以知道，虽然 `utime` 和 `RTC` 都能够获取时间，但是只有 `RTC` 是能够设置时间的，所以 `utime` 的时间也是来源于 `RTC` 设置的时间，整个系统中的时间，除了从网络中获取的，其余均来自于 `RTC`，网络中同步的时间，如基站提供的时间、NTP 服务器提供的时间则是通过 `RTC` 来设置到系统中的。

上面提到不能频繁进行 NTP 对时的原因也在这里，因为 RTC 每设置一次时间都会擦写模块内部的 flash，会导致 flash 的寿命减少，flash 的擦写次数上限一般为 10 万次。

`RTC` 模块中还有一个函数对于部分场景比较实用，`rtc.set_alarm`，具体用法和适用的模块详见对应的 API 介绍文档，这个函数同样会擦写 flash，不宜频繁调用。其实用性主要体现在，部分型号可以在关机后由 `RTC` 唤醒开机，而开机时间就是由这个函数进行设置的，这个功能可以应用于对功耗要求较高的场景，除此之外还可以对一般的低功耗模式进行唤醒，详见 [低功耗](./../hardware-advanced/pm.html)。

## 综合示例代码

以下是一个完整的示例代码，该代码实现了获取当前时间、RTC 时间、时间同步、时间格式化、时间延时等功能。

```python
import utime
import machine
import ntptime

# 同步东八区时间
ntptime.host = "pool.ntp.org"
ntptime.settime(timezone=8)
current_timestamp = utime.localtime()
print("Synchronized time:", current_timestamp)

# 获取 RTC 时间
rtc = machine.RTC()
rtc_time = rtc.datetime()
print("RTC time:", rtc_time)

# 获取当前时间
current_timestamp = utime.localtime()
print("Current timestamp:", current_timestamp)

# 延时
utime.sleep(1)
print("Delay 1 second.")
utime.sleep_ms(500)
print("Delay 500ms.")
```

## 总结

用户经常关注的时间相关的功能应用均在此做了介绍，如有疑问或更好的建议欢迎联系我们，也可以直接向我们提交文档贡献，后续本文将继续完善和补充。
