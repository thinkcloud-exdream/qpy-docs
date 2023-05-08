# 屏幕显示

本章节介绍使用QuecPython进行屏幕点亮显示，目前QuecPython开发支持的屏幕接口有SPI、MIPI、I2C（段码屏）等，具体模组支持的接口详情在下表8-1所示；下文以QuecPython开发常用的LCD进行开发介绍。

| 模组型号                    | LCD接口        |
| --------------------------- | -------------- |
| EC200U\EC600U               | MIPI、SPI、I2C |
| EC600N\EC600M\EC800M\EC800M | SPI、I2C       |

表8-1

## LCD介绍

LCD（Liquid Crystal Display），液晶显示器，为平面超薄的显示设备，它由一定数量的彩色或者黑白像素组成，放置于光源或者反射面前方。它的主要原理是以电流刺激液晶分子产生点、线、面配合背部灯管构成画面。

QuecPYthon开发常中，LCD的几个重要的参数有驱动IC、屏幕尺寸以及分辨率等，在选型中，可根据模组支持的接口去选择对应的LCD。目前公版固件中，SPI接口的LCD最大分辨率支持240×320，MIPI接口支持最大的分辨率为480×854（开发板“铀”）。

ST7789V LCD为官方天猫旗舰店售卖的一款屏幕，可搭配QuecPython开发板进行开发，该屏幕的驱动IC为ST7789V，SPI接口，分辨率为240×240，接口定义如下表8-2所示。

| 序号 | LCD引脚 | 引脚定义                       |
| ---- | ------- | ------------------------------ |
| 1    | GND     | 电源地                         |
| 2    | VCC     | 电源3.3V                       |
| 3    | SCL     | SPI总线时钟信号                |
| 4    | SDA     | SPI总线写数据信号              |
| 5    | RES     | 液晶屏复位控制信号，低电平复位 |
| 6    | DC      | 写寄存器/写数据控制信号        |
| 7    | BLK     | 液晶屏背光控制信号             |

表8-2

##  硬件连接

### SPI类型的屏幕

模组有LCD显示驱动的接口LCM（LCD Module），可用于SPI LCD的屏幕，当然也可以选择模组其他SPI接口。具体的硬件连接可参考下表，需要注意的是，模组引脚的电压域为1.8V，需经过电平转换之后方可使用。

| ST7789V LCD | 模组LCM接口  | 模组SPI接口 |
| :---------- | ------------ | ----------- |
| SCL         | LCD_SPI_CLK  | SPI_SCLK    |
| SDA         | LCD_SPI_DOUT | SPI_MOSI    |
| RES         | LCD_RST      | gpio复用    |
| DC          | LCD_SPI_RS   | gpio复用    |
|             | LCD_CS       | SPI_CS      |

### MIPI类型的屏幕

目前支持MIPI的模组有EC200U/EC600U系列，需要搭配6线FLASH使用，可参考QuecPython开发板“铀“的电路，具体硬件连接请联系移远技术支持进行确认。

## 驱动代码编写

选择一款屏幕后正常情况下屏幕厂商会提供C的驱动代码，需要将C代码转成python脚本，下面介绍部分参数的格式，详情文档看《基于QUECPYTHON实现SPI类型屏幕驱动》、《基于QuecPython-MIPI大屏使用指导》。

SPI类型格式参数如下：

type  + len + value

type：0:cmd; 1:data; 2:delay

len: 若 type 为 cmd: len 表示后面接多少个 data  ;若 type 为 data: len 表示 data 的长度  ;若 type 为 delay: len 无实际意义。为 0 即可  

value: 若 type 为 delay：表示延时的时长，单位为 ms。 

MIPI类型格式参数如下：

cmd + delay_ms + data_len + data_list

cmd: 命令

delay_ms：延时多久，单位为ms

data_len: 对应命令后接多个数据

data_list：实际数据

## 实验测试

用开发板连接LCD屏，插入USB上电后能看到LCD屏幕有背光亮起，但此时的LCD还未进行初始化，无法进行其他显示操作，需执行初始化程序之后就能进行图片文字显示已经gui显示等。

执行初始化之前

![](E:\QuecPython网站搬移\V3\teedoc_with_qpydoc_1\docs\Getting_started\zh\media\hardware-advanced\lcd_display\lcd_display_1.jpg)

执行初始化之后

![](E:\QuecPython网站搬移\V3\teedoc_with_qpydoc_1\docs\Getting_started\zh\media\hardware-advanced\lcd_display\lcd_display_2.jpg)



