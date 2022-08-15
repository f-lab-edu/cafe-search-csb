import aiohttp
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from schemas import Cafe

app = FastAPI()

async def scrap_cafe(id: int):
    url = f"https://place.map.kakao.com/main/v/{id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            page = await response.json()
            if not page["isExist"]:
                return
    
    basic_info = page["basicInfo"]
    address = basic_info.get("address")
    phone = basic_info.get("phonenum")
    tags = basic_info.get("tags")
    img_url = basic_info.get("mainphotourl")
    facilities = basic_info.get("facilityInfo")
    
    cafe = Cafe(
        address=address,
        phone=phone,
        tags=tags,
        img_url=img_url,
        facilities=facilities
    )

    return cafe

@app.get("/scrap/{id}")
async def get_cafe(id: int):
    cafe = await scrap_cafe(id)
    cafe = jsonable_encoder(cafe)
    return JSONResponse(content=cafe)
