# `class Pin` - I/O引脚控制

Pin对象用来控制I/O引脚（以GPIO为大家所熟知）。Pin对象一般与一个物理引脚关联，可以驱动输出电平或读取电平。Pin类提供方法来设置引脚的模式、设置或获取引脚逻辑电平。对模拟引脚的控制，参考[ADC](http://docs.micropython.org/en/latest/esp32/quickref.html#ADC)类。

Pin对象是通过制定具体I/O引脚的标识符来构造的。这个标识符可能是与端口或引脚编号相关的整数、字符串或元组。

**示例：**

```python
from machine import Pin

# create an output pin on pin #0
p0 = Pin(0, Pin.OUT)

# set the value low then high
p0.value(0)
p0.value(1)

# create an input pin on pin #2, with a pull up resistor
p2 = Pin(2, Pin.IN, Pin.PULL_UP)

# read and print the pin value
print(p2.value())

# reconfigure pin #0 in input mode with a pull down resistor
p0.init(p0.IN, p0.PULL_DOWN)

# configure an irq callback
p0.irq(lambda p:print(p))
```

## 构造函数

### `machine.Pin`

```python
class machine.Pin(id, mode=- 1, pull=- 1, *, value=None, drive=0, alt=- 1)
```

创建Pin对象，以访问关联给定`id`的引脚外设。若额外的参数被传入构造函数，则用于初始化该引脚。任何没有指定的参数，将保持之前的状态。

**参数描述：**

- `id` - 引脚标识，int型表示引脚编号，str型表示引脚名称，tuple型表示([port, pin],)；<a href="#label_pinmap">点此查看</a>引脚编号与物理引脚的映射关系。
- `mode` - 引脚输入输出模式，`Pin.IN`：输入模式，`Pin.OUT`：输出模式。

    <span id="label_pinmap">引脚编号与物理引脚的映射关系：</span>

    |引脚编号|引脚名称|物理引脚脚序|
    |---|---|---|
    |`Pin.GPIO0`|`"gpio0"`|`10`|
    |`Pin.GPIO0`|`"gpio0"`|`10`|
    |`Pin.GPIO0`|`"gpio0"`|`10`|

## 方法

### `Pin.value`

```python
Pin.value([x])
```

该方法用于设置或读取引脚电平，取决于参数`x`是否提供。

**参数描述：**

- `x` - 提供该参数，用于设置引脚电平；`1` 表示设置引脚电平为高，`0`表示设置引脚电平为低。

**返回值描述：**

当参数`x`没有提供时，返回引脚电平；`1` 表示获取到的引脚电平为高，`0`表示获取到的引脚电平为低。

## 属性

### `Pin.attr1`

此处添加属性功能描述。

### `Pin.attr2`

此处添加属性功能描述。

## 常量

### `Pin.IN`

此处添加常量功能描述。

### `Pin.OUT`

此处添加常量功能描述。
