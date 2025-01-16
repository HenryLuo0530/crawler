import json
from youtubesearchpython import VideosSearch
"""
The package above has stopped maintaining.
In /python_env/lib/python3.12/site-packages/youtubesearchpython/core/requests.py
comment out line 25: proxies=self.proxy
"""

def youtube_search(keywords: str) -> str:
    video_search = VideosSearch(keywords, limit = 1)
    search_result = video_search.result()
    with open("./json_file/video_result.json", "w", encoding="utf-8") as file:
        json.dump(search_result, file, ensure_ascii=False, indent=4)
    video_link = search_result["result"][0]["link"]
    return video_link

if __name__ == "__main__":
    print(youtube_search('Gawr Gura reflect'))