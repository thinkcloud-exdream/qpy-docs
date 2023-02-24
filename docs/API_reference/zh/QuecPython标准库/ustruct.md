
# ustruct - 打包和解压原始数据类型

模块功能：`ustruct`模块实现相应CPython模块的子集。更多信息请参阅阅CPython文档：[struct](https://docs.python.org/3/library/struct.html)


## 格式字符串

格式字符串是用来在打包和解包数据时指定预期布局的机制。 其使用指定被打包/解包数据类型的`格式字符`进行构建。 此外，还有一些特殊字符用来控制`字节顺序`，`大小`和`对齐方式`。


### **字节顺序，大小和对齐方式**

默认情况下，C类型以机器的本机格式和字节顺序表示，并在必要时通过跳过填充字节来正确对齐（根据C编译器使用的规则）。根据下表，格式字符串的第一个字符可用于指示打包数据的字节顺序，大小和对齐方式：

| Character | Byte order             | Size     | Alignment |
| --------- | ---------------------- | -------- | --------- |
| `@`       | native                 | native   | native    |
| `=`       | native                 | standard | none      |
| `<`       | little-endian          | standard | none      |
| `>`       | big-endian             | standard | none      |
| `!`       | network (= big-endian) | standard | none      |

> 如果第一个字符不是其中之一，则假定为 '@' 。


### **格式化字符表**

| Format | C Type               | Python type | Standard size |
| ------ | -------------------- | ----------- | ------------- |
| `x`    | `pad byte`           | no value    |               |
| `c`    | `char`               | bytes of length 1 | 1       |
| `b`    | `signed char`        | integer     | 1             |
| `B`    | `unsigned char`      | integer     | 1             |
| `?`    | `_Bool`              | bool        | 1             |
| `h`    | `short`              | integer     | 2             |
| `H`    | `unsigned short`     | integer     | 2             |
| `i`    | `int`                | integer     | 4             |
| `I`    | `unsigned int`       | integer     | 4             |
| `l`    | `long`               | integer     | 4             |
| `L`    | `unsigned long`      | integer     | 4             |
| `q`    | `long long`          | integer     | 8             |
| `Q`    | `unsigned long long` | integer     | 8             |
| `n`    | `ssize_t`            | integer     |               |
| `N`    | `size_t`             | integer     |               |
| `e`    |                      | float       | 2             |
| `f`    | `float`              | float       | 4             |
| `d`    | `double`             | float       | 8             |
| `s`    | `char[]`             | bytes       |               |
| `p`    | `char[]`             | bytes       |               |
| `P`    | `void *`             | integer     | 4             |


## `ustruct`方法

### `ustruct.calcsize`

```python
ustruct.calcsize(fmt)
```

返回存放 `fmt` 需要的字节数。

**参数描述：**

- `fmt` - 格式字符的类型，详情见上文格化式字符表

**示例：**

```python
>>> import ustruct
>>> ustruct.calcsize('i')
4
>>> ustruct.calcsize('f')
4
>>> ustruct.calcsize('d')
8
```



### `ustruct.pack`

```python
ustruct.pack(fmt, v1, v2, ...)
```

按照格式字符串 `fmt` 压缩参数v1、 v2、…。

**参数描述：**

- `fmt` - 格式字符的类型，详情见上文格化式字符表

**返回值描述：**

- 返回参数编码后的字节对象。



### `ustruct.unpack`

```python
ustruct.unpack(fmt, data)
```

根据格式化字符串 `fmt` 对数据进行解压，返回值为一个元组。

**参数描述：**

- `fmt` - 格式字符的类型，详情见上文格化式字符表
- `data` - 要进行解压的数据

**返回值描述：**

- 返回包含解压值的元组(即使只包含一个项)。

**示例：**

```python
>>> import ustruct
>>> ustruct.pack('ii', 7, 9)  #打包两个整数
b'\x07\x00\x00\x00\t\x00\x00\x00'
>>> ustruct.unpack('ii', b'\x07\x00\x00\x00\t\x00\x00\x00')  #解压两个整数
(7, 9)
```



### `ustruct.pack_into`

```python
ustruct.pack_into(fmt, buffer, offset, v1, v2, ...)
```

根据格式字符串`fmt`将值v1、v2、 …打包到从`offset`开始的缓冲区中。从缓冲区的末尾算起，`offset`可能为负。

**参数描述：**

- `fmt` - 格式字符的类型，详情见上文格化式字符表
- `buffer` - 可写数据缓冲区
- `offset` - 写入的起始位置



### `ustruct.unpack_from`

```python
ustruct.unpack_from(fmt, data, offset=0)
```

根据格式化字符串 `fmt` 解析从 `offest` 开始的数据解压，从缓冲区末尾开始计数的偏移量可能为负值。

**参数描述：**

- `fmt` - 格式字符的类型，详情见上文格化式字符表
- `data` - 数据缓冲区(缓冲区大小以字节为单位)
- `offset` - 解压的起始位置

**返回值描述：**

- 返回解压值的元组(即使只包含一个项)。
