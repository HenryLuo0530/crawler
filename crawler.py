import requests
from bs4 import BeautifulSoup
import json

def crawl(days: int, latitude: int, longitude: int) -> int:
    url = f"https://clearoutside.com/forecast/{latitude}/{longitude}?view=midnight"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("[S] Succeed to request web data.")
    else:
        print("[E] Failed to request web data")
        print(f"[E] Response status code {response.status_code}")
        return 1
    soup = BeautifulSoup(response.text, "html.parser")
    elements = soup.find_all("div", class_="fc_day", limit=days)
    data_list = []
    for all in elements:
        data = {}

        #處理日期
        dates = all.find("div", class_="fc_day_date")
        date = dates.text
        data["dates"] = date

        #處理時間和品質
        ul = all.find("div", class_="fc_hours fc_hour_ratings")
        lis_bad  = ul.find_all("li", class_="fc_bad")
        lis_ok   = ul.find_all("li", class_="fc_ok")
        lis_good = ul.find_all("li", class_="fc_good")
        time_quality_list = []
        for li in lis_bad:
            time_quality = li.text
            time_quality_list.append(time_quality)
        for li in lis_ok:
            time_quality = li.text
            time_quality_list.append(time_quality)
        for li in lis_good:
            time_quality = li.text
            time_quality_list.append(time_quality)
        time_quality_list.sort()
        data["time_and_quality"] = time_quality_list

        data_list.append(data)

    with open("seeings.json", "w", encoding="utf-8") as file:
        json.dump(data_list, file, ensure_ascii=False, indent=4)
    print("[S] Data has been stored successfully")
    return 0
