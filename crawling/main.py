import asyncio
import csv
import time
from typing import Tuple, Union, List
import aiohttp
from scrap.config import settings
from scrap.utils import RESPONSE_TYPE


url_map = {
    settings.CRAWL_HOST1: 0,
    settings.CRAWL_HOST2: 0,
    settings.CRAWL_HOST3: 0
}

INTERVAL = 10
FAILURE_INTERVAL = 60


async def make_queue(filename: str) -> asyncio.Queue:
    """
    output:
    queue: [["스타벅스", 1234], ["탐앤탐스", 5678]]
    """
    queue = asyncio.Queue()
    with open(filename, "r", encoding="utf-8") as fr:
        rdr = csv.DictReader(fr, fieldnames=['name', 'id'])
        for line in rdr:
            id, name = line['id'], line['name']
            queue.put_nowait((name, id))
    return queue


def print_result(results: List[RESPONSE_TYPE], queue: asyncio.Queue) -> None:
    """
    resp_json["status"]에 따라 다른 결과 출력
    status
      success : 크롤링 성공
      Fail : KAKAO MAP 크롤링 실패. scrap_server 사이드 문제
      Connect-Failed : CRAWL_HOST 연결 실패. main의 ClientSession 문제
    """
    for result in results:
        url, name, id, resp_json = result
        if resp_json["status"] == "Fail":
            url_map[url] = FAILURE_INTERVAL
            queue.put_nowait((name, id))
            print(f"{url} BANNED")
        elif resp_json["status"] == "success":
            print(f"{url} - {name} saved")
        elif resp_json["status"] == "Connect-Failed":
            print(f"Session Closed")
            queue.put_nowait((name, id))


async def fetch(
    session: aiohttp.ClientSession,
    url: str,
    name: str,
    id: int
) -> Tuple[str, str, int, RESPONSE_TYPE]:
    try:
        async with session.get(f"{url}/scrap/{id}") as response:
            resp_json = await response.json()
    except:
        resp_json = {"status": "connection-failed"}
    finally:
        return (url, name, id, resp_json)


async def send_request(queue: asyncio.Queue, session: aiohttp.ClientSession):
    """
    failure_interval
      - 특정 CRAWL_HOST가 KAKAO MAP 연결 실패 시 60으로 설정
      - 한번의 루프(10초) 마다 failure_interval 1씩 감소. 총 600초(10분) 동안 해당 호스트 중지
    """
    fetchers = []
    for url, failure_interval in url_map.items():
        if failure_interval == 0:
            try:
                name, id = await queue.get()
                fetchers.append(asyncio.create_task(fetch(session, url, name, id)))
            except asyncio.QueueEmpty:
                break
        else:
            failure_interval -= 1
            url_map[url] = failure_interval
    results = await asyncio.gather(*fetchers)
    print_result(results, queue)


async def main():
    queue = await make_queue(settings.CAFE_FN)
    async with aiohttp.ClientSession() as session:
        while queue:
            await send_request(queue, session)
            await asyncio.sleep(INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())
