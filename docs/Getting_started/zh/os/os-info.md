# 系统信息

本文主要介绍如何使用 uos、usys、modem 等模块查询模组的固件信息、模组剩余内存大小等用户经常关注的信息，本文将不断补充，以方便用户了解模组的基本信息。

## 查询固件版本信息

```python
>>> import uos
# 查询QuecPython固件版本信息(QuecPython独有命名规则)
>>> uos.uname()
# 返回值(EC600U型号为例)
# ('sysname=EC600U-CNLB', 'nodename=EC600U', 'release=1.13.0', 'version=v1.12 on Sat_Nov_19_2022_5:29:48_PM', 'machine=EC600U with QUECTEL', 'qpyver=V0002')
```

如上所示我们可以查询到模组型号 machine = EC600U with QUECTEL，即 EC600U，但固件中对型号的区分是 sysname = EC600U-CNLB，即这个固件可以在 EC600UCNLB 这个子型号中使用，一般严格遵循字母数字一一对应原则，但是也有例外情况存在，固件具体适用的模组型号以下载区的固件描述和移远官方技术人员描述为准。还可以查询到固件的编译日期和 microPython 版本 version = v1.12 on Sat_Nov_19_2022_5: 29: 48_PM，一般用于判断 BETA 版本(仅用于测试严禁量产的版本)新旧，由于 BETA 版本仅仅用于测试，所以 QuecPython 版本并非是正式发布的，故版本号信息不会变更，只能通过编译时间来确认版本，建议用户进行版本控制时也使用这种方式判断版本，拿到测试版本进行测试时也可以方便的进行版本控制。qpyver = V0002 这个字段即为 QuecPython 固件官网发布的正式版本号，在此不过多赘述。

为什么要查询固件版本？

在开发的过程中难免会遇到一些问题，并找到官方人员或技术前辈咨询，那么此时需要提供的信息中，固件版本就是必不可少的，除此之外使用 uos 库查询固件版本还有如下方法：

```python
>>> import uos
>>> uos.uname2()
# 返回值(以EC600U型号为例，需要注意此方法较老的固件版本不支持)
# (sysname='EC600U-CNLB', nodename='EC600U', release='1.13.0', version='v1.12 on Sat_Nov_19_2022_5:29:48_PM', machine='EC600U with QUECTEL', qpyver='V0002')
```

如上所示，此接口和 uos.uname()返回的信息是一样的，只是返回值兼容了 microPython 的用法，更方便用户在脚本中访问返回值中“=”右边的信息，具体用法参考 [uos - 基本系统服务](../../../API_reference/zh/QuecPython标准库/uos.html)。

除此之外我们还可以使用如下方法获取固件版本信息：

```python
>>> import modem
# 查询Quectel固件版本信息(Quectel通用命名规则)
>>> modem.getDevFwVersion()
# 常见返回值类型(以EC600U型号为例)
# 'EC600UCNLBR03A01M08_OCPU_QPY_BETA1207'
# 'EC600UCNLBR03A02M08_OCPU_QPY'
```

如上所示，常见的两种返回值主要区别为是否包含 BETA 字段，包含 BETA 字段的固件为非正式发布版本固件，仅能用于测试，不用于项目量产，BETA 后为编译固件的日期，12 月 7 日。我们一般仅需关注是否包含 BETA 字段和 BETA 后的日期。

此版本号除了使用 QuecPython 脚本查询外还可以使用 AT+GMR 命令进行查询，在这里不是我们的重点。

AT 命令仅需一行即可查询，脚本需要两行，怎么解决？

```python
>>> import modem;modem.getDevFwVersion() # 两行合为一行，交互界面回车即可返回结果
```

## 查询模组运行内存和文件系统剩余空间

```python
import gc
import uos

usr = uos.statvfs("/usr")

print('获取usr目录状态信息:', usr)
print('f_bsize – 文件系统块大小，单位字节：', usr[0])
print('f_bfree – 可用块数：', usr[3])
print('usr剩下总空间 {} 字节'.format(usr[0] * usr[3]))
print('usr剩下总空间 {} KB'.format((usr[0] * usr[3])/1024))
print('usr剩下总空间 {} MB'.format((usr[0] * usr[3]) / 1024 / 1024))

bak = uos.statvfs("/bak")

print('获取bak目录状态信息:', bak)
print('f_bsize – 文件系统块大小，单位字节：', bak[0])
print('f_bfree – 可用块数：', bak[3])
print('bak剩下总空间 {} 字节'.format(bak[0] * bak[3]))
print('bak剩下总空间 {} KB'.format((bak[0] * bak[3])/1024))
print('bak剩下总空间 {} MB'.format((bak[0] * bak[3]) / 1024 / 1024))

mem = gc.mem_free()
print('剩余可用RAM空间:{}KB'.format(mem / 1024))
```

如上所示我们使用 uos.statvfs 这个函数查询了根目录下'usr'和'bak'两个文件夹的状态信息，可以获取到文件夹的剩余空间大小。关于根目录和这两个文件夹做如下简介，根目录：对于用户来说是不允许操作的，所以对根目录做的任何操作都会导致报 OSerror 异常。'usr'目录：此目录是允许客户做文件读写操作的，通常客户代码等文件均是主要存放在这里，如需扩展请看 [外扩存储](./../hardware-advanced/ext-storage.html) 章节。'bak'目录：此目录是用于量产时存放客户需要备份的重要文件，可读不可写，存放重要文件请看 [备份分区和数据安全区的使用](./../mass-production/data-backup.html) 章节。

其他 uos 相关使用请查看 [uos - 基本系统服务](../../../API_reference/zh/QuecPython标准库/uos.html)。

## 查询 microPython 虚拟机版本

```python
>>> try:import usys as sys 
... except ImportError:import sys
>>> sys.implementation
# 返回值
# (name='micropython', version=(1, 13, 0), mpy=10245)
```

如上所示可以直接查询到 microPython 虚拟机版本是 1.13.0 版本，虽然可以查询到 microPython 虚拟机版本，但是不少用法仍和 microPython 不同，需要注意。以上示例使用 try-except 语句进行 import 的原因就是不同时期的固件 microPython 虚拟机版本不同，部分模块出现了更名的情况，为避免出现异常导致程序退出运行，使用了 python 的异常处理语法。后续 QuecPython 将为避免出现此类情况，在移植 microPython 新虚拟机时即将模块命名同历史版本进行兼容，方便用户的使用。

## 查询 microPython 语言版本

```python
>>> try:import usys as sys 
... except ImportError:import sys
>>> sys.version
# 返回值
# '3.4.0'
>>> sys.version_info
# 返回值
# (3, 4, 0)
```

如上所示，使用了两个 API 进行的查询，两个 API 的主要差异为返回值形式不同。当前查询的 microPython 语言版本是 3.4.0，在语法上是兼容电脑端 CPython 的 3.4.0 版本，后续是否有变更可以使用此接口查询。

## 查询设备的 IMEI

```python
>>> import modem
>>> modem.getDevImei()
# 返回值
# '866327040830317'
```

如上所示，获取设备的 IMEI 号虽然十分简单，但是又特别的常用，所以在这里介绍一下如何查询。那么，IMEI 是什么呢？

物联网模块的 IMEI 是国际移动设备身份码（International Mobile Equipment Identity）的缩写，它是用于识别物联网模块的唯一标识符。在物联网场景中，IMEI 可以用于以下几个方面：

1. 设备识别和管理：通过 IMEI，可以唯一地识别和管理物联网设备，包括设备的制造商、型号和版本等信息。这些信息对于设备的维护和升级非常重要。
2. 安全性和防盗：IMEI 可以用于防止设备被盗或丢失。如果设备的 IMEI 被注册到一个中央数据库中，就可以通过该数据库来追踪设备的位置和使用情况。
3. 远程管理和控制：IMEI 可以用于远程管理和控制物联网设备。例如，如果设备出现故障或需要更新固件，就可以通过 IMEI 来远程诊断和修复设备。
4. 数据统计和分析：IMEI 可以用于统计和分析物联网设备的使用情况。例如，可以根据 IMEI 来确定设备的使用时间、位置、频率和使用模式等信息，以便更好地了解设备的使用情况和优化设备的性能。

总之，IMEI 是物联网设备非常重要的标识符，可以用于设备管理、安全性、远程管理和数据分析等方面。

使用 modem 库查询其他设备信息不再赘述，请查看 [modem - 设备相关](./../API_reference/zh/QuecPython类库/modem.html)。

## 总结

用户经常关注的模块相关的，可以通过 microPython 脚本查询到的信息均在此做了介绍，如有疑问或更好的建议欢迎联系我们，也可以直接向我们提交文档贡献，后续本文将继续完善和补充。
