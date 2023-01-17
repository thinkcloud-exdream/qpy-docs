# QuecPython 开发指南编写注意事项

## 目录结构

开发指南根目录下存在一个名为`README.md`的文件，作为开发指南的首页入口。

> 文档中心使用的[teedoc](https://gitee.com/teedoc)架构要求每个版块的首页文件都要是名为`README.md`的文件。

每个功能板块在根目录下均对应一个文件夹，在该文件夹内，按照功能板块，拆分为多个对应的md文件。

所有md文件中引用的图片，均存放于media目录中：
- 开发指南文件夹下有多少文件夹，在media也按照目录关系建立相应的文件夹。
- 图片统一为png格式，命名请见名知意，如`BSP.xxx.png`，其中`xxx`表示用简短英文编写的图片作用描述。

目录结构示例如下：

```
QuecPython官网文档中心/开发指南
├── BSP应用开发
│   ├── BSP-Audio应用开发.md
│   ├── BSP-GPIO应用开发.md
│   ├── BSP-UART应用开发.md
│   └── BSP应用开发.md
├── Note.md
├── OTA升级
│   ├── OTA升级-固件.md
│   ├── OTA升级-文件.md
│   └── OTA升级.md
├── README.md
├── media
│   ├── BSP应用开发
│   │   └── BSP.xxx.png
│   └── OTA升级
│       └── OTA.xxx.png
├── 外设应用开发
│   ├── 外设-LCD应用开发.md
│   ├── 外设-摄像头应用开发.md
│   └── 外设应用开发.md
├── 多线程应用开发
│   ├── 多线程-互斥锁应用.md
│   ├── 多线程-创建线程.md
│   ├── 多线程-消息队列应用.md
│   └── 多线程应用开发.md
├── 快速入门.md
└── 网络通信应用开发
    ├── 网络通信-HTTP通信.md
    ├── 网络通信-MQTT通信.md
    ├── 网络通信-SNMP通信.md
    ├── 网络通信-TCP与UDP通信.md
    ├── 网络通信-WebSocket通信.md
    ├── 网络通信-数据拨号.md
    └── 网络通信应用开发.md
```

## README.md

README.md作为板块的首页入口，需要对该板块做综合性描述，并且在最后提供板块的所有二级目录链接。

## 正文内容格式

参照以下格式：

```markdown
# BSP 应用开发

正文

```

## QuecPython 开发指南

[点此查看](./README.md)
