# `pm` - 低功耗

模块功能：在无业务处理时使系统进入休眠状态，进入低功耗模式。

## 创建wake_lock锁

### `pm.create_wakelock`

```python
pm.create_wakelock(lock_name, name_size)
```

创建wake_lock锁。

- **参数描述**

| 参数      | 类型   | 说明            |
| :-------- | :----- | --------------- |
| lock_name | string | 自定义lock名    |
| name_size | int    | lock_name的长度 |

* **返回值描述**

成功返回wakelock的标识号，否则返回-1。

> **注意**:BC25PA平台不支持此方法。

## 删除wake_lock锁

### `pm.delete_wakelock`

```python
pm.delete_wakelock(lpm_fd)
```

删除wake_lock锁。

- **参数描述**

| 参数   | 类型 | 说明                   |
| :----- | :--- | ---------------------- |
| lpm_fd | int  | 需要删除的锁对应标识id |

* **返回值描述**

成功返回0。

> **注意**：BC25PA平台不支持此方法。


## 加锁

### `pm.wakelock_lock`

```python
pm.wakelock_lock(lpm_fd)
```

- **参数描述**

| 参数   | 类型 | 说明                             |
| :----- | :--- | -------------------------------- |
| lpm_fd | int  | 需要执行加锁操作的wakelock标识id |

* **返回值描述**

成功返回0，否则返回-1。

> **注意**：BC25PA平台不支持此方法。


## 释放锁

### `pm.wakelock_unlock`

```python
pm.wakelock_unlock(lpm_fd)
```

释放锁

- **参数描述**

| 参数   | 类型 | 说明                               |
| :----- | :--- | ---------------------------------- |
| lpm_fd | int  | 需要执行释放锁操作的wakelock标识id |

* **返回值描述**

成功返回0，否则返回-1。

> **注意**：BC25PA平台不支持此方法。

## 自动休眠模式控制

### `pm.autosleep`

```python
pm.autosleep(sleep_flag)
```

自动休眠模式控制

- **参数描述**

| 参数       | 类型 | 说明                           |
| :--------- | :--- | ------------------------------ |
| sleep_flag | int  | 0，关闭自动休眠；1开启自动休眠 |

* **返回值描述**

成功返回0，失败返回-1



## 获取已创建的锁数量

### `pm.get_wakelock_num`

```python
pm.get_wakelock_num()
```

获取已创建的锁数量

- **参数描述**

无

* **返回值描述**

返回已创建wakelock锁的数量。

> 注意：BC25PA平台不支持此方法。



## 设置PSM模式的控制时间

### `pm.set_psm_time`

```python
pm.set_psm_time(tau_uint,tau_time,act_uint,act_time)  # 设置并启用PSM <模式1>

pm.set_psm_time(mode)# 单独设置启用或禁用 <模式2>
```




* **参数描述**

| 参数     | 参数类型 | 参数说明                                                     |
| -------- | -------- | ------------------------------------------------------------ |
| mode     | int      | 是否启用PSM:<br/>0 禁用PSM<br/>1 启用PSM<br/>2 (仅BC25平台)禁用PSM并删除PSM的所有参数，如有默认值，则重置默认值。(注意此种模式禁用的情况下，如果要启用PSM必须用**模式1**，用**模式2**没有任何的意义,因为设置的TAU和ACT时间全部清零了)。 |
| tau_uint | int      | tau(T3412)定时器单位                                         |
| tau_time | int      | tau(T3412)定时器时间周期值                                   |
| act_uint | int      | act(T3324)定时器单位                                         |
| act_time | int      | act(T3324)定时器时间周期值                                   |

* **tau定时器说明**

| tau定时器单位值 | 类型 | 单位值说明   |
| --------------- | ---- | ------------ |
| 0               | int  | 10 分钟      |
| 1               | int  | 1 小时       |
| 2               | int  | 10 小时      |
| 3               | int  | 2 秒         |
| 4               | int  | 30 秒        |
| 5               | int  | 1 分钟       |
| 6               | int  | 320 小时     |
| 7               | int  | 定时器被停用 |

* **act定时器单位说明**

| act定时器单位值 | 类型 | 单位值说明   |
| --------------- | ---- | ------------ |
| 0               | int  | 2 秒         |
| 1               | int  | 1 分钟       |
| 2               | int  | 6 分钟       |
| 7               | int  | 定时器被停用 |

* **返回值**

  True: 	成功
  False:	失败


- **示例**

```python
>>> import pm
>>> pm.set_psm_time(1,2,1,4)  #设置tau定时器周期为 1小时 * 2 = 2小时， act定时器周期值为 1分钟 * 4 = 4分钟。
True
>>>
```

> **注意**：仅BC25/ECX00U/ECX00E支持

## 获取PSM模式的控制时间

### `pm.get_psm_time`

```python
pm.get_psm_time()
```



* **参数**

  无

* **返回值**

  成功：返回值为list类型，说明如下：

  | 参数    | 类型 | 单位值说明                                                   |
  | ------- | ---- | ------------------------------------------------------------ |
  | list[0] | int  | mode说明: <br/>0-禁用PSM. <br/>1-启用PSM. <br/>2-(仅BC25平台)禁用 PSM 并删除 PSM 的所有参数,若有默认值,则重置为默认值。 |
  | list[1] | int  | tau定时器单位                                                |
  | list[2] | int  | tau定时器时间周期值                                          |
  | list[3] | int  | act定时器单位                                                |
  | list[4] | int  | act定时器时间周期值                                          |

  失败：返回None。

- **示例**


```python
>>> pm.get_psm_time()

[1, 1, 1, 1, 2]


```

> **注意**：仅BC25/ECX00U/ECX00E平台支持

##### 使用示例

模拟测试，实际开发请根据业务场景选择使用！

```python
import pm
import utime

# 创建wakelock锁
lpm_fd = pm.create_wakelock("test_lock", len("test_lock"))
# 设置自动休眠模式
pm.autosleep(1)

# 模拟测试，实际开发请根据业务场景选择使用
while 1:
    utime.sleep(20)  # 休眠
    res = pm.wakelock_lock(lpm_fd)
    print("ql_lpm_idlelock_lock, g_c1_axi_fd = %d" %lpm_fd)
    print("unlock  sleep")
    utime.sleep(20)
    res = pm.wakelock_unlock(lpm_fd)
    print(res)
    print("ql_lpm_idlelock_unlock, g_c1_axi_fd = %d" % lpm_fd)
    num = pm.get_wakelock_num()  # 获取已创建锁的数量
    print(num)
```


