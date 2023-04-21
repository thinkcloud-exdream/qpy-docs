# USBNET应用指导说明

本文中对USBNET一些基础概念进行了简要说明，描述了如何使用 QuecPython 的`USBNET`模块的功能，包含USB网卡使用的前提条件。



## 1. 基础概念说明

### 1.1 什么是USBNET

USBNET（Universal Serial Bus Network），是一种USB网络技术，可以通过USB接口在计算机之间传输数据。它通常用于连接嵌入式设备，例如智能手机或网络路由器，与计算机进行通信。USBNET技术使嵌入式设备可以像普通计算机一样直接连接到网络，从而方便了设备的管理和控制。因此，USBNET被广泛应用于各种计算机和网络设备中。



### 1.3 `ECM`模式和`RNDIS`模式的区别
ECM和RNDIS是USBNET中的两种网络模式。具体区别如下：

* `ECM` - 全称是"Ethernet Control Model"，它是一种通过USB连接来模拟Ethernet网络连接的技术。ECM能够在device和host之间交换ethernet frame， 符合ECM规范的设备，认为自己是一个虚拟的网络接口， 可以被分配MAC和IP。ECM可以被用于连接任何支持TCP/IP协议的设备，例如计算机、网络路由器、智能手机等，从而使它们可以直接访问网络。

* `RNDIS` - 全称是"Remote Network Driver Interface Specification"，它是一种使嵌入式设备通过USB接口来实现远程网络连接的技术，实际上就是TCP/IP over USB。RNDIS可以让嵌入式设备直接连接到计算机的网络，从而方便了设备的管理和控制。

因此，ECM和RNDIS都是USBNET中常见的网络模式，它们可以使嵌入式设备通过USB连接实现网络连接和通信。



### 1.2 什么是PID

PID是"Product ID"的缩写，指的是USB设备的产品标识号。每一个USB设备都必须拥有唯一的PID，以便计算机能够识别和区分不同的USB设备。PID通常由USB设备制造商进行分配，并写入设备的固件中。
在USB连接建立时，计算机会读取USB设备的PID信息，并根据PID来确定设备的厂商和型号等信息。这些信息可以用来识别设备，并为其加载正确的驱动程序，以确保设备可以正常工作。因此，PID是USB设备中重要的标识之一。



## 2. USBNET应用指导文档列表

* [USBNET功能应用指导](./usbnet.md)


