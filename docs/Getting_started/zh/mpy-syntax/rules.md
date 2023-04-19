# 编写 MicroPython 代码的基本规范

MicroPython 是一种基于 Python 的轻量级和高效的编程语言，它可以运行在微控制器和受限制的系统上，提供了丰富的功能和灵活性。MicroPython 实现了 Python 3.4 的核心语法，以及部分 Python 3.5 及更高版本的特性，如异步编程等。MicroPython 还提供了一些独有的特性，如内置模块、原生代码等。

要编写高质量的 MicroPython 代码，在掌握 MicroPython 的语法和特性之前，需要了解和遵循一些基本的规范和原则，以提高代码的可读性、可维护性和可扩展性。本篇将介绍编写 MicroPython 代码的基本规范。

## 格式

格式是指编写代码时遵循的一些规则和约定，比如缩进、空行、代码风格等。格式对于代码的可读性和可维护性非常重要，也是编程的基本素养之一。在很多时候，格式不会影响代码的功能和执行结果，但会影响代码的美观和规范。

### 缩进

缩进是指在代码的每一行前面添加一定数量的空格或制表符（Tab 键），以表示代码之间的层次关系。在 MicroPython 中，缩进是必须的，因为它决定了代码块（block）的范围。代码块是指一组有逻辑关系的语句，通常用于表示条件判断、循环、函数等结构。在 MicroPython 中，同一个代码块内的语句必须有相同的缩进量，而不同代码块之间的缩进量必须不同。一般来说，每个缩进量为 4 个空格或一个制表符。

例如，以下代码使用了缩进来表示不同的代码块：

```python
# 这是一个 if 语句，用于判断 x 是否大于 0
# if 语句是一种条件语句，用于根据条件执行不同的操作
# if 语句的格式为：if 条件: 代码块
# 如果条件为真（True），则执行冒号后面的代码块
# 如果条件为假（False），则跳过冒号后面的代码块
if x > 0:
    # 这是 if 语句的代码块，用于打印 x 是正数
    # 注意这一行前面有 4 个空格，表示它属于 if 语句的代码块
    print("x is positive")
else:
    # 这是 else 语句的代码块，用于打印 x 是负数或零
    # else 语句是 if 语句的可选部分，用于处理条件为假时的情况
    # else 语句的格式为：else: 代码块
    # 注意 else 前面没有空格，表示它和 if 语句处于同一层次
    print("x is negative or zero")
```

注意：如果缩进不正确，会导致语法错误（SyntaxError），所以要注意保持缩进的一致性和正确性。

例如，以下代码就会产生缩进错误，因为第二个 print 语句没有和第一个 print 语句对齐：

```python
# 这是一个错误示范，会导致 SyntaxError: unexpected indent
if x > 0:
    print("x is positive")
  print("x is also greater than zero")
```

另外，以下代码也会产生缩进错误，因为混用了空格和制表符来缩进：

```python
# 这是一个错误示范，会导致 SyntaxError: inconsistent use of tabs and spaces in indentation
if x > 0:
    print("x is positive") # 这一行使用了 4 个空格来缩进
else:
 print("x is negative or zero") # 这一行使用了一个制表符来缩进
```

在 MicroPython 中，建议使用空格而不是制表符来缩进，因为空格的显示更稳定和一致，而制表符的显示可能会因为不同的编辑器或 IDE 而有所差异。如果你不小心混用了空格和制表符，你可以使用一些工具来转换或统一它们。现代的很多 IDE 都包含了类似的代码格式化功能。

### 空行

空行是指在代码中插入一行或多行没有任何内容的行，以增加代码的可读性和美观性。在 MicroPython 中，空行不会影响代码的功能和执行结果，但会让代码看起来更清晰和整洁。一般来说，在不同的函数、类或模块之间添加空行，可以区分它们之间的逻辑关系。在一个函数、类或模块内部，也可以根据需要添加空行，以分隔不同的功能或逻辑。

例如，以下代码使用了空行来增加可读性：

```python
# 这是一个定义函数的语句，用于计算两个数的平方和
# 函数是一种可以重复使用的代码段，用于完成特定的任务
# 函数可以接收参数（输入）并返回结果（输出）
# 函数可以通过 def 关键字来定义
# def 关键字后面跟着函数名和括号，括号里面是参数列表
# def 关键字后面还要跟着一个冒号，表示开始定义函数体（函数内部的代码）
def square_sum(a, b):
    # 这是函数内部的第一个语句，用于计算 a 的平方
    # 注意这一行前面有 4 个空格，表示它属于函数体
    a_squared = a ** 2

    # 这是函数内部的第二个语句，用于计算 b 的平方
    # 注意这一行前面也有 4 个空格，表示它和上一行属于同一个代码块
    b_squared = b ** 2

    # 这是函数内部的第三个语句，用于返回 a 和 b 的平方和
    # return 关键字用于表示函数的返回值，即函数执行后的结果
    # return 关键字后面跟着要返回的值或表达式
    return a_squared + b_squared

# 这是一个空行，用于分隔函数定义和函数调用

# 这是一个调用函数的语句，用于打印 3 和 4 的平方和
# 函数可以通过函数名和括号来调用，括号里面是实际传入的参数值
# 函数调用后会返回一个值，可以用 print 函数来打印这个值
print(square_sum(3, 4))
```

注意：空行不要过多或过少，否则会影响代码的美观和规范。

例如，以下代码就使用了过多的空行，会让代码看起来松散和冗余：

```python
# 这是一个错误示范，使用了过多的空行

def square_sum(a, b):


    a_squared = a ** 2


    b_squared = b ** 2


    return a_squared + b_squared



print(square_sum(3, 4))
```

### 代码风格和规范

代码风格是指编写代码时遵循的一些习惯和偏好，比如命名、注释、空格等。代码风格对于代码的可读性和可维护性也非常重要，也是编程的基本素养之一。代码风格不会影响代码的功能和执行结果，但会影响代码的一致性和标准化。

为了让不同的程序员能够更好地协作和交流，Python 社区制定了一些公认的代码风格和规范，比如 PEP 8。PEP 8 是 Python Enhancement Proposal（Python 增强提案）的第 8 号文档，它详细地描述了如何编写优雅和清晰的 Python 代码。PEP 8 涵盖了命名、注释、空格、换行、括号等方面的规则和建议，是 Python 程序员的必读参考资料。

MicroPython 是 Python 3 的一个子集，因此 PEP 8 也适用于 MicroPython。虽然 PEP 8 不是强制性的，但是遵循 PEP 8 可以让你的代码更容易被其他人理解和接受，也可以提高你的编程水平和信誉。你可以在 [Python 官网](https://www.python.org/dev/peps/pep-0008/) 查看 PEP 8 的完整内容：

除了 PEP 8 之外，你还可以参考一些其他的代码风格和规范，比如 Google Python Style Guide（谷歌 Python 风格指南）或 The Hitchhiker’s Guide to Python（Python 之旅指南）。这些资料都可以在网上找到，你可以根据自己的需要和喜好选择合适的风格和规范。

注意：代码风格和规范不是一成不变的，而是随着时间和技术的发展而不断更新和改进的。你应该保持对最新的代码风格和规范的关注和学习，同时也要灵活地适应不同的项目和环境。

## 注释

注释是指在代码中添加一些文字说明，以帮助理解和维护代码。在 MicroPython 中，注释是不会被执行的，只是为了方便程序员或其他阅读者阅读和理解代码。注释可以用于说明代码的功能、目的、逻辑、算法等方面，也可以用于调试或测试代码。

在 MicroPython 中，有两种常见的注释方式：单行注释和多行注释。

### 单行注释

单行注释是指在一行代码的末尾或者一行空白处添加一个井号（#），后面跟着要注释的内容。单行注释只对该行有效，不会影响其他行。

例如，以下代码使用了单行注释来说明变量的含义和函数的功能：

```python
# 这是一个单行注释，用于说明这个程序的目的
# 这个程序用于计算两个数的平方和

# 定义两个变量 a 和 b，分别赋值为 3 和 4
a = 3 # 这是一个单行注释，用于说明变量 a 的值
b = 4 # 这是一个单行注释，用于说明变量 b 的值

# 定义一个函数 square_sum，用于计算两个数的平方和
def square_sum(a, b): # 这是一个单行注释，用于说明函数的参数
    # 这是一个单行注释，用于说明函数内部的逻辑
    # 计算 a 的平方并赋值给 a_squared
    a_squared = a ** 2
    # 计算 b 的平方并赋值给 b_squared
    b_squared = b ** 2
    # 返回 a 和 b 的平方和
    return a_squared + b_squared

# 调用函数 square_sum，并打印返回值
print(square_sum(a, b)) # 这是一个单行注释，用于说明函数的调用和输出
```

### 多行注释

多行注释是指在多行代码之前或之间添加三对引号（`"""` 或 `'''`），中间跟着要注释的内容。多行注释可以跨越多行，直到遇到另一对引号结束。

例如，以下代码使用了多行注释来说明模块的作者和版本信息：

```python
"""
这是一个多行注释，用于说明模块的作者和版本信息
作者：张三
版本：1.0
日期：2023-04-19
"""

# 这是一个单行注释，用于说明这个程序的目的
# 这个程序用于计算两个数的平方和

# 定义两个变量 a 和 b，分别赋值为 3 和 4
a = 3 
b = 4 

# 定义一个函数 square_sum，用于计算两个数的平方和
def square_sum(a, b): 
    # 计算 a 的平方并赋值给 a_squared
    a_squared = a ** 2
    # 计算 b 的平方并赋值给 b_squared
    b_squared = b ** 2
    # 返回 a 和 b 的平方和
    return a_squared + b_squared

# 调用函数 square_sum，并打印返回值
print(square_sum(a, b)) 
```

### 注释的使用注意事项

在编写注释时，要注意以下几点：

- 注释要简洁明了，不要过长或过短。
- 注释要与代码保持一致，不要出现与代码相矛盾或过时的情况。
- 注释要适当地分布在代码中，不要过多或过少。过多的注释会影响代码的可读性和美观性，过少的注释会影响代码的理解和维护。
- 注释要遵循一定的格式和规范，以便于统一和标准化。例如，可以使用 PEP 8 或其他代码风格指南中关于注释的规则和建议。

## 关键字

关键字是指在 MicroPython 中具有特殊含义和功能的单词，它们是 MicroPython 语言的基本组成部分。关键字不能用作其他用途，比如变量名、函数名或类名等，否则会引发语法错误。例如，以下代码就是错误的，因为它试图把关键字 if 作为变量名：

```python
# 错误示例：使用关键字作为变量名
if = 1 # SyntaxError: invalid syntax
```

### 关键字有哪些？

要查看 MicroPython 中有哪些关键字，可以直接参考以下列表，它包含了 MicroPython 中所有的关键字（按字母顺序排列）：

- False
- None
- True
- and
- as
- assert
- async
- await
- break
- class
- continue
- def
- del
- elif
- else
- except
- finally
- for
- from
- global
- if
- import
- in
- is
- lambda
- nonlocal
- not
- or
- pass
- raise
- return
- try
- while
- with
- yield

如果你想判断一个字符串是否是关键字，你可以使用一个简单的方法：尝试把它作为变量名赋值，如果出现语法错误，说明它是关键字；如果没有出现语法错误，说明它不是关键字。以下代码就是使用这个方法的示例：

```python
# 使用赋值语句判断关键字

try: # 尝试执行以下代码块
    if = 1 # 把 "if" 作为变量名赋值，这会引发语法错误，因为 "if" 是关键字
except SyntaxError: # 如果捕获到语法错误异常，执行以下代码块
    print("if is a keyword") # 打印 "if is a keyword"

try: # 尝试执行以下代码块
    foo = 1 # 把 "foo" 作为变量名赋值，这不会引发语法错误，因为 "foo" 不是关键字
except SyntaxError: # 如果捕获到语法错误异常，执行以下代码块（这里不会执行）
    print("foo is a keyword") # 打印 "foo is a keyword"
else: # 如果没有捕获到语法错误异常，执行以下代码块（这里会执行）
    print("foo is not a keyword") # 打印 "foo is not a keyword"
```

### 关键字的作用和特点

关键字在 MicroPython 中扮演着不同的角色，有些是用来定义数据类型和值的，如 False、None、True；有些是用来控制程序流程和逻辑的，如 if、else、for、while、break、continue 等；有些是用来定义函数和类的，如 def、class、return、yield 等；有些是用来处理异常和错误的，如 try、except、finally、raise 等；有些是用来实现异步编程的，如 async、await 等；还有一些是用来实现其他功能的，如 import、global、nonlocal、pass 等。

关键字在 MicroPython 中具有以下特点：

- 关键字都是小写字母，不区分大小写。
- 关键字不能被重新赋值或修改。
- 关键字不能被覆盖或隐藏，即使在不同的作用域中也不能使用相同的关键字作为标识符。
- 关键字在不同的上下文中可能有不同的含义和功能，需要根据具体情况理解和使用。

以下是一些使用关键字的示例：

```python
# 使用 False、None 和 True 表示布尔值和空值
a = False # a 是一个布尔值，表示假
b = None # b 是一个空值，表示没有任何对象
c = True # c 是一个布尔值，表示真

# 使用 if、else 和 elif 控制条件分支
x = 10 # x 是一个整数
if x > 0: # 如果 x 大于 0
    print("x is positive") # 打印 "x is positive"
elif x < 0: # 否则如果 x 小于 0
    print("x is negative") # 打印 "x is negative"
else: # 否则
    print("x is zero") # 打印 "x is zero"

# 使用 for 和 while 循环遍历序列或执行重复操作
l = [1, 2, 3] # l 是一个列表
for i in l: # 对于 l 中的每个元素 i
    print(i) # 打印 i

n = 5 # n 是一个整数
while n > 0: # 当 n 大于 0 时
    print(n) # 打印 n
    n -= 1 # n 减 1

# 使用 break 和 continue 控制循环的中断和继续
m = 10 # m 是一个整数
while True: # 无限循环
    print(m) # 打印 m
    m -= 1 # m 减 1
    if m == 5: # 如果 m 等于 5
        break # 中断循环
    if m % 2 == 0: # 如果 m 是偶数
        continue # 跳过本次循环的剩余部分，继续下一次循环

# 使用 def 和 class 定义函数和类
def add(a, b): # 定义一个函数 add，接受两个参数 a 和 b
    return a + b # 返回 a 和 b 的和

class Point: # 定义一个类 Point
    def __init__(self, x, y): # 定义类的初始化方法，接受两个参数 x 和 y
        self.x = x # 把 x 赋值给类的属性 x
        self.y = y # 把 y 赋值给类的属性 y

# 使用 try、except、finally 和 raise 处理异常和错误
try: # 尝试执行以下代码块
    print(1 / 0) # 打印 1 除以 0，这会引发 ZeroDivisionError 异常
except ZeroDivisionError: # 如果捕获到 ZeroDivisionError 异常，执行以下代码块
    print("Cannot divide by zero") # 打印 "Cannot divide by zero"
finally: # 无论是否捕获到异常，都执行以下代码块
    print("Done") # 打印 "Done"

def foo(): # 定义一个函数 foo
    raise ValueError("Something went wrong") # 抛出一个 ValueError 异常，附带一条错误信息

foo() # 调用 foo 函数，这会引发 ValueError 异常

# 使用 async 和 await 实现异步编程
import uasyncio as asyncio # 导入 uasyncio 模块，提供异步编程的功能

async def hello(): # 定义一个异步函数 hello
    print("Hello") # 打印 "Hello"
    await asyncio.sleep(1) # 等待 1 秒，让出控制权给其他异步任务
    print("World") # 打印 "World"

async def main(): # 定义一个异步函数 main
    await asyncio.gather(hello(), hello()) # 等待两个 hello 函数并发执行

asyncio.run(main()) # 运行 main 函数，输出 "Hello\nHello\nWorld\nWorld"

# 使用 import、global 和 nonlocal 实现模块导入和变量作用域的控制
import math # 导入 math 模块，提供数学相关的功能

print(math.pi) # 打印 math 模块中的 pi 常量，输出 3.141592653589793

x = 1 # 定义一个全局变量 x，赋值为 1

def foo(): # 定义一个函数 foo
    global x # 声明 x 是全局变量
    x = 2 # 修改全局变量 x 的值为 2

foo() # 调用 foo 函数
print(x) # 打印全局变量 x 的值，输出 2

def bar(): # 定义一个函数 bar
    x = 3 # 定义一个局部变量 x，赋值为 3
    def baz(): # 定义一个嵌套函数 baz
        nonlocal x # 声明 x 是非局部变量，即 bar 函数中的局部变量 x
        x = 4 # 修改非局部变量 x 的值为 4
    baz() # 调用 baz 函数
    print(x) # 打印非局部变量 x 的值，输出 4

bar() # 调用 bar 函数
```

## 标识符

标识符是指在 MicroPython 中用来命名变量、函数、类、模块等对象的名称，它们是由程序员自己定义的。标识符可以由字母、数字、下划线组成，但不能以数字开头。以下代码展示了一些合法和不合法的标识符的示例：

```python
# 合法的标识符

name = "Alice" # 定义一个变量 name，赋值为 "Alice"
age = 18 # 定义一个变量 age，赋值为 18
def hello(): # 定义一个函数 hello
    print("Hello, world!") # 打印 "Hello, world!"
class Person: # 定义一个类 Person
    pass # 空语句，表示什么也不做
import math # 导入 math 模块
```

```python
# 不合法的标识符

1st = "first" # SyntaxError: invalid syntax，不能以数字开头
if = 1 # SyntaxError: invalid syntax，不能使用关键字
my-name = "Bob" # SyntaxError: can't assign to operator，不能使用除下划线以外的特殊字符
```

### 标识符的命名规则

在 MicroPython 中，有一些命名规则需要遵守，否则可能会引发错误或者造成混淆。以下是一些常见的命名规则：

- 标识符不能与关键字重名，否则会引发语法错误。
- 标识符区分大小写，即大写字母和小写字母是不同的。例如，name 和 Name 是两个不同的标识符。
- 标识符不能包含空格或者其他特殊字符（如标点符号），否则会引发语法错误。
- 标识符不能以数字开头，否则会引发语法错误。
- 标识符不能与内置函数或模块重名，否则会覆盖或隐藏它们。例如，如果你定义了一个变量叫 print，那么你就无法使用内置的 print 函数了。

以下是一些遵守和违反命名规则的示例：

```python
# 遵守命名规则的示例

x = 10 # 合法的变量名

y = x + 1 # 合法的表达式
z = x * y # 合法的表达式

def add(a, b): # 合法的函数名和参数名
    return a + b # 合法的返回语句

print(z) # 合法的函数调用
```

```python
# 违反命名规则的示例

from = "China" # SyntaxError: invalid syntax，使用了关键字作为变量名
Name = "Alice" # 不会引发错误，但是容易与 name 混淆
my name = "Bob" # SyntaxError: invalid syntax，使用了空格作为变量名
my-name = "Bob" # SyntaxError: can't assign to operator，使用了特殊字符作为变量名
1st = "first" # SyntaxError: invalid syntax，以数字开头作为变量名
print = "Hello" # 不会引发错误，但是覆盖了内置的 print 函数
```

### 命名风格和建议

除了遵守命名规则外，在 MicroPython 中还有一些命名风格和建议可以参考，以提高代码的可读性和一致性。以下是一些常见的命名风格和建议：

- 使用有意义的单词作为标识符，避免使用无意义或者过于简单的单字母。例如，使用 name 而不是 n，使用 temperature 而不是 t，使用 is_prime 而不是 p 等。
- 使用下划线分隔单词，以提高可读性。例如，使用 my_name 而不是 myname，使用 get_length 而不是 getlength 等。
- 使用不同的命名风格来区分不同类型的对象。例如，使用小写字母和下划线来命名变量、函数和模块，如 x、add、math 等；使用首字母大写来命名类，如 Point、Person 等；使用全大写字母和下划线来命名常量，如 PI、MAX_VALUE 等。
- 避免使用可能引起歧义或者冲突的标识符。例如，不要使用 l、O 或者 I 作为变量名，因为它们可能与数字 1 或者 0 混淆；不要使用内置函数或模块的名称作为标识符，因为它们可能覆盖或隐藏原有的功能。

以下是一些遵守和违反命名风格和建议的示例：

```python
# 遵守命名风格和建议的示例

name = "Alice" # 使用有意义的单词作为变量名
age = 18 # 使用小写字母和下划线作为变量名

def get_area(width, height): # 使用有意义的单词和下划线作为函数名和参数名
    return width * height # 使用有意义的表达式作为返回值

class Rectangle: # 使用首字母大写作为类名
    def __init__(self, width, height): # 使用有意义的单词和下划线作为方法名和参数名
        self.width = width # 使用有意义的单词和下划线作为属性名
        self.height = height # 使用有意义的单词和下划线作为属性名

PI = 3.14 # 使用全大写字母和下划线作为常量名
```

```python
# 违反命名风格和建议的示例

n = "Bob" # 使用无意义或者过于简单的单字母作为变量名
t = 20 # 使用无意义或者过于简单的单字母作为变量名

def f(x): # 使用无意义或者过于简单的单字母作为函数名和参数名
    return x * x # 使用无意义或者过于简单的表达式作为返回值

class point: # 使用小写字母作为类名
    def __init__(self, x, y): # 使用无意义或者过于简单的单字母作为方法名和参数名
        self.x = x # 使用无意义或者过于简单的单字母作为属性名
        self.y = y # 使用无意义或者过于简单的单字母作为属性名
        
max_value = 100 # 使用小写字母和下划线作为常量名

l = [1, 2, 3] # 使用可能与数字 1 混淆的单字母 l 作为变量名
O = "Hello" # 使用可能与数字 0 混淆的单字母 O 作为变量名
I = "World" # 使用可能与数字 1 混淆的单字母 I 作为变量名

print = "Hello" # 使用内置函数 print 的名称作为变量名
math = 10 # 使用内置模块 math 的名称作为变量名
```
