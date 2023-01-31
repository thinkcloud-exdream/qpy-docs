QuecPython doc website
=====

visit: [teedoc.neucrack.com](https://teedoc.neucrack.com/) or [teedoc.github.io](https://teedoc.github.io)


## build locally

* Install Python3 first

```bash
# On Windows system, just double-click Python exe installer.
sudo apt install python3 python3-pip python3-venv
```

* Create virtual environment of Python3

```bash
# On Windows system, use 'path\to\.pyenv3' instead.
python3 -m venv path/to/.pyenv3
```

* Activate virtual environment of Python3

```bash
# On Windows system, run 'path\to\.pyenv3\Scripts\activate.bat' instead under working directory.
source path/to/.pyenv3/bin/activate
```

* Install teedoc

```bash
pip3 install teedoc
```

* Get source files

```bash
git clone https://gitee.com/qpy-doc-center/teedoc_with_qpydoc.git
```

* Install plugins

```bash
cd teedoc_with_qpydoc
teedoc install
```

* build and serve

```bash
# Build static pages of website.
./build.sh

# Build static pages of website and start service.
./build.sh -s
```

then visit [http://127.0.0.1:80](http://127.0.0.1:80)


