# QuecPython 入门学习路线

 QuecPython 移植于 MicroPython 开源库，开发者在移远通信模块上 使 用 MicroPython 即可调用模块软件功能和外部硬件接口，进行二次开发。与open C相比，QuecPython开发具有轻松入门、语法简介、随写随测等优点，大大降低了用户开发学习的门槛。

## 入门要求

物联网开发向上承接了互联网，向下承接了嵌入式硬件。QuecPython开发需要有一定的嵌入式开发经验，了解相关硬件知识，API接口等。

## 语法学习

QuecPython移植于MicroPython，无论是在功能接口定义还是目录结构形式都与MicroPython保持高度的一致。MicroPython是Python3语言的精简高效实现，开发者在入门学习时因掌握基础的Pyhton3语法。需要注意的是Python3与QuecPython只是语法上兼容，脚本里导入的库和函数会存在差异，不能将电脑端运行的脚本放在QuecPyhton上运行，QuecPython相关库可参考官网WIKI。

## 开发板选型

目前QuecPython的开发板有QuecPython 开发板、核心板和DTU开发板等，用户可根据自身需求选择对应的开发板。如果是初学者可购买QuecPython 开发板，它资源相对丰富，适合入门学习。其他两种型号开发板可用于项目调试上，只需要用到部分硬件资源。

## 快速上手

一、Hello World打印

1.开发板接入电脑，需要安装驱动和烧录模块固件，具体的操作方法参照《QPYcom工具使用说明》

2.hello world打印

（1）交互窗口打印

如下图所示，使用QPYcom工具，端口连接“QuecPython的交互端口”，选择“交互”界面，进行如下交互打印。

![](E:\QuecPython网站搬移\V1\teedoc_with_qpydoc\docs\development_guide\zh\media\QuecPython快速入门\快速入门_入门学习_1.jpg)

（2）编写*test_helloworld.py*文件打印

创建*test_helloworld.py*文件，编写脚本如下所示

```python
import utime    # 导入定时模块
print_num = 5   # 定义打印次数
while print_num:
    print("hello world")
    print_num -= 1   # 自减
    utime.sleep(2)   # 延迟2秒
```



