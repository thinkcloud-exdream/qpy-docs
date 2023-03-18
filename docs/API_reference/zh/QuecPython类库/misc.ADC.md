# class ADC - 电压采集功能

用于采集电压信号。

## 构造函数

### `misc.ADC`

```python
class misc.ADC()
```

**示例：**

```python
from misc import ADC
adc = ADC()
```

## 方法

### `ADC.open`

```python
ADC.open()
```

ADC功能初始化。

**返回值描述：**

`0`表示初始化成功，`-1`表示初始化失败。

### `ADC.read`

```python
ADC.read(ADCn)
```

读取指定通道的电压值，单位`mV`。

**参数描述：**

- `ADCn`-ADC通道,int类型,<a href="#label_pinmap">点此查看</a>支持的通道与对应引脚

**返回值描述：**

成功返回指定通道电压值，错误返回整型`-1`。

**示例：**

```python
>>>adc.read(ADC.ADC0)  #读取ADC通道0电压值
613
>>>adc.read(ADC.ADC1)  #读取ADC通道1电压值
605
```

<span id="label_pinmap">**ADC通道与物理引脚的映射关系：**</span>

EC100Y系列对应引脚如下<br/>ADC0 – 引脚号39<br/>ADC1 – 引脚号81<br/>EC600S/EC600N系列对应引脚如下<br/>ADC0 – 引脚号19<br/>EC600M系列对应引脚如下<br/>ADC0 – 引脚号19<br/>ADC1 – 引脚号20<br/>EC800N系列对应引脚如下<br/>ADC0 – 引脚号9<br/>EC600U系列对应引脚如下<br />ADC0 – 引脚号19<br/>ADC1 – 引脚号20<br />ADC2 – 引脚号113<br />ADC3 – 引脚号114<br />EC200U系列对应引脚如下<br />ADC0 – 引脚号45<br/>ADC1 – 引脚号44<br />ADC2 – 引脚号43<br />EC200A系列对应引脚如下<br/>ADC0 – 引脚号45<br/>ADC1 – 引脚号44<br/>BG95系列对应引脚如下<br/>ADC0 – 引脚号24<br/>EG915U系列对应引脚如下<br/>ADC0 – 引脚号24<br/>ADC1 – 引脚号2<br/>EC800M系列对应引脚如下<br/>ADC0 – 引脚号9<br/>ADC1 – 引脚号96<br/>EG912N系列对应引脚如下<br/>ADC0 – 引脚号24<br/>ADC1 – 引脚号2

### ADC.close

```python
ADC.close()
```

**返回值描述：**

`0`表示关闭成功，`-1`表示关闭失败。

## 常量

| 常量     | 说明     | 适用平台                                                     |
| -------- | -------- | ------------------------------------------------------------ |
| ADC.ADC0 | ADC通道0 | EC600S/EC600N/EC100Y/EC600U/EC200U/BC25PA/EC800N/BG95M3/EC200A/EC600M/EG915U/EC800M/EG912N |
| ADC.ADC1 | ADC通道1 | EC600U/EC200U/EC200A/EC600M/EG915U/EC800M/EG912N             |
| ADC.ADC2 | ADC通道2 | EC600U/EC200U                                                |
| ADC.ADC3 | ADC通道3 | EC600U                                                       |