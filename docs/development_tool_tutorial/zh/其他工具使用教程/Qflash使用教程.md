## Qflash

该工具用于固件升级烧录，无需安装便可直接在装有Windows系统上运行，在[下载](https://python.quectel.com/download)之后对压缩包进行解压，运行 QFlash.exe

注意事项：

1、工具和固件包的存储路径不应包含任何空格，推荐使用英文字符；

2、固件包的存储/载入路径需是本地路径，不能使用 U 盘或网盘路径；

支持型号：ASR，RDA双平台，移芯平台目前需要特定版本才能烧录，请联系技术支持人员；

ASR平台需要把固件后缀改为.zip；

官网下载固件并解压，模块上电开机之后，选择适配的固件，端口选择AT Port串口或通过发送AT指令**AT+QDOWNLOAD=1**进入强制下载模式选择下载口，点击“**Start**”后工具会自动切换到下载端口并完成升级。若升级完成后仍是下载口，需要重启模块恢复端口加载。

<img src="..\media\其他工具使用教程\其他工具_QFlash界面介绍1.png" style="border-style: solid; border-radius: 10px; color: \#f1f1f1;" border=3 alt="">

固件烧录中

<img src="..\media\其他工具使用教程\其他工具_QFlash固件烧录1.png" style="border-style: solid; border-radius: 10px; color: \#f1f1f1;" border=3 alt="">

固件烧录完成

<img src="..\media\其他工具使用教程\其他工具_QFlash固件烧录2.png" style="border-style: solid; border-radius: 10px; color: \#f1f1f1;" border=3 alt="">