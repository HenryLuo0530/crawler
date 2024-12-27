import requests
from bs4 import BeautifulSoup

url = "https://clearoutside.com/forecast/25.04/121.56?view=midday"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
elements = soup.find_all("div", class_="fc_day")
for all in elements:
    dates = all.find("div", class_="fc_day_date")
    date = dates.text
    print(date)
    ul = all.find("div", class_="fc_hours fc_hour_ratings")
    lis = ul.find_all("li", class_="fc_bad")
    for li in lis:
        time_quality = li.text
        print(time_quality)
            

#print(response.text)
"""
if response.status_code == 200:
    with open('rawdata.html', 'w', encoding='utf-8') as file:
        file.write(response.text)
    print("succeeded\n")
else:
    print("failed\n")
"""