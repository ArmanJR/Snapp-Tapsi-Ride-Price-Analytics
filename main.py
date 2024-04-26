import time
from datetime import datetime
import pytz
import requests
import json

proxies = {
    "http": "YOUR_PROXY",
}

f = open("tokens/snapp_token.txt", "r")
snappToken = f.read().strip()
snappHeaders = {
    'content-type': 'application/json',
    'Host': 'app.snapp.taxi',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
    'authorization': 'Bearer ' + snappToken,
}

f = open("tokens/tapsi_token.txt", "r")
tapsiToken = f.read().strip()
tapsiHeaders = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,fa;q=0.8",
    "Connection": "keep-alive",
    "Content-Length": "221",
    "Cookie": "token=" + tapsiToken,
    "Host": "api.tapsi.cab",
    "Origin": "https://app.tapsi.cab",
    "Referer": "https://app.tapsi.cab/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "content-type": "application/json",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "'macOS'",
    "x-agent": "v2.2|passenger|WEBAPP|6.1.4||5.0",
    "x-authorization": tapsiToken,
}


def loc_normalizer(coord, service):
    if service == "snapp":
        return coord
    return float(str(coord) + "000001")


# might be outdated!
def get_snapp(origin_lat, origin_lng, dest_lat, dest_lng):
    origin_lat = loc_normalizer(origin_lat, "snapp")
    origin_lng = loc_normalizer(origin_lng, "snapp")
    dest_lat = loc_normalizer(dest_lat, "snapp")
    dest_lng = loc_normalizer(dest_lng, "snapp")
    snappData = {
        "points": [
            {
                "lat": origin_lat,
                "lng": origin_lng
            },
            {
                "lat": dest_lat,
                "lng": dest_lng
            },
            None
        ],
        "round_trip": False,
        "service_types": [
            1,
            2
        ],
        "priceriderecom": False
    }
    response = requests.post("https://app.snapp.taxi/api/api-base/v2/passenger/newprice/s/6/0", json=snappData,
                             headers=snappHeaders, proxies=proxies)
    responseJson = json.loads(response.text)
    isOk = 'status' in responseJson and responseJson['status'] == 200
    price_snapp = ""
    if isOk:
        price_snapp = str(int(responseJson["data"]["prices"][0]["final"] / 10))
    return price_snapp


# might be outdated!
def get_tapsi(origin_lat, origin_lng, dest_lat, dest_lng):
    origin_lat = loc_normalizer(origin_lat, "tapsi")
    origin_lng = loc_normalizer(origin_lng, "tapsi")
    dest_lat = loc_normalizer(dest_lat, "tapsi")
    dest_lng = loc_normalizer(dest_lng, "tapsi")
    tapsiData = {
        "origin": {
            "latitude": origin_lat,
            "longitude": origin_lng
        },
        "destinations": [
            {
                "latitude": dest_lat,
                "longitude": dest_lng
            }
        ],
        "hasReturn": False,
        "waitingTime": 0,
        "gateway": "CAB",
        "initiatedVia": "WEB"
    }
    response = requests.post("https://api.tapsi.cab/api/v2.4/ride/preview", json=tapsiData, headers=tapsiHeaders, proxies=proxies)
    responseJson = json.loads(response.text)
    isOk = 'result' in responseJson and responseJson['result'] == 'OK'
    price_tapsi = ""
    if isOk:
        normal_service = None
        for category in responseJson["data"]["categories"]:
            if category["key"] == "NORMAL":
                normal_service = category["services"][0]
                break

        if normal_service:
            price_tapsi = str(normal_service["prices"][0]["passengerShare"])
    return price_tapsi


file_data = ""
# the final destination
dest = {
    "lat": 35.783020,
    "lng": 51.419115
}
origins = [
    # this is the main origin location; uncomment and fill it
    # {"lat": , "lng": , "district": "خونه من"},
    # these are the other candidate locations for the origin you want to test
    {"lat": 35.741281, "lng": 51.316010, "district": "باغ فیض هجرت"},
    {"lat": 35.741265, "lng": 51.326608, "district": "باغ فیض باهنر"},
    {"lat": 35.737783, "lng": 51.313119, "district": "ستاری کورش"},
    {"lat": 35.735796, "lng": 51.302750, "district": "میدون سازمان برنامه"},
    {"lat": 35.733684, "lng": 51.305773, "district": "شقایق شمالی"},
    {"lat": 35.725488, "lng": 51.325243, "district": "کاشانی اباذر"},
    {"lat": 35.733412, "lng": 51.326646, "district": "اباذر پردیس زندگی"},
    {"lat": 35.740152, "lng": 51.303493, "district": "کاشانی سر جنت"},
    {"lat": 35.727298, "lng": 51.304213, "district": "فردوس شقایق"},
    {"lat": 35.732470, "lng": 51.310532, "district": "کاشانی مینیاتور"},
    {"lat": 35.725788, "lng": 51.295987, "district": "هایپراستار"}
]

for origin in origins:
    time.sleep(1)
    now = datetime.now(pytz.timezone('Asia/Tehran'))
    now_time = now.strftime('%H:%M:%S')
    now_date = now.strftime('%Y-%m-%d')
    today = datetime.today().strftime('%A')
    snapp = get_snapp(origin_lat=origin["lat"], origin_lng=origin["lng"], dest_lat=dest["lat"], dest_lng=dest["lng"])
    tapsi = get_tapsi(origin_lat=origin["lat"], origin_lng=origin["lng"], dest_lat=dest["lat"], dest_lng=dest["lng"])
    bothOk = str(snapp != "" and tapsi != "")
    file_data = file_data + "\n" + origin["district"] + "," + snapp + "," + tapsi + "," + now_time + "," + now_date + "," + today + "," + bothOk
    print(origin["district"])

f = open("results.csv", "a")
f.write(file_data)
f.close()