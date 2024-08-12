首先确保你安装了asyncio、aiohttp以及BeautifulSoup解析文本的python库。

这三个库都可以通过pip命令安装，命令如下

```
pip install beautifulsoup4 asyncio aiohttp -i https://pypi.tuna.tsinghua.edu.cn/simple
```

------------



这里有两个关键字。

async、await

下面是一个简单的程序；

```
import asyncio

async def hello():
    print("Hello, world!")
    await asyncio.sleep(1)
    print("Hello again!")

aaa = hello()
asyncio.run(aaa)
```

async关键字会将 原本的hello()函数变成一个coroutine function；

而hello()并不会直接执行，此时的aaa是一个coroutine object；

既然coroutine无法直接执行，那么我们该怎样运行定义的函数呢？

我们需要用asyncio.run(aaa)这个函数，它首先会建立eventloop，然后将aaa这个coroutine变成task 

那么await在这里有什么作用呢？

await会等待这个coroutine成为一个task

await还可以提取coroutine或task返回值。

还有asyncio.gather()、asyncio.create_task()都可以将coroutine变成task；

只不过asyncio.run()和asyncio.gather()是隐式的将coroutine变成task，而asyncio.create_task()是显式的将coroutine变成task。

--------------



程序的主要部分

```
async def fetch(session, url):
    async with session.get(url) as response:	#使用 aiohttp 的异步上下文管理器发送请求，并获取响应。
        return await response.text()


async def get_text(url):
    conn = aiohttp.TCPConnector(limit=2)	#限制并发数量
    async with aiohttp.ClientSession(connector=conn) as session:
        BEGIN = time.time()
        response_text = await fetch(session, url)
```

```
tasks = [asyncio.ensure_future(get_text(url)) for url in hrefs_list]	#ensure_future() 会启动协程的执行，并返回一个 asyncio.Task 对象。
loop = asyncio.get_event_loop()		#获得一个事件循环，如果当前线程还没有事件循环，则创建一个新的事件循环loop；
loop.run_until_complete(asyncio.wait(tasks))	#asyncio.wait() 等待它们全部完成，然后输出每个任务的结果
```
