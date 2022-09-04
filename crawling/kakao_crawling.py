import asyncio
import csv
import aiohttp

""" kakao map crawling

kakao map으로부터 카페 정보를 얻어옵니다.

  Input File(cafe.csv)
  - cafe_name, cafe_id
  - 장안생활카페, 353979517

  Ouput File(cafe_info.csv)
   - cafe_name, address, tags, img_src, facilities
   - 장안생활카페,서울 동대문구 천호대로89길 9 1층 (우)02644,,"['#카카오페이', '#제로페이']",//t1.kakaocdn.net/thumb/T800x0.q80/?fname=http%3A%2F%2Ft1.kakaocdn.net%2Ffiy_reboot%2Fplace%2F3C1315A88989449C97C48DA979535DB,"['WIFI', '동물출입금지', '주차', '장애시설', '놀이방시설 없음', '흡연실']"
"""


NUM_OF_WORKERS = 5


async def worker(session: aiohttp.ClientSession, queue: asyncio.Queue, wtr: csv.writer):
    while not queue.empty():
        name, id = await queue.get()
        async with session.get(f"http://127.0.0.1:8000/scrap/{id}") as response:
            cafe = await response.json()
            if cafe:
                wtr.writerow([name, cafe['address'], cafe['phone'], cafe['tags'], cafe['img_url'], cafe['facilities']])


async def create_cafe(queue: asyncio.Queue, rdr: csv.DictReader):
    for line in rdr:
        id, name = line['id'], line['name']
        await queue.put((id, name))


async def main():
    queue = asyncio.Queue(10)
    with open('./cafe.csv', 'r', encoding='utf-8') as fr, open('./cafe_info.csv', 'a', encoding='utf-8', newline='') as fw:
        rdr = csv.DictReader(fr, fieldnames=['name', 'id'])
        wtr = csv.writer(fw)
        cafe_producer = asyncio.create_task(create_cafe(queue, rdr))
        async with aiohttp.ClientSession() as session:
            cafe_consumers = [asyncio.create_task(worker(session, queue, wtr)) for _ in range(NUM_OF_WORKERS)]
        await asyncio.gather(cafe_producer, *cafe_consumers)


asyncio.run(main())
