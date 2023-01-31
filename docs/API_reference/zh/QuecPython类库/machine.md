# `machine - 硬件相关功能

`machine`模块包含硬件相关的特定功能。大多数功能允许直接并且非严格地访问和控制系统硬件。如果使用不正确，可能会导致板级功能异常，甚至死机；极端条件下，可能会引起硬件损坏。

> machine模块内的函数或类方法的回调函数，应当被看做在中断上下文中执行，这在物理设备或虚拟设备中均适用。

**示例：**

```python
import machine
from micropython import const

GPIOA = const(0x48000000)
GPIO_BSRR = const(0x18)
GPIO_IDR = const(0x10)

# set PA2 high
machine.mem32[GPIOA + GPIO_BSRR] = 1 << 2

# read PA3
value = (machine.mem32[GPIOA + GPIO_IDR] >> 3) & 1
```

## 内存访问功能

本模块提供3个对象，用于原始内存访问。

### `machine.mem8`

读写8位内存。

### `machine.mem16`

读写16位内存。

### `machine.mem32`

读写32位内存。

<br>
使用脚标[...]来索引这些对象的内存。请注意，无论被访问的内存有多大，地址是按照字节访问的。

**示例：**

```python
import machine
from micropython import const

GPIOA = const(0x48000000)
GPIO_BSRR = const(0x18)
GPIO_IDR = const(0x10)

# set PA2 high
machine.mem32[GPIOA + GPIO_BSRR] = 1 << 2

# read PA3
value = (machine.mem32[GPIOA + GPIO_IDR] >> 3) & 1
```

## 复位相关功能

### `machine.reset`

```python
machine.reset()
```

以类似于按下外部复位按键的方式复位设备。

### `machine.soft_reset`

```python
machine.soft_reset()
```

复位虚拟机解释器，删除所有的Python对象并且复位Python的堆内存。

## 中断相关功能

以下函数允许控制中断。某些系统需要中断正常运行，因此长时间禁用它们可能会破坏核心功能，例如看门狗定时器可能会意外触发。中断只应在最短时间内禁用，然后重新启用，恢复到以前的状态。例如：

```python
import machine

# Disable interrupts
state = machine.disable_irq()

# Do a small amount of time-critical work here

# Enable interrupts
machine.enable_irq(state)
```

### `machine.disable_irq`

```python
machine.disable_irq()
```

禁用中断请求。返回此前的中断状态。此返回值应传递给`enable_irq()`函数，以还原调用`disable_irq()`之前的中断状态。

### `machine.enable_irq`

```python
machine.enable_irq(state)
```

启用中断请求。`state`参数应该是最近一次调用`disable_irq()`函数时的返回值。

## 常量

### `machine.IDLE`

此处添加描述。

### `machine.SLEEP`

此处添加描述。

### `machine.DEEPSLEEP`

此处添加描述。

## Classes

- [class Pin – 控制I/O引脚](./machine.Pin.md)
- [class Signal – 控制和感知外部I/O设备](./machine.Signal.md)
- [class ADC – 模数转换](./machine.ADC.md)
- [class ADCBlock – 控制ADC外设](./machine.ADCBlock.md)
- [class PWM – 脉冲宽度调制](./PWM.md)
- [class UART – 串口通信](./machine.UART.md)
- [class SPI – SPI通信 (主机功能)](./machine.SPI.md)
- [class I2C – I2C通信](./machine.I2C.md)
- [class I2S – I2S音频协议](./machine.I2S.md)
- [class RTC – 实时时钟](./machine.RTC.md)
- [class Timer – 硬件定时器](./machine.Timer.md)
- [class WDT – 看门狗定时器](./machine.WDT.md)
- [class SD – SD卡 (仅支持cc3200)](./machine.SD.md)
- [class SDCard – SD卡](./machine.SDCard.md)
