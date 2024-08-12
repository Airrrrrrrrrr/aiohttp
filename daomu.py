import requests
from bs4 import BeautifulSoup
import time
import asyncio
import aiohttp


BASE_URL = "https://www.kunnu.com/wanmei/"
hrefs_list = []
titles_list = []
text_list = []


def get_list():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    for a in soup.select('[target=_blank]'):
        hrefs_list.append(a['href'])


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def get_text(url):
    conn = aiohttp.TCPConnector(limit=2)
    async with aiohttp.ClientSession(connector=conn) as session:
        BEGIN = time.time()
        response_text = await fetch(session, url)
        soup = BeautifulSoup(response_text, 'html.parser')
        for title in soup.select('#nr_title'):
            titles_list.append(title.text)
            file_title = title.text
        for p in soup.select('#nr1'):
            text_list.append(p.text)
            file_path = f"C://Users//20962//PycharmProjects//pythonProject4//wanmei//{file_title}_.txt"

            with open(file_path, 'w+', encoding='utf-8') as f:
                f.write(p.text)
                f.close()

        END = time.time()
        print(END - BEGIN)



get_list()
tasks = [asyncio.ensure_future(get_text(url)) for url in hrefs_list]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
