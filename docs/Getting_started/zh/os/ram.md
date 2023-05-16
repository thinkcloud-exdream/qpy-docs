# Ram - 内存管理

本文主要介绍什么是内存管理、怎么使用内存管理等相关问题。

## 内存管理简介

Quecpython的内存可分为模组heap和python虚拟机gc两部分。

### heap管理

heap是模组本身的堆空间，heap不足时往往会引发模组死机，我们并不能直接控制它的使用和释放。但我们可以通过_thread中的接口监控其余量，亦可控制python创建线程时申请的栈空间。

### GC内存管理

GC是模组在启动时分配给python虚拟机的内存，python运行时的对象都存储在这个空间中。GC默认会在用完时触发GC回收，我们可以监控GC使用情况、开关自动回收、调整自动回收阈值，以及手动进行gc回收。



### 软件设计

接口可参考[_thread功能API说明文档](..\..\..\API_reference\zh\QuecPython_stdilb\_thread.md)和[GC功能API说明文档](..\..\..\API_reference\zh\QuecPython_stdilb\gc.md).

## 内存管理功能应用实例

在本文中，我们将使用 QuecPython 开发板，演示GC功能。

### 准备工作

Quecpython开发板

### 代码实现

```python
#heap管理
>>> import _thread
>>> _thread.get_heap_size() #获取剩余heap，单位byte
2199424
>>> _thread.stack_size(8192) #设置python创建线程时申请的栈空间
0
#gc管理
>>> import gc     
>>> gc.mem_free() #获取剩余gc，单位byte
493760
>>> gc.mem_alloc() #获取已申请gc，单位byte
18576
>>> gc.disable() #关闭gc自动回收
>>> gc.isenabled() #查询gc自动回收状态，已关闭
False
>>> gc.enable() #打开gc自动回收
>>> gc.isenabled() #查询gc自动回收状态，已打开
True
>>> gc.threshold(int(512*1024*0.75)) #设置gc自动回收阈值，参数整型，单位byte，gc使用量达到参数值时触发gc回收，可由总量乘百分比得到

>>> gc.collect() #手动触发gc回收
>>> gc.mem_free() #已经不再使用（所属对象引用计数器被置零）的gc内存被回收，gc总量回升
506928
```

## 总结

内存管理功能在此做了详细的介绍，如有疑问或更好的建议欢迎联系我们，也可以直接向我们提交文档贡献，后续本文将继续完善和补充更多应用案例。