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

1. 若该技术板块存在多种应用场景，每种应用场景均需对应一篇文档，如socket编程，会存在 tcp client，tcp server 和 udp 三种不同场景，需编写3篇文档。
2. 每篇文档按照常规的应用开发流程描述即可，可粘贴每个开发环节对应的代码片段，完整的代码由于篇幅过程，禁止粘贴在文档中，而是在文末给出代码链接。
3. 代码链接必须指向[https://github.com/QuecPython](https://github.com/QuecPython)组织中的仓库，禁止将代码仓库放在任何其他组织中。代码仓库的建立，联系Chavis。

> 代码仓库的建立，联系Chavis。

4. 应根据文档所属功能在当前目录下新建对应子目录，如网络相关的md文件，则新建network目录，将对应md文件存在在network目录下；若同一个功能模块需要编写多篇文档，如socket模块，需要编写tcp client.md，tcp server.md 和 udp.md 3篇文档，则应该在network目录下再新建socket子目录用于存放这3篇文档。

5. 所有md文档中引用的图片，都应根据文档所属功能在media目录下新建合适的子目录，并将图片文件存放在该子目录下：

   * 图片格式统一为png格式；
   * 图片命名符合见名知意的要求，如bsp.uart.xxx.png，其中`xxx`表示用简短英文编写的图片作用描述。

6. 应用指导文档的编写应包含功能简介、应用场景说明、功能实现、注意事项几个部分，注意事项部分可选，没有则不写。

   * 若该技术板块只需要写一篇md文档，则该文档中需要包含：功能简介、应用场景说明、功能实现、注意事项（可选）；
   * 若该技术板块需要按应用场景编写多篇md文档，则功能简介应放到README.md中，其他几项放到各自的md中，如socket示例如下：

   ```
   socket
   ├-- README.md		：socket简介
   ├-- tcp_client.md	：tcp client 应用场景、功能实现、注意事项
   ├-- tcp_server.md	：tcp server 应用场景、功能实现、注意事项
   └-- udp.md			：udp 应用场景、功能实现、注意事项
   ```

   

## QuecPython 应用指导

[点此查看](./README.md)