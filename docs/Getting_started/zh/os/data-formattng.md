# 数据格式转换

在Python中，处理二进制数据是非常常见的操作。MicroPython中提供了两个模块，ustruct和ubinascii，用于对二进制数据进行打包、解包、编码和解码等处理。本文将介绍ustruct和ubinascii模块的功能，并提供一些使用示例。

## ustruct

ustruct模块是MicroPython中一个处理二进制数据的模块，可以将Python中的数据类型转换为二进制数据，也可以将二进制数据转换为Python中的数据类型。ustruct提供了**pack、unpack、calcsize、pack_into和unpack_from**五个函数。



### 1.1 ustruct支持的格式表

ustruct中支持的格式如下表：

| Format | C Type               | Python             | 字节数 |
| ------ | -------------------- | ------------------ | ------ |
| `x`    | pad byte             | no value           | 1      |
| `c`    | `char`               | string of length 1 | 1      |
| `b`    | `signed char`        | integer            | 1      |
| `B`    | `unsigned char`      | integer            | 1      |
| `?`    | `_Bool`              | bool               | 1      |
| `h`    | `short`              | integer            | 2      |
| `H`    | `unsigned short`     | integer            | 2      |
| `i`    | `int`                | integer            | 4      |
| `I`    | `unsigned int`       | integer or long    | 4      |
| `l`    | `long`               | integer            | 4      |
| `L`    | `unsigned long`      | long               | 4      |
| `q`    | `long long`          | long               | 8      |
| `Q`    | `unsigned long long` | long               | 8      |
| `f`    | `float`              | float              | 4      |
| `d`    | `double`             | float              | 8      |
| `s`    | `char[]`             | string             | 1      |
| `p`    | `char[]`             | string             | 1      |
| `P`    | `void *`             | long               |        |

注1.q和Q只在机器支持64位操作时有意思

注2.每个格式前可以有一个数字，表示个数

注3.s格式表示一定长度的字符串，4s表示长度为4的字符串，但是p表示的是pascal字符串

注4.P用来转换一个指针，其长度和机器字长相关

注5.最后一个可以用来表示指针类型的，占4个字节



### 1.2 ustruct对齐方式

为了同c中的结构体交换数据，还要考虑有的c或c++编译器使用了字节对齐，通常是以4个字节为单位的32位系统，故而ustruct根据本地机器字节顺序转换.可以用格式中的第一个字符来改变对齐方式.定义如下：

| Character | Byte order    | Size | Alignment       |
| :-------- | :------------ | :--- | :-------------- |
| @(默认)   | 本机          | 本机 | 本机,凑够4字节  |
| =         | 本机          | 标准 | none,按原字节数 |
| <         | 小端          | 标准 | none,按原字节数 |
| >         | 大端          | 标准 | none,按原字节数 |
| !         | network(大端) | 标准 | none,按原字节数 |




### 1.3 pack和unpack函数

pack函数将一个Python值的序列根据指定的格式（fmt）打包成一个字节串，而unpack函数将指定的格式字符串（fmt）和一个字节串解包成一个元组。

下面是一个使用pack和unpack函数的示例：

```python
import ustruct

buf = ustruct.pack('4sI', b'MPYN', 12345)
print(buf)  # 输出 b'MPYN\x39\x30\x01\x00'

s, i = ustruct.unpack('4sI', buf)
print(s, i)  # 输出 b'MPYN' 12345
```

在这个例子中，'4sI'表示使用4个字节的字符串和一个整数进行打包和解包。



### 1.4 calcsize函数

calcsize函数返回指定格式（fmt）的字节串所需要的长度。

下面是一个使用calcsize函数的示例：

```python
import ustruct

size = ustruct.calcsize('4sI')
print(size)  # 输出 8
```

在这个例子中，'4sI'表示使用4个字节的字符串和一个整数进行打包，所需长度为8个字节。



### 1.5 pack_into函数

pack_into函数将一个Python值的序列根据指定的格式（fmt）打包到一个指定的缓冲区（buffer）的指定偏移量（offset）处。

下面是一个使用pack_into函数的示例：

```python
import ustruct

buf = bytearray(8)
ustruct.pack_into('>hhl', buf, 0, 32767, -12345, 123456789)
print(buf)  # 输出 b'\x7f\xff\xcf\xc7\x80\x8d\x05\xcb'

```

在这个例子中，'>hhl'表示使用大端序，将一个16位整数、一个32位整数和一个32位有符号整数打包成一个字节串，并将它们放到buf的偏移量为0的位置。



### 1.6 unpack_from函数

unpack_from函数将指定的格式字符串（fmt）和一个字节串从指定偏移量（offset）处

开始处理二进制数据并解包成一个元组。

下面是一个使用unpack_from函数的示例：

```python
import ustruct

data = b'\x01\x02\x03\x04\x05\x06\x07\x08'
a, b = ustruct.unpack_from('HH', data, 2)
print(a, b)  # 输出 0x0302 0x0405

```

在这个例子中，'HH'表示使用两个16位无符号整数进行解包，unpack_from函数将字节串中从偏移量为2的位置开始的数据按照格式字符串解包成两个整数。



### 1.7 大小端测试

MicroPython在处理二进制数据时支持大小端，可以通过指定格式字符串来选择使用大端序（'>'）或小端序（'<'）进行打包和解包。

下面是一个使用大端序和小端序的示例：

```python
import ustruct

buf = ustruct.pack('>Hl', 32767, 123456789)
print(buf)  # 输出 b'\x7f\xff\x05\xcd\x15\xcd\x5b\x07'

s, i = ustruct.unpack('<Hl', buf)
print(s, i)  # 输出 258 123456789

```

在这个例子中，'>Hl'表示使用大端序，将一个16位整数和一个32位有符号整数打包成一个字节串，'<Hl'表示使用小端序，将同样的字节串解包成一个16位整数和一个32位有符号整数



### 1.8 总结

ustruct模块主要用于打包、解包、编码和解码二进制数据，支持大小端序。

它的主要函数有pack、unpack、calcsize、pack_into和unpack_from。其中pack函数将Python值的序列按照指定的格式打包成一个字节串，

> unpack函数将一个字节串解包成一个元组，
>
> calcsize函数返回指定格式的字节串所需的长度，
>
> pack_into函数将Python值的序列按照指定格式打包到指定的缓冲区中，
>
> unpack_from函数将一个字节串从指定偏移量开始解包成一个元组。

通过使用这些函数，可以方便地进行二进制数据的打包、解包和编码解码操作。



## ubinascii

ubinascii模块用于将二进制数据进行编码和解码。它提供了多种编码和解码方法，如十六进制编码和解码、Base64编码和解码等。



### 2.1 hexlify和unhexlify函数

hexlify函数将一个字节串编码成十六进制表示的字符串，unhexlify函数将一个十六进制表示的字符串解码成字节串。

下面是一个使用hexlify和unhexlify函数的示例：

```python
import ubinascii

data = b'\x01\x02\x03\x04\x05\x06\x07\x08'
hexstr = ubinascii.hexlify(data)
print(hexstr)  # 输出 b'0102030405060708'

bytearr = ubinascii.unhexlify(hexstr)
print(bytearr)  # 输出 b'\x01\x02\x03\x04\x05\x06\x07\x08'

```

在这个例子中，hexlify函数将字节串b'\x01\x02\x03\x04\x05\x06\x07\x08'编码成十六进制字符串b'0102030405060708'，unhexlify函数将十六进制字符串解码成字节串b'\x01\x02\x03\x04\x05\x06\x07\x08'。



### 2.2 b2a_base64和a2b_base64函数

b2a_base64函数将一个字节串编码成Base64表示的字符串，a2b_base64函数将一个Base64表示的字符串解码成字节串。

下面是一个使用b2a_base64和a2b_base64函数的示例：

```python
import ubinascii

data = b'\x01\x02\x03\x04\x05\x06\x07\x08'
base64str = ubinascii.b2a_base64(data)
print(base64str)  # 输出 b'AQIDBAUGBwg='

bytearr = ubinascii.a2b_base64(base64str)
print(bytearr)  # 输出 b'\x01\x02\x03\x04\x05\x06\x07\x08'

```

在这个例子中，b2a_base64函数将字节串b'\x01\x02\x03\x04\x05\x06\x07\x08'编码成Base64字符串b'AQIDBAUGBwg='，a2b_base64函数将Base64字符串解码成字节串b'\x01\x02\x03\x04\x05\x06\x07\x08'。



### 2.3 总结

ubinascii模块主要用于将二进制数据进行编码和解码。

它的主要函数有hexlify、unhexlify、b2a_base64和a2b_base64。

>其中hexlify函数将一个字节串编码成十六进制表示的字符串，
>
>unhexlify函数将一个十六进制表示的字符串解码成字节串，
>
>b2a_base64函数将一个字节串编码成Base64表示的字符串，
>
>a2b_base64函数将一个Base64表示的字符串解码成字节串。

通过使用这些函数，可以方便地进行二进制数据的编码和解码操作。