import requests
from bs4 import BeautifulSoup
import json

url = "https://clearoutside.com/forecast/25.04/121.56?view=midnight"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
elements = soup.find_all("div", class_="fc_day")
data_list = []
for all in elements:
    data = {}

    #處理日期
    dates = all.find("div", class_="fc_day_date")
    date = dates.text
    data["date"] = date

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
print(data_list)

#print(response.text)
"""
if response.status_code == 200:
    with open('rawdata.html', 'w', encoding='utf-8') as file:
        file.write(response.text)
    print("succeeded\n")
else:
    print("failed\n")
"""