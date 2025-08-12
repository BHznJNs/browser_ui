# API 文档

本文档提供了 ``browser_ui`` 库的详细 API 参考。

## ``BrowserUI`` 类

``BrowserUI`` 是库的核心类，用于创建和管理浏览器 GUI 应用。

### 初始化

初始化 ``BrowserUI`` 实例。

- ##static_dir##: (可选) 静态文件（HTML, CSS, JS）所在的目录。如果提供此参数，将使用生产模式。
- ##port##: (可选) Web 服务器的端口，默认为 ``8080``。
- ##dev_server_url##: (可选) 前端开发服务器的 URL。如果提供此参数，将使用开发模式，``static_dir`` 将被忽略。

##注意##：必须提供 ``static_dir`` 或 ``dev_server_url`` 中的一个。

---

### 启动

启动 Web 服务器并在浏览器中打开应用。

- ##path##: (可选) 浏览器中要打开的初始路径，默认为根路径 (``/``)。

##注意##：此方法会启动一个新线程运行服务器，并使用 ``webbrowser`` 打开浏览器。

---

### 停止

停止 Web 服务器并释放资源。

##注意##：一旦调用此方法，``BrowserUI`` 实例不能再次使用。

---

### 注册方法

注册一个 Python 函数，使其可以从前端 JavaScript 调用。

- ##method_name##: 在 JavaScript 中调用此函数时使用的名称。
- ##method##: 要注册的 Python 函数。该函数可以接受一个参数（来自前端的 payload）并返回可序列化的数据。支持普通函数和生成器函数。

##示例##：
```python
def my_method(data):
    return {"result": data["input"] * 2}

ui.register_method("my_method", my_method)
```

---

### 添加事件监听器

为页面事件添加监听器。

- ##event_type##: ``EventType`` 枚举成员，如 ``EventType.page_loaded`` 或 ``EventType.page_closed``。
- ##callback##: 事件触发时要执行的函数（无参数）。

##示例##：
```python
def on_page_load():
    print("Page loaded!")

ui.add_event_listener(EventType.page_loaded, on_page_load)
```

---

### 发送事件

向前端发送一个服务器发送事件 (SSE)。

- ##event##: 事件的名称（字符串）。
- ##data##: 要发送的可序列化数据。

##示例##：
```python
ui.send_event("update", {"message": "New data available"})
```

---

### 注册模板变量

注册用于 HTML 模板渲染的变量。

- ##**args##: 关键字参数，其中键是模板中的变量名，值是变量的值。

##示例##：
```python
ui.register_template_vars(username="user123", theme="dark")
```

在 HTML 中使用：
```html
<h1>Hello, {{ username }}!</h1>
```

## ``EventType`` 枚举

``EventType`` 枚举定义了可以监听的页面事件。

- ``EventType.page_loaded``: 页面加载完成时触发。
- ``EventType.page_closed``: 页面关闭时触发。

##类方法##：
- 从字符串转换为 ``EventType`` 枚举成员。

## 类型定义

- ``Serializable``: 可序列化的数据类型，包括基本类型、列表、元组和字典。
- ``SerializableCallable``: 返回 ``Serializable`` 的可调用对象。
- ``GeneratorCallable``: 返回生成器（产生 ``Serializable`` 值）的可调用对象。

## JavaScript API

注入到前端的 JavaScript 提供了以下全局对象和函数。

### 调用后端函数

调用在后端注册的 Python 函数。

- ##method##: 要调用的 Python 函数的名称。
- ##payload##: (可选) 要发送到后端的数据（将序列化为 JSON）。
- ##返回##: 如果是普通函数，返回一个 Promise，解析为从后端返回的数据；如果是生成器函数，返回一个异步迭代器。

##示例##：
```javascript
const result = await requestBackend("my_method", { input: 5 });
console.log(result);  // { result: 10 }
```

对于生成器函数：
```javascript
const iter = await requestBackend("my_generator");
for await (const value of iter) {
    console.log(value);
}
```

### 后端监听器对象

用于监听来自后端的服务器发送事件 (SSE)。

- 添加一个持久的事件监听器。
- 移除一个事件监听器。
- 添加一个一次性的事件监听器。

##示例##：
```javascript
backendListener.on("update", (data) => {
    console.log("Received update:", JSON.parse(data));
});
```
