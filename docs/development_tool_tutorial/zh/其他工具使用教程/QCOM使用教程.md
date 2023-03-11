## QCOM

该工具用于串口发送和接收数据。

在QuecPython官网中对该工具进行[下载](https://python.quectel.com/download)，解压后双击运行QCOM_V1.6.exe<img src="..\media\其他工具使用教程\其他工具_QCOM下载.png" style="border-style: solid; border-radius: 10px; color: \#f1f1f1;" border=3 alt="">

功能如图所示：<img src="..\media\其他工具使用教程\其他工具_QCOM界面介绍1.png" style="border-style: solid; border-radius: 10px; color: \#f1f1f1;" border=3 alt="">

黄色区域用于设置端口信息。

红色区域显示接收到的数据。

蓝色区域显示状态信息。

紫色区域用于发送数据或文件。

绿色区域用于连续发送数据。

根据PC与终端的连接情况，设置对应的端口信息，其中包含对端口号、波特率、数据位、校验位、停止位、流控制的设置，在完成以上设置之后，点击Open Port打开所选择的端口。

<img src="..\media\其他工具使用教程\其他工具_QCOM界面介绍2.png" style="border-style: solid; border-radius: 10px; color: \#f1f1f1;" border=3 alt="">

<img src="..\media\其他工具使用教程\其他工具_QCOM界面介绍3.png" style="border-style: solid; border-radius: 10px; color: \#f1f1f1;" border=3 alt="">

A)红色区域用于输入将要发送的数据。

B)绿色区域用于选择需要的文件并发送整个文件。

C)蓝色区域用于将接收到的数据保存为文件。

D) DTR：开启COM口的DTR引脚。

E) RTS：启用COM口的RTS引脚。

F) View File：显示已发送文件的数据。

G) Show Time：显示每个接收数据的时间。

H) HEX String：输入字符串为HEX String。

I) Show in HEX：接收到的数据以HEX格式显示。

J) Send with Enter：按“Enter”发送数据。

K)Clear Information：清除所有接收到的数据和状态信息。

L)Send Command：开始发送您输入的数据。

M)Select File：选择要发送的文件。

N)Send File：开始发送您选择的文件。

O) Save Log：选择保存日志数据的文件。

<img src="..\media\其他工具使用教程\其他工具_QCOM界面介绍4.png" style="border-style: solid; border-radius: 10px; color: \#f1f1f1;" border=3 alt="">

A)红色区域用于发送数据。

B)蓝色区域用于输入将要发送的命令或数据。

C)绿色区域用于开始数据发送。

D)Choose All Commands：启用所有可发送的命令。

E) HEX：输入字符串为HEX字符串。

F) Enter：按“Enter”键发送数据。

G)延迟：每个数据的延迟时间。

H)延迟时间：默认延迟时间。

I)运行次数：连续发送所有选定数据的次数。

J) Run：开始连续发送所有选中的数据。

K)Stop：停止连续发送所有所选数据。

L) Save As Script：保存所有数据并配置为ini文件。

M)Load Test Script：从ini文件加载数据和配置。

N)Clear All Commands：清除所有的命令或数据。

### AT命令的发送

打开设备管理器，确定AT串口，打开QCOM，选择AT串口，点击**Open Port**，端口设置会变灰，同时也会看到 Open COM Port Success字样，说明串口已经成功打开；勾选**Send With Enter**，在 Input String 框内输入 **AT**，然后点击 **Send Command** 按钮进行发送，模块端正常回复相应数据。

<img src="..\media\其他工具使用教程\其他工具_QCOM界面介绍5.png" style="border-style: solid; border-radius: 10px; color: \#f1f1f1;" border=3 alt="">