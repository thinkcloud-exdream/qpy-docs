# ujson - JSON编码和解码
`ujson`模块实现在Python数据对象和JSON数据格式之间进行转换的功能。该模块实现相应CPython模块的子集。更多信息请参阅CPython文档：[json](https://docs.python.org/3.5/library/json.html#module-json)


## 编码json数据

将`Python`对象编码成json字符串

### `ujson.dump`

```python
ujson.dump(obj, stream)
```

序列化`obj`数据对象转化成`JSON`字符串，并将其写入到给定的`stream`中。

### `ujson.dumps`

```python
ujson.dumps(obj)
```

将`obj`字典类型的数据转换成`JSON`字符串。

## 解码json数据

将JSON数据解码成`Python`对象。

### `ujson.load`

```python
ujson.load(stream)
```

解析给定的数据`stream`，将其解析为`JSON`字符串并反序列化成`Python`对象，最终将对象返回。

### `ujson.loads`

```python
ujson.loads(str)
```

解析`JSON`字符串`str`并返回一个`Python`对象。
