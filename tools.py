def dayTranslation(day_and_date: str) -> str:
    dict = {
        "Monday"   : "星期一",
        "Tuesday"  : "星期二",
        "Wednesday": "星期三",
        "Tursday"  : "星期四",
        "Friday"   : "星期五",
        "Saturday" : "星期六",
        "Sunday"   : "星期日"
    }
    time_list = day_and_date.split(" ")
    day = time_list[0]
    date = time_list[1]
    translated_day = dict[day]
    msg = translated_day + " " + date
    return msg