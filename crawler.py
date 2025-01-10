import requests
from bs4 import BeautifulSoup
import json

def seeing_crawl(days: int, latitude: int, longitude: int) -> int:
    url = f"https://clearoutside.com/forecast/{latitude}/{longitude}?view=midday"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("[S] Succeed to request web data.")
    else:
        print("[E] Failed to request web data.")
        print(f"[E] Response status code {response.status_code}.")
        return 1
    soup = BeautifulSoup(response.text, "html.parser")
    elements = soup.find_all("div", class_="fc_day", limit=days)
    data_list = []
    for all in elements:
        data = {}

        #處理星期與日期
        day_and_date = all.find("div", class_="fc_day_date")
        data["day_and_date"] = day_and_date.text

        #處理月亮
        moon_info = all.find("div", class_="fc_moon")
        moon_phase = moon_info.find("span", class_="fc_moon_phase")
        data["moon_phase"] = moon_phase.text
        moon_percentage = moon_info.find("span", class_="fc_moon_percentage")
        data["moon_percentage"] = moon_percentage.text

        #處理時間、品質和天文黑夜
        ul_and_daylight = all.find("div", class_="fc_hours fc_hour_ratings")

        daylight_content = ul_and_daylight.find("div", class_="fc_daylight").get_text()
        daylight_list = daylight_content.split(". ")
        atro_dark_contnent = daylight_list[4]
        time_element = atro_dark_contnent.split(" ")
        start_time = time_element[2].split(":")
        start_time_hour = start_time[0]
        end_time = time_element[4].split(":")
        end_time_hour = end_time[0]
        data["astro_dark"] = [start_time_hour, end_time_hour]

        li_class_name = ["fc_bad", "fc_ok", "fc_good"]
        time_quality_list = []
        for i in range(0, 3):
            li_quality = ul_and_daylight.find_all("li", class_=li_class_name[i])
            for li in li_quality:
                time_quality = li.text
                time_and_quality = time_quality.split(" ")
                time = time_and_quality[1]
                quality = time_and_quality[2]
                time_quality_list.append([time, quality])
        
        sort_hour = [
            "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23",
            "00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11"
        ]
        sort_key = { sort_hour[i]: i for i in range(0, 24) }
        time_quality_list_sorted = sorted(time_quality_list, key=lambda k: sort_key[k[0]])
        data["time_and_quality"] = time_quality_list_sorted

        data_list.append(data)

    with open("./json_file/seeings.json", "w", encoding="utf-8") as file:
        json.dump(data_list, file, ensure_ascii=False, indent=4)
    print("[S] Data has been stored successfully.")
    return 0

if __name__ == "__main__":
    seeing_crawl(days=3, latitude=25.17, longitude=121.56)