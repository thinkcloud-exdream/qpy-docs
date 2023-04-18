# ntptime - 网络时间同步

该模块用于网络时间同步。

> BC25PA平台电信卡开卡时需要说明SIM卡须支持此类业务，移动联通一般不限制(开卡时需要和运营商确认)。


### `ntptime.host`

```python
ntptime.host
```
**返回值描述：**

* 返回当前的ntp服务器，默认为"ntp.aliyun.com"。


### `ntptime.sethost`

```python
ntptime.sethost(host)
```

设置ntp服务器。

**参数描述：**

* `host` -  ntp服务器地址，字符串类型


**返回值描述：**

* 成功返回整型值0，失败返回整型值-1。


### `ntptime.settime`

```python
ntptime.settime(timezone=0)
```

同步ntp时间。

**参数描述：**

* `timezone` -  时区设置，默认为0, 范围 (-12~12)，int类型


**返回值描述：**

* 成功返回整型值0，失败返回整型值-1。



**示例：**

```python
import ntptime
import log
import utime
import checkNet


'''
下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值
'''
PROJECT_NAME = "QuecPython_NTP_example"
PROJECT_VERSION = "1.0.0"

checknet = checkNet.CheckNetwork(PROJECT_NAME, PROJECT_VERSION)

# 设置日志输出级别
log.basicConfig(level=log.INFO)
ntp_log = log.getLogger("NtpTime")

if __name__ == '__main__':
    stagecode, subcode = checknet.wait_network_connected(30)
    if stagecode == 3 and subcode == 1:
        ntp_log.info('Network connection successful!')

        # 查看默认ntp服务
        ntp_log.info(ntptime.host)
        # 设置ntp服务
        ntptime.sethost('pool.ntp.org')

        # 同步ntp服务时间
        ntptime.settime()
    else:
        ntp_log.info('Network connection failed! stagecode = {}, subcode = {}'.format(stagecode, subcode))
```