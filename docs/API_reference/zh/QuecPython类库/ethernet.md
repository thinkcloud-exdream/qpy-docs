# `ethernet` - 以太网相关功能
`ethernet`模块包含以太网控制及网络配置功能。主要是针对不同类型以太网卡提供统一的管理方式。

**示例：**  

根据不同应用场景，分别以终端模式、网关模式、静态ip配置举例网卡初始化使用过程。

<div class="warn">
<body>
1. 以下示例只是针对模组侧的网卡应用配置，也需要对端进行对应操作方可正常使用。<br>
2. 以下示例部分网卡未完全实现，请根据不同网卡驱动对应说明进行使用。
</body>
</div>

终端模式：

```python
# 作为终端工作模式时，模块通过以太网网口连接外网。如W5500网口连接路由器，通过dhcp获取ip信息，从而模组可以通过该网口连接外部网络。

import ethernet

# 加载对应的网卡驱动，并初始化网卡相关配置，driver替换成实际对应的网卡驱动
nic = ethernet.diver(...)
print(nic.ipconfig())

# 获取动态IP地址
nic.dhcp()
print(nic.ipconfig())

# 此时可以启动其他网络服务，并通过以太网进行网络访问
...

```

网关模式：

```python
# 作为网关使用配置时，使用4G连接外网。如W5500网口连接电脑，电脑需要配置静态ip与W5500以太网卡同一网段，网关与W5500网卡地址一致，从而电脑能够通过4G网卡连接网络。
import ethernet
import dataCall

# 加载对应的网卡驱动，并初始化网卡相关配置，driver替换成实际对应的网卡驱动
nic = ethernet.diver(...)
print(nic.ipconfig())

# 获取当前4G拨号ip信息
lte=dataCall.getInfo(1, 0)
print(lte)
if lte[2][0] == 1:
  # 设置默认网卡，将4G作为默认网卡
  nic.set_default_NIC(lte[2][2]) 

#启动网卡
nic.set_up()

# 此时其他设备可以通过网线连接模组，实现4G上网
...

```

静态IP配置： 

```python
# 静态ip配置，根据当前已有环境，自定义网络信息。
import ethernet

# 加载对应的网卡驱动，并初始化网卡相关配置，driver替换成实际对应的网卡驱动
nic = ethernet.diver(...)
print(nic.ipconfig())

# 配置静态ip地址192.168.0.2，子网掩码255.255.255.0，网关地址192.168.0.1
nic.set_addr('192.168.0.2','255.255.255.0','')
print(nic.ipconfig())

# 启动网卡
nic.set_up()

# 终端模式下，此时可以启动其他网络服务，并通过以太网进行网络访问
...

```

## Classes
- [class W5500 – W5500驱动](./ethernet.W5500.md)
- [class DM9051 – DM9051驱动](./ethernet.DM9051.md)
- [class CH395 – CH395驱动](./ethernet.CH395.md)
- [class YT8512H/SZ18201 – YT8512H/SZ18201驱动](./ethernet.YT8512H.md)
