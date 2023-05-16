# 线程_thread 开发常见问题

## 1、线程有个数限制？

最多16个。

## 2、线程栈大小

默认8192字节，展锐平台创建线程支持最大65535字节，ASR平台和CAT M平台 创建线程支持最大的栈size 代码中未设置上限。

## 3、Socket、MQTT、串口的数据监听会不会阻塞其他线程

1、Socket、MQTT本身是‘阻塞函数’，不会阻塞其他线程。

2、串口本身是‘非阻塞函数’，不会阻塞其他线程。

## 4、如何判断线程状态是否正常

多线程编程时，建议在主线程中对其他子线程进行监控，避免其他子线程出现异常情况停止工作等情况导致工作异常。