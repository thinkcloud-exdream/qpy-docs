# QuecPython API 参考手册编写注意事项

## 编写规范

参考[Quectel_QuecPython_WiKi编写规范.pdf](https://knowledge.quectel.com/download/attachments/151561997/%5BInternal%5DQuectel_QuecPython_WiKi%E7%BC%96%E5%86%99%E8%A7%84%E8%8C%83_V1.0.0_Preliminary_20230112.pdf?api=v2)。

## 目录结构

API 参考手册根目录下存在一个名为`README.md`的文件，该文件用来描述 QuecPython 的简介和 API 三个板块的的入口链接。

> 文档中心使用的[teedoc](https://gitee.com/teedoc)架构要求每个版块的首页文件都要是名为`README.md`的文件。

参照原官网的三个主要板块，将 API 参考手册的目录结构整体划分为 [QuecPython 标准库](https://python.quectel.com/wiki/#/zh-cn/api/pythonStdlib)、[QuecPython类库](https://python.quectel.com/wiki/#/zh-cn/api/QuecPythonClasslib) 和 [QuecPython组件库](https://python.quectel.com/wiki/#/zh-cn/api/QuecPythonThirdlib)。

每个目录结构下，均有对应的同名md文件，这些md文件分别对相应的板块做了综合叙述，并列出了板块中包含了哪些模块，点击这些模块名，就可以跳转到对应的模块的md文件中。

同时，每个目录下，也包含了一系列名为`<modname>.md`的文件，用来描述名为`<modname>`的模块的API；若模块下包含类，则在该目录下创建名为`<modname>.<classname>.md`。以`machine`模块为例，在`QuecPython类库`目录下应创建`machine.md`文件，其下存在`Pin`等类，需要创建`machime.Pin.md`文件。

所有md文件中引用的图片，均存放于media目录中：
- README.md中的图片存放于media根目录。
- 其余文件中的图片请存放于media下的对应目录中。
- 图片统一为png格式，命名请见名知意，如`machine.Pin.xxx.png`，其中`xxx`表示用简短英文编写的图片作用描述。

目录结构示例如下：

```
QuecPython官网文档中心/API手册
├── README.md
├── QuecPython标准库
│   ├── QuecPython标准库.md
│   ├── gc.md
│   ├── ubinascii.md
│   ├── ucollections.md
│   ├── uos.md
│   └── urandom.md
├── QuecPython类库
│   ├── QuecPython类库.md
│   ├── atcmd.md
│   ├── cellLocator.md
│   ├── dataCall.md
│   ├── example.md
│   ├── machine.Pin.md
│   ├── machine.md
│   └── wifilocator.md
├── QuecPython组件库
│   ├── QuecPython组件库.md
│   ├── TenCentYun.md
│   ├── aLiYun.md
│   ├── log.md
│   ├── request.md
│   └── umqtt.md
└── media
    ├── QuecPython架构.png
    ├── QuecPython标准库
    │   └── uos.xxx.png
    ├── QuecPython类库
    │   ├── machine.xxx.png
    │   └── machine.Pin.xxx.png
    └── QuecPython组件库
        └── umqtt.xxx.png
```

## README.md

README.md作为板块的首页入口，需要对该板块做综合性描述，并且在最后提供板块的所有二级目录链接。

## 关于 CSS 样式

文档在QuecPython官网上会按照某个CSS样式进行效果渲染。

该CSS样式存放于远程git仓库。拉取命令如下：

```bash
git clone https://toscode.gitee.com/qpy-doc-center/typora-theme-pie.git
```

需要在每一个md文件的第一行添加如下代码：

```html
<link rel="stylesheet" type="text/css" href="path/to/typora-theme-pie/pie.css">
```

其中，`path/to/typora-theme-pie/pie.css`表示CSS样式相对于当前md的相对路径。

> 因为后台会对文档自动进行该CSS样式渲染，因此提交的文档开头可不必添加上述CSS样式的应用。

## QuecPython API 参考手册

[点此查看](./README.md)
