# QuecPython 开发工具使用教程编写注意事项

## 目录结构

开发工具使用教程根目录下存在一个名为`README.md`的文件，作为开发工具使用教程的首页入口。

> 文档中心使用的[teedoc](https://gitee.com/teedoc)架构要求每个版块的首页文件都要是名为`README.md`的文件。

每个工具在根目录下均对应一个`XXX使用教程`的文件夹，在该文件夹内，按照工具的功能板块，拆分为多个对应的md文件。

所有md文件中引用的图片，均存放于media目录中：
- 工具文档下有多少文件夹，在media也按照目录关系建立相应的文件夹。
- 图片统一为png格式，命名请见名知意，如`QPYcom.xxx.png`，其中`xxx`表示用简短英文编写的图片作用描述。

目录结构示例如下：

```
QuecPython官网文档中心/开发工具使用教程
├── Note.md
├── QPYcom使用教程
│   ├── QPYcom使用教程-REPL交互.md
│   ├── QPYcom使用教程-固件合成与烧录.md
│   └── QPYcom使用教程-文件传输.md
├── media
│   ├── QPYcom使用教程
│   │   └── QPYcom.xxx.png
│   └── 产测工具使用教程
│       └── 产测工具.xxx.png
└── 产测工具使用教程
    ├── 产测工具使用教程-fnc1.md
    └── 产测工具使用教程-fnc2.md
```

## README.md

README.md作为板块的首页入口，需要对该板块做综合性描述，并且在最后提供板块的所有二级目录链接。

## 正文内容格式

参照以下格式：

```markdown
# QPYcom REPL交互使用教程

正文

```

## QuecPython 开发工具使用教程

[点此查看](./README.md)
