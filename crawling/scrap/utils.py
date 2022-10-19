import json
from typing import Dict, List, Union, Tuple
import requests
from sqlalchemy.orm import Session
from db.model import Cafe, Facility


REQ_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Host": "place.map.kakao.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
}
KAKAOMAP_BASE_URL = "https://place.map.kakao.com/main/v"
RESPONSE_TYPE = Dict[str, Union[str, Dict, List]]


facility_map = {
    "smokingroom" : Facility(name="흡연"),
    "fordisabled" : Facility(name="장애인시설"),
    "nursery" : Facility(name="놀이방"),
    "parking" : Facility(name="주차"),
    "wifi" : Facility(name="wifi"),
    "pet" : Facility(name="애완동물출입")
}


def change_address(addr: Dict[str, str]) -> Tuple[str, str, str]:
    addr = addr.replace("'", "\"")
    addr = json.loads(addr)
    newaddr = addr["newaddr"]
    region = addr["region"]
    addrbunho = addr["addrbunho"]
    postcode = newaddr["bsizonno"]
    jibeonfullname = region["fullname"] + " " + addrbunho
    dorofullname = region["newaddrfullname"] + " " + newaddr["newaddrfull"]
    return postcode, jibeonfullname, dorofullname


def change_response(response: RESPONSE_TYPE) -> RESPONSE_TYPE:
    if not response["isExist"]:
        return {"status":"NotExist"}
    basic_info = response["basicInfo"]
    name = basic_info["placenamefull"]
    address = basic_info.get("address")
    postcode, jibeonfullname, dorofullname = change_address(address)
    phone = basic_info.get("phonenum")
    tags = basic_info.get("tags")
    img_url = basic_info.get("mainphotourl")
    facilities = basic_info.get("facilityInfo")
    resp = {
        "name":name,
        "jibeonfullname":jibeonfullname,
        "dorofullname":dorofullname,
        "postcode":postcode,
        "phone":phone,
        "tags":tags,
        "img_url":img_url,
        "facilities":facilities,
        "status":"success"
    }
    return resp


def get_resp_with_json(id: int) -> RESPONSE_TYPE:
    resp = requests.get(f"{KAKAOMAP_BASE_URL}/{id}", headers=REQ_HEADERS)
    resp = resp.json()
    resp = change_response(resp)
    return resp


def create_cafe(resp: RESPONSE_TYPE, db: Session) -> None:
    cafe = Cafe(
        cafename = resp["name"],
        phone = resp["phone"],
        jibeonfullname = resp["jibeonfullname"],
        dorofullname = resp["dorofullname"],
        imageurl = resp["image_url"],
        tags = ' '.join(resp["tags"])
    )
    for facility, able in resp["facilities"]:
        if able == "N":
            cafe.disable_facilities.append(facility_map[facility])
        else:
            cafe.able_facilities.append(facility_map[facility])
    db.add(cafe)
    db.commit()
