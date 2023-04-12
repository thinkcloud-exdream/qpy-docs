# 文件管理

本文主要介绍如何使用`QuecPython`的文件系统。

## POSIX API

在QuePython上操作文件可直接使用POSIX的接口进行开发

1. 打开文件

   ```py
   open(file, mode="r")
   ```

   - file: 文件路径(**在QuecPython里，用户文件路径在/usr下，所以用户创建读取文件都要在此目录下进行**)

   - mode: 打开模式，可选，默认为只读

     | 模式 | 描述                                                         |
     | ---- | ------------------------------------------------------------ |
     | w    | 以**只写**方式打开文件。如果该文件已存在则打开文件，并从开头开始编辑，**即原有内容会被删除**。如果该文件不存在，创建新文件。 |
     | r    | 以**只读**方式打开文件。文件的指针将会放在文件的开头。       |
     | w+   | 以**读写**方式打开文件。如果该文件已存在则打开文件，并从开头开始编辑，**即原有内容会被删除**。如果该文件不存在，创建新文件。 |
     | r+   | 以**读写**方式打开文件。该文件必须存在。文件的指针将会放在文件的开头。 |
     | wb   | 以**只写**方式打开**二进制**文件。如果该文件已存在则打开文件，并从开头开始编辑，**即原有内容会被删除**。如果该文件不存在，创建新文件。 |
     | rb   | 以**只读**方式打开**二进制**文件。文件的指针将会放在文件的开头。 |
     | wb+  | 以**读写**方式打开**二进制**文件。如果该文件已存在则打开文件，并从开头开始编辑，**即原有内容会被删除**。如果该文件不存在，创建新文件。 |
     | rb+  | 以**读写**方式打开**二进制**文件。该文件必须存在。文件的指针将会放在文件的开头。 |
     | a    | 打开一个文件用于**追加**。如果该文件已存在，文件指针将会放在文件的结尾，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。 |
     | a+   | 打开一个文件用于**读写**。如果该文件已存在，文件指针将会放在文件的结尾，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行读写。 |
     | ab   | 打开一个二进制文件用于**追加**。如果该文件已存在，文件指针将会放在文件的结尾，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。 |
     | ab+  | 打开一个二进制文件用于**读写**。如果该文件已存在，文件指针将会放在文件的结尾，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行读写。 |

2.  写入文件

   ```py
   write(str)
   ```

   - ​	str: 要写入的数据

   该函数返回成功写入的字符串长度

3. 读取文件

   ```py
   read(size)
   ```

   - ​	size:要读取的长度，单位字节

   该函数返回成功读到的数据

4. 读取文件的一行

   ```py
   readline(size)
   ```

   - size:要读取的长度，单位字节

   调用此方法会根据结束符自动读取，并返回一个等于size长度的字符串，如果size为-1则返回整行。

5. 读取文件所有行

   ```py
   readlines()
   ```

   调用此方法会根据结束符自动分行读取，并返回一个包含所有分行的列表。

6. 移动文件指针

   ```py
   seek(offset, whence)
   ```

   - offset:  开始的偏移量，也就是代表需要移动偏移的字节数
   - whence: 可选，默认值为 0。给offset参数一个定义，表示要从哪个位置开始偏移；0代表从文件开头开始算起，1代表从当前位置开始算起，2代表从文件末尾算起。

7. 关闭文件

   ```py
   close()
   ```

   调用后关闭文件，不再继续操作该文件。

综合示例

```py
# 创建一个test.txt文件,注意路径在/usr下
f = open("/usr/test.txt", "w+")
i = f.write("hello world\n")
i = i + f.write("hello quecpython\n")
print("成功写入了{}个字节".format(i))
f.seek(0)
str = f.read(10)
print("读取10个字节:{}".format(str))
f.seek(0)
str = f.readline()
print("读取一行:{}".format(str))
f.seek(0)
str = f.readlines()
print("读取所有行:{}".format(str))
f.close()
# del f # 非必须操作,系统gc的时候会自动回收
print("文件关闭 测试结束")
```

运行结果

```py
>>> import example
>>> example.exec("/usr/test.py")

成功写入了29个字节
读取10个字节:hello worl
读取一行:hello world
读取所有行:['hello world\n', 'hello quecpython\n']
文件关闭 测试结束
>>> 
```

## UOS API

当进行文件高级操作的时候，需要调用uos库进行操作，以下是综合示例。

```py
import uos

def main():

    # 创建文件 此处并没有对文件进行写入操作
    f = open("/usr/uos_test","w")
    f.close()
    del f

    # 查看文件是否存在
    t = uos.listdir("/usr")
    print("检查usr路径的文件:{}".format(t))

    if "uos_test" not in t:
        print("新建文件不存在 测试失败")
        return

    # 查看文件状态
    a = uos.stat("/usr/uos_test")
    print("文件占用了{}字节".format(a[6]))

    # 重命名文件
    uos.rename("/usr/uos_test", "/usr/uos_test_new")
    t = uos.listdir("/usr")
    print("已经重命名测试文件 检查usr路径的文件:{}".format(t))

    if "uos_test_new" not in t:
        print("重命名文件不存在 测试失败")
        return

    # 删除文件
    uos.remove("/usr/uos_test_new")
    t = uos.listdir("/usr")
    print("已经删除测试文件 检查usr路径的文件:{}".format(t))

    if "uos_test_new" in t:
        print("删除文件失败 测试失败")
        return

    # 目录操作
    t = uos.getcwd()
    print("当前路径是:{}".format(t))
    uos.chdir("/usr")
    t = uos.getcwd()
    print("当前路径是:{}".format(t))
    if "/usr" != t:
        print("文件夹切换失败")
        return

    uos.mkdir("testdir")
    t = uos.listdir("/usr")
    print("创建测试文件夹 检查当前路径的文件:{}".format(t))

    if "testdir" not in t:
        print("文件夹创建失败")
        return

    uos.rmdir("testdir")
    t = uos.listdir("/usr")
    print("删除测试文件夹 检查当前路径的文件:{}".format(t))
    
    if "testdir" in t:
        print("文件夹删除失败")
        return

if __name__ == "__main__":
    main()
```

示例输出

```py
>>> example.exec("/usr/test.py")

检查usr路径的文件:['test.py', 'system_config.json', 'uos_test']
文件占用了0字节

已经重命名测试文件 检查usr路径的文件:['test.py', 'system_config.json', 'uos_test_new']
已经删除测试文件 检查usr路径的文件:['test.py', 'system_config.json']

当前路径是:/
当前路径是:/usr

创建测试文件夹 检查当前路径的文件:['test.py', 'system_config.json', 'testdir']

删除测试文件夹 检查当前路径的文件:['test.py', 'system_config.json']
>>> 
```

