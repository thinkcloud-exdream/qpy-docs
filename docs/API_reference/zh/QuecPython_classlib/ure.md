# ure - 正则表达式

该模块通过正则表达式匹配数据。

>目前支持的操作符较少，部分操作符暂不支持。

**示例：**

```python
import ure

res = '''
$GNRMC,133648.00,A,3149.2969,N,11706.9027,E,0.055,,311020,,,A,V*18
$GNGGA,133648.00,3149.2969,N,11706.9027,E,1,24,1.03,88.9,M,,M,,*6C
$GNGLL,3149.2969,N,11706.9027,E,133648.00,A,A*7A
$GNGSA,A,3,31,26,11,194,27,195,08,09,03,193,04,16,1.41,1.03,0.97,1*31
'''

r = ure.search("GNGGA(.+?)M", res)
print(r.group(0))
```

## 编译并生成正则表达式对象

### `ure.compile`

```python
ure.compile(regex)
```

用于编译正则表达式，生成一个正则表达式对象，供 match() 和 search() 这两个函数使用。

**参数描述：**

- `regex` - 正则表达式，字符串类型。


## 匹配

### `ure.match`

```python
ure.match(regex, string)
```

将正则表达式对象 与 string 匹配，匹配通常从字符串的起始位置进行。

**参数描述：**

- `regex` - 正则表达式，字符串类型。
- `string` - 需要匹配的字符串数据。

**返回值描述：**

- 匹配成功返回一个匹配的对象，否则返回None。

## 查找

### `ure.search`

```python
ure.search(regex, string)
```

扫描整个字符串并返回第一个成功的匹配。

**参数描述：**

- `regex` - 正则表达式，字符串类型。
- `string` - 需要查找的字符串数据。

**返回值描述：**

- 匹配成功返回一个匹配的对象，否则返回None。


## 匹配单个字符串

### `match.group`

```python
match.group(index)
```

匹配 match() 和 serach() 方法返回的对象。

**参数描述：**

- `index` - 整型，正则表达式中，group()用来提出分组截获的字符串, index=0返回整体，根据编写的正则表达式进行获取，当分组不存在时会抛出异常。

**返回值描述：**

- 返回匹配的整个表达式的字符串。


## 常量

### 支持的操作符
- `‘.’` - 字符类型，匹配任意字符。
- `‘[]’` - 字符类型，匹配字符集合，支持单个字符和一个范围，包括负集。
- `‘^’` - 字符类型，匹配字符串的开头。
- `‘$’` - 字符类型，匹配字符串的结尾。
- `‘?’` - 字符类型，匹配零个或前面的子模式之一。
- `‘*’` - 字符类型，匹配零个或多个先前的子模式。
- `‘+’` - 字符类型，匹配一个或多个先前的子模式。
- `‘??’` - 字符类型，非贪婪版本的 ? ，匹配0或1。
- `‘*?’` - 字符类型，非贪婪版本的*，匹配零个或多个。
- `‘+?’` - 字符类型，非贪婪版本的+，匹配一个或多个。
- `‘\|’` - 字符类型，匹配该操作符的左侧子模式或右侧子模式。
- `‘\d’` - 字符类型，数字匹配。
- `‘\D’` - 字符类型，非数字匹配。
- `‘\s’` - 字符类型，匹配空格。
- `‘\S’` - 字符类型，匹配非空格。
- `‘\w’` - 字符类型，匹配”单词字符” (仅限ASCII)。
- `‘\W’` - 字符类型，匹配非“单词字符”（仅限ASCII）。


### 不支持的操作符
- `‘{m,n}’` - 重复次数。
- `‘(?P<name>...)’` - 命名组。
- `‘(?:...)’` - 非捕获组。
- `‘\b’` - 更高级的断言。
- `‘\B’` - 更高级的断言。
- `‘\r’` - 特殊字符转义，改用Python自己的转义。
- `‘\n’` - 特殊字符转义，改用Python自己的转义。
