from bs4 import BeautifulSoup
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from schemas import Cafe
from utils import remove_space, start_webdriver

chrome, wait = start_webdriver()
app = FastAPI()

async def scrap_cafe(id: int):
    url = f"https://place.map.kakao.com/{id}"
    chrome.get(url)
    chrome.delete_all_cookies()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span[class=txt_address]")))
    
    html = chrome.page_source
    soup =BeautifulSoup(html, 'html.parser')

    if soup.find("div", class_="info_noresult"):
        return {}

    address = remove_space(soup.find("span", class_="txt_address").text)
    
    phone = soup.find("span", class_="txt_contact")
    phone = phone.text if phone else ""

    tags = soup.find("span", class_="tag_g")
    tags = tags.find_all("a", class_="link_tag") if tags else []
    tags = [tag.text for tag in tags]
    
    img_url = soup.find("span", class_="bg_present")
    img_url = img_url['style'].split('url')[-1][2:-3] if img_url else ""

    facilities = soup.find("ul", class_="list_facility")
    facilities = facilities.find_all("span", class_="color_g") if facilities else []
    facilities = [remove_space(facility.text) for facility in facilities]

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

@app.on_event("shutdown")
async def app_shutdown():
    chrome.close()
