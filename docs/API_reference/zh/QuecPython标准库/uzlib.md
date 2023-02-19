

```
本文阐述了QuecPython的uzlib模块的用法，描述了uzlib模块最新版本的特性。
```

uzlib 模块解压缩用[DEFLATE算法](https://en.wikipedia.org/wiki/DEFLATE)压缩的二进制数据 （通常在zlib库和gzip存档器中使用）。该模块实现相应CPython模块的子集，更多信息请参阅阅CPython文档：[zlib](https://docs.python.org/3.5/library/zlib.html#module-zlib)


> 注意：1.压缩尚未实现。2.解压缩前，应检查模块内可使用的空间，确保有足够空间解压文件。


## 构造函数

### `uzlib.decompress`

```python
uzlib.decompress(data, wbits=0, bufsize=0)
```

返回解压后的 bytes 对象。`wbits`是解压时使用的DEFLATE字典窗口大小（8-15，字典大小是`wbits`值的2的幂）。如果该值为正，则假定`data`为zlib流（带有zlib标头），如果为负，则假定为原始的DEFLATE流。`bufsize`参数是为了与CPython兼容，将被忽略。


### `uzlib.DecompIO`

```python
class uzlib.DecompIO(stream, wbits=0)
```

创建一个`stream`装饰器，该装饰器允许在另一个流中透明地压缩数据。这允许处理数据大于可用堆大小的压缩流。wbits的值除了上面所述的值以外，还可以取值24..31（16 + 8..15），这表示输入流具有gzip标头。

