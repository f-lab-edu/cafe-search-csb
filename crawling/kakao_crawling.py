import asyncio
import aiohttp
import csv

"""
입력 파일(cafe.csv) 형태
  - 장안생활카페,353979517
  - 더크림 디저트쇼룸,526696751

출력 파일(cafe_info.csv) 형태
  - 장안생활카페,서울 동대문구 천호대로89길 9 1층 (우)02644,,"['#카카오페이', '#제로페이']",//t1.kakaocdn.net/thumb/T800x0.q80/?fname=http%3A%2F%2Ft1.kakaocdn.net%2Ffiy_reboot%2Fplace%2F3C1315A88989449C97C48DA979535DB,"['WIFI', '동물출입금지', '주차', '장애시설', '놀이방시설 없음', '흡연실']"
  - 더크림 디저트쇼룸,서울 동대문구 천호대로79길 55 1층 (우)02635,070-7808-7313,"['#디저트카페', '#카카오페이', '#제로페이']",//t1.kakaocdn.net/thumb/T800x0.q80/?fname=http%3A%2F%2Ft1.daumcdn.net%2Fplace%2F9CC84996DD2D4B1A84E81B30821D6CD,[]
"""

async def worker(session, queue, wtr):
    while not queue.empty():
        name, id = await queue.get()
        async with session.get(f"http://127.0.0.1:8000/scrap/{id}") as response:
            cafe = await response.json()
            if cafe:
                wtr.writerow([name, cafe['address'], cafe['phone'], cafe['tags'], cafe['img_url'], cafe['facilities']])
            else:
                continue

async def create_cafe(queue: asyncio.Queue, rdr):
    for line in rdr:
        id, name = line[-1], line[0]
        await queue.put((id, name))

async def main():
    queue = asyncio.Queue(10)

    with open('./cafe.csv', 'r', encoding='utf-8') as fr, open('./cafe_info.csv', 'a', encoding='utf-8', newline='') as fw:
        rdr = csv.reader(fr)
        wtr = csv.writer(fw)

        cafe_producer = asyncio.create_task(create_cafe(queue, rdr))
        async with aiohttp.ClientSession() as session:
            cafe_consumer = [asyncio.create_task(worker(session, queue, wtr)) for _ in range(5)]
        
        await asyncio.gather(cafe_producer, *cafe_consumer)

asyncio.run(main())
