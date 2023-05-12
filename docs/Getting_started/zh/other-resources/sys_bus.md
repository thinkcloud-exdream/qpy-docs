# sys_bus

sys_bus是一个基于MicroPython的事件总线模块，可以在MicroPython设备之间进行消息发布和订阅。它提供了订阅、发布、取消订阅等功能，并支持异步和同步发布。本文将介绍sys_bus的使用方法及其架构原理。



## 1. 导入sys_bus模块

使用sys_bus模块之前，需要将该模块安装到MicroPython设备中。可以将sys_bus.py文件上传到MicroPython设备中，并通过`import`命令导入该模块：

```python
import sys_bus
```



## 2. sys_bus模块的基本用法

sys_bus模块提供了订阅、发布、取消订阅等功能，并支持异步和同步发布。



### 2.1 订阅

使用`subscribe()`函数订阅一个主题，可以接收该主题下的所有消息。

```python
def callback(topic, msg):
    print('Received message:', msg)

sys_bus.subscribe('topic1', callback)
```

在这个示例中，我们定义了一个名为callback的回调函数，并使用`subscribe()`函数订阅了名为`topic1`的主题。当`topic1`主题下有新消息时，callback函数会被自动调用。



### 2.2 发布

使用`publish()`函数发布一条消息，该消息将被发送到指定的主题下。

```python
sys_bus.publish('topic1', 'Hello, World!')
```

在这个示例中，我们使用`publish()`函数发布了一条消息`Hello, World!`，该消息将被发送到`topic1`主题下。



### 2.3 取消订阅

使用`unsubscribe()`函数取消订阅一个主题。

```python
sys_bus.unsubscribe('topic1', callback)
```

在这个示例中，我们使用`unsubscribe()`函数取消了对`topic1`主题的订阅。



### 2.4 异步发布

使用`publish_async()`函数异步发布一条消息，该消息将在新的线程中被发送到指定的主题下。

```python
sys_bus.publish_async('topic1', 'Hello, World!')
```

在这个示例中，我们使用`publish_async()`函数异步发布了一条消息`Hello, World!`，该消息将在新的线程中被发送到`topic1`主题下。



### 2.5 同步发布

使用`publish_sync()`函数同步发布一条消息，该消息将在当前线程中被发送到指定的主题下。

```python
sys_bus.publish_sync('topic1', 'Hello, World!')
```

在这个示例中，我们使用`publish_sync()`函数同步发布了一条消息`Hello, World!`，该消息将在当前线程中被发送到`topic1`主题下。



## 3. 完整示例

下面是一个使用sys_bus模块的完整示例，它实现了一个简单的消息发布和订阅系统。该系统由一个

Publisher和Subscriber两个类组成，Publisher用于发布消息，Subscriber用于订阅消息。

```python
import sys_bus

class Publisher:
    def __init__(self, topic):
        self.topic = topic

    def publish(self, msg):
        sys_bus.publish(self.topic, msg)

class Subscriber:
    def __init__(self, topic, callback):
        self.topic = topic
        self.callback = callback
        sys_bus.subscribe(self.topic, self.callback)

    def unsubscribe(self):
        sys_bus.unsubscribe(self.topic, self.callback)
        
        
def callback(topic, msg):
    print('Received message:', msg)

p = Publisher('topic1')
s = Subscriber('topic1', callback)

p.publish('Hello, World!')

s.unsubscribe()
        
```



在这个示例中，我们定义了一个名为Publisher的类，用于发布消息。它的构造函数需要一个主题作为参数，用于指定发布的主题。`publish()`方法用于发布一条消息到指定主题。

我们还定义了一个名为Subscriber的类，用于订阅消息。它的构造函数需要两个参数，一个是主题，一个是回调函数。回调函数用于处理接收到的消息。`unsubscribe()`方法用于取消订阅。

我们还定义了一个名为callback的回调函数，并创建了一个Publisher和一个Subscriber对象。在Publisher对象中，我们使用`publish()`函数发布了一条消息`Hello, World!`，该消息将被发送到`topic1`主题下。在Subscriber对象中，我们使用`unsubscribe()`函数取消了对`topic1`主题的订阅。

通过这个简单的示例，我们可以看到sys_bus模块是如何实现消息发布和订阅的。我们可以使用Publisher对象发布消息，并使用Subscriber对象订阅消息，以实现设备之间的通信。同时，sys_bus模块还提供了异步和同步发布的功能，以满足不同应用场景的需求。



