    本章对 QuecPython 标准库进行整体的叙述，每个模块的具体功能描述，请查看下文中相应的链接。

# QuecPython 标准库

> - QuecPython 提供了内置模块，这些模块反映了 Python 标准库（例如 `os`，`time`），以及 QuecPython 特定的模块（例如 `bluetooth`，`machine`）。<br><br>
> - 大多数标准库模块实现了等效的 Python 模块，并在少数情况下提供一些特定于 QuecPython 的扩展模块（例如`array`，`os`）。<br><br>
> - 为了允许扩展，内置模块可以从加载到设备上的 Python 代码扩展而来。

本文描述了 QuecPython 内置的模块（函数和类库）。

通过在REPL上输入以下代码，以查看所有可被导入的内置库：

```python
help('modules')
```

## QuecPython 标准库列表

- [`uos` - 基本系统服务](./uos.md)
- [`gc` - 内存碎片回收](./gc.md)
- [`ubinascii` - 二进制与ASCII转换](./ubinascii.md)
- [`ucollections` - 集合和容器类型](./ucollections.md)
- [`urandom` - 生成随机数](./urandom.md)
- [`...`](./....md)

<!--参考https://python.quectel.com/wiki/#/zh-cn/api/pythonStdlib进行补充-->
