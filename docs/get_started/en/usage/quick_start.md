---
title: teedoc quick start
keywords: teedoc use, teedoc quick start
desc: teedoc, which converts markdown or jupyter notbook into html static web pages, introduces the quick and easy way to use teedoc
---

This document is mainly to let you who are new to contact you quickly get started. For more details, please see the more detailed documents later.

## Install Python3

`teedoc` is a software developed based on `Python3` language, and it needs the support of this software

For example, on `Ubuntu`:

```shell
sudo apt install python3 python3-pip git
```

`Windows` and `macOS` please go to [Official Website Download](https://www.python.org/downloads/)


## Install teedoc

Open the terminal (`Windows` press `Ctrl+R` and enter `cmd`), enter:

```shell
pip3 install teedoc
```

Use the following command to update the software later

>! Be sure to update the software and plug-ins at the same time before use, to prevent problems caused by different versions

```shell
pip3 install -U teedoc
```

> If your network uses `pypi.org` and the speed is very slow, you can choose other sources, such as Tsinghua tuna source: `pip3 install teedoc -i https://pypi.tuna.tsinghua.edu.cn/simple`

Now you can use the `teedoc` command in the terminal

If not, please check if the `Python` executable directory is not added to the environment variable `PATH`,
For example, it may be in `~/.local/bin`

## New Project

Create an empty directory to store the document project

```shell
mkdir my_site
cd my_site
teedoc init
```

or
```shell
teedoc -d my_site init
```

Select `1`, which is the `minimal` template to generate, or you can directly generate it with `teedoc -d my_site --template=minimal init`

This will automatically generate some basic files in the `my_site` directory


In addition, in addition to using the `init` command to generate a minimal project, you can also get a source code of the official website document and modify it based on the content of this document
```shell
git clone https://github.com/teedoc/teedoc.github.io my_site
```
or
```shell
git clone https://gitee.com/teedoc/teedoc.gitee.io my_site
```

## Install plugin

This will install the plugin according to the plugin settings of `plugins` in `site_config.sjon`

```shell
cd my_site
teedoc install
```

> The plug-in is also released in the form of `python` package, so this will download the corresponding plug-in from `pypi.org`. Similarly, other sources can also be used, such as Tsinghua tuna source: `teedoc -i https://pypi. tuna.tsinghua.edu.cn/simple install`

>! Be sure to update the software and plug-ins at the same time before use, to prevent problems caused by different versions

## Build an `HTML` page and start an `HTTP` service

```shell
teedoc serve
```

This command will first build all `HTML` pages and copy resource files, and then start an `HTTP` service
If you only need to generate pages, use

```shell
teedoc build
```


After displaying `Starting server at 0.0.0.0:2333 ....`, it is fine

Open the browser to visit: [http://127.0.0.1:2333](http://127.0.0.1:2333)


At the same time, you can see that there is an additional `out` directory under the directory, which is the generated static website content, directly copy it to the server and use `nginx` or `apache` for deployment.


## Document structure

There are several important files in the project:
* The project root directory has a `site_config.json` file, which is the main configuration of the project
* There can be multiple documents in the project, set in the `route` configuration item of `site_config`, each document directory must have `config.json` and `sidebar.json` (`json` file can also be `yaml `File), `config` file is responsible for the configuration items of this document, such as the document name, multiple documents can use `import` to share a template

## Add a document

* Create a `markdown` (end with `.md`) file in the directory where this file is located, such as `first.md`
* Add sidebar link in `sidebar.yaml`

```markdown
items:
-label: Brief
    file: README.md
-label: First
    file: first.md
```

## More examples

For more information, please visit: [teedoc.neucrack.com](https://teedoc.neucrack.com/) or [teedoc.github.io](https://teedoc.github.io/)

For more examples, visit: [github.com/teedoc/teedoc.github.io](https://github.com/teedoc/teedoc.github.io) or [https://github.com/teedoc/template]( https://github.com/teedoc/template), or [sipeed wiki](https://github.com/sipeed/sipeed_wiki)
