QuecPython doc website
=====

visit: [teedoc.neucrack.com](https://teedoc.neucrack.com/) or [teedoc.github.io](https://teedoc.github.io)


## build locally

* Install Python3 first

```shell
sudo apt install python3 python3-pip
```

* Install teedoc

```
pip3 install teedoc
```

* Get source files

```
git clone https://gitee.com/qpy-doc-center/teedoc_with_qpydoc.git
```

* Install plugins

```
cd qpy-doc-center
teedoc install
```

* build and serve

```
# 编译静态网站文件
./build.sh
# 编译并预览
./build.sh -s
```

then visit [http://127.0.0.1:80](http://127.0.0.1:80)


