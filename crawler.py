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

        lis_bad  = ul_and_daylight.find_all("li", class_="fc_bad")
        lis_ok   = ul_and_daylight.find_all("li", class_="fc_ok")
        lis_good = ul_and_daylight.find_all("li", class_="fc_good")
        time_quality_list = []
        for li in lis_bad:
            time_quality = li.text
            time_and_quality = time_quality.split(" ")
            time = time_and_quality[1]
            quality = time_and_quality[2]
            time_quality_list.append([time, quality])
        for li in lis_ok:
            time_quality = li.text
            time_and_quality = time_quality.split(" ")
            time = time_and_quality[1]
            quality = time_and_quality[2]
            time_quality_list.append([time, quality])
        for li in lis_good:
            time_quality = li.text
            time_and_quality = time_quality.split(" ")
            time = time_and_quality[1]
            quality = time_and_quality[2]
            time_quality_list.append([time, quality])
        
        sort_key = {
            "12": 0,
            "13": 1,
            "14": 2,
            "15": 3,
            "16": 4,
            "17": 5,
            "18": 6,
            "19": 7,
            "20": 8,
            "21": 9,
            "22": 10,
            "23": 11,
            "00": 12,
            "01": 13,
            "02": 14,
            "03": 15,
            "04": 16,
            "05": 17,
            "06": 18,
            "07": 19,
            "08": 20,
            "09": 21,
            "10": 22,
            "11": 23
        }
        time_quality_list_sorted = sorted(time_quality_list, key=lambda k: sort_key[k[0]])
        data["time_and_quality"] = time_quality_list_sorted

        data_list.append(data)

    with open("./json_file/seeings.json", "w", encoding="utf-8") as file:
        json.dump(data_list, file, ensure_ascii=False, indent=4)
    print("[S] Data has been stored successfully.")
    return 0

if __name__ == "__main__":
    seeing_crawl(days=3, latitude=25.17, longitude=121.56)