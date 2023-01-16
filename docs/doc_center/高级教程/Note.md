# QuecPython 高级教程文档编写注意事项

## 目录结构

高级教程根目录下存在一个名为`README.md`的文件，作为高级教程的首页入口。

> 文档中心使用的[teedoc](https://gitee.com/teedoc)架构要求每个版块的首页文件都要是名为`README.md`的文件。

每个功能板块在根目录下均对应一个文件夹，在该文件夹内，按照功能板块，拆分为多个对应的md文件。

所有md文件中引用的图片，均存放于media目录中：
- 高级教程文件夹下有多少文件夹，在media也按照目录关系建立相应的文件夹。
- 图片统一为png格式，命名请见名知意，如`BT.xxx.png`，其中`xxx`表示用简短英文编写的图片作用描述。

目录结构示例如下：

```
QuecPython官网文档中心/高级教程
├── Note.md
├── QuecPython应用框架
│   ├── QuecPython应用框架-EventMesh.md
│   ├── QuecPython应用框架-HeliosService.md
│   └── QuecPython应用框架.md
├── README.md
├── media
│   ├── 云平台对接
│   │   └── Cloud.xxx.png
│   └── 蓝牙开发
│       └── BT.xxx.png
├── 云平台对接
│   ├── 云平台对接-AWS.md
│   ├── 云平台对接-华为云.md
│   ├── 云平台对接-移远云.md
│   ├── 云平台对接-腾讯云.md
│   ├── 云平台对接-阿里云.md
│   └── 云平台对接.md
├── 图形化界面开发
│   ├── 图形化界面开发-Demo-手表.md
│   ├── 图形化界面开发-Demo-贪吃蛇.md
│   ├── 图形化界面开发-LVGL概述.md
│   ├── 图形化界面开发-基础控件应用.md
│   └── 图形化界面开发.md
└── 蓝牙开发
    ├── 低功耗蓝牙开发
    │   ├── 低功耗蓝牙开发-Master.md
    │   └── 低功耗蓝牙开发-Slave.md
    ├── 经典蓝牙开发
    │   ├── 经典蓝牙开发-Master.md
    │   └── 经典蓝牙开发-Slave.md
    └── 蓝牙开发.md
```

## README.md

README.md作为板块的首页入口，需要对该板块做综合性描述，并且在最后提供板块的所有二级目录链接。

## 正文内容格式

参照以下格式：

```markdown
# 低功耗蓝牙开发教程

正文

```

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

## QuecPython 高级教程

[点此查看](./README.md)
