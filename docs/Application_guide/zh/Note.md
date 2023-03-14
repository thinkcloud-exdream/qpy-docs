# QuecPython 高级教程文档编写注意事项

## 目录结构

目录结构示例如下：

```
QuecPython官网文档中心/Application_guide
├── Note.md
├── README.md
├── bsp
│   ├── README.md
│   ├── gpio.md
│   ├── iic.md
│   ├── spi.md
│   └── uart.md
├── config.json
├── media
│   └── network
│       └── test.png
├── network
│   ├── README.md
│   ├── datacall.md
│   ├── http
│   │   ├── http_get.md
│   │   └── http_post.md
│   ├── mqtt.md
│   └── socket
│       ├── tcp_client.md
│       ├── tcp_server.md
│       └── udp.md
└── sidebar.yaml
```

## README.md

README.md作为板块的首页入口，需要对该板块做综合性描述，并且在最后提供板块的所有二级目录链接。

## 正文注意事项

1. 若该技术板块存在多种应用场景，每种应用场景均需对应一篇文档，如socket编程，会存在 tcp client，tcp server 和 udp 三种不同场景，需编写3片文档。

2. 每篇文档按照常规的应用开发流程描述即可，可粘贴每个开发环节对应的代码片段，完整的代码由于篇幅过程，禁止粘贴在文档中，而是在文末给出代码链接。

3. 代码链接必须指向[https://github.com/QuecPython](https://github.com/QuecPython)组织中的仓库，禁止将代码仓库放在任何其他组织中。

> 代码仓库的建立，联系Chavis。

## QuecPython 应用指导

[点此查看](./README.md)
