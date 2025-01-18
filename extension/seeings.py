import json
from random import randint

from extension import tools

def get_data() -> dict:
    with open("./json_file/seeings.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

def check_input(limit_days, types, method, latitude, longitude) -> int:
    try:
        limit_days, types = int(limit_days), int(types)
        method = str(method)
        latitude, longitude = float(latitude), float(longitude)
    except:
        return 10

    if (limit_days < 1):
        return 1
    elif (limit_days > 7):
        return 2

    method_list = ['a', 's']
    if (types < 0) or (types > 1) or (method not in method_list):
        return 3
    
    return 0

def date_translation(date: dict) -> str:
    weekday_dictionary = {
        "Monday"   : "星期一",
        "Tuesday"  : "星期二",
        "Wednesday": "星期三",
        "Thursday" : "星期四",
        "Friday"   : "星期五",
        "Saturday" : "星期六",
        "Sunday"   : "星期日"
    }
    weekday = date["weekday"]
    translated_weekday = weekday_dictionary[weekday]
    month = date["month"]
    formatted_month = "{:0>2}".format(month)
    day = date["day"]
    formatted_day = "{:0>2}".format(day)
    msg = f"{translated_weekday} {formatted_month}/{formatted_day}"
    return msg

def hour_translation(hour: int) -> str:
    number_dictionary = {
        0: ":zero:",
        1: ":one:",
        2: ":two:",
        3: ":three:",
        4: ":four:",
        5: ":five:",
        6: ":six:",
        7: ":seven:",
        8: ":eight:",
        9: ":nine:",
        10: ":keycap_ten:",
        11: "<:eleven:1323325078946975845>",
        12: "<:twelve:1323325154528464977>",
        13: "<:thirteen:1323325315170304010>",
        14: "<:fourteen:1323325556980318219>",
        15: "<:fifteen:1323325893942181969>",
        16: "<:sixteen:1323325957502930977>",
        17: "<:seventeen:1323326016072061008>",
        18: "<:eighteen:1323326094346162206>",
        19: "<:nineteen:1323326149945851964>",
        20: "<:twenty:1323326226017816657>",
        21: "<:twenty_one:1323326290425544725>",
        22: "<:twenty_two:1323326382830256159>",
        23: "<:twenty_three:1323326503060242433>"
    }
    translated_hour = number_dictionary[hour]
    return translated_hour

def moon_translation(moon_phase: str, moon_percentage: str) -> str:
    waxing_list = ["Waxing Crescent", "First Quarter", "Waxing Gibbous"]
    # waning_list = ["Waning Gibbous", "Third Quarter", "Waning Crescent"]
    phase_list = [
        (95, 100, "<:moon_full:1329814215892009010>", "<:moon_full:1329814215892009010>"),
        (82,  94, "<:moon_waxing_88:1329814217678651526>", "<:moon_waning_88:1329814214256103487>"),
        (70,  81, "<:moon_waxing_75:1329814219494785054>", "<:moon_waning_75:1329814212381507635>"),
        (57,  69, "<:moon_waxing_63:1329854192256417924>", "<:moon_waning_63:1329814210036764723>"),
        (43,  56, "<:moon_waxing_50:1329854193934012508>", "<:moon_waning_50:1329814208149454848>"),
        (32,  42, "<:moon_waxing_38:1329854195473322025>", "<:moon_waning_38:1329814206362681424>"),
        (20,  31, "<:moon_waxing_25:1329854197029666947>", "<:moon_waning_25:1329814204630175859>"),
        ( 7,  19, "<:moon_waxing_13:1329854198770307224>", "<:moon_waning_13:1329814202986008576>"),
        ( 0,   6, "<:moon_new:1329814201295966339>", "<:moon_new:1329814201295966339>")
    ]
    
    is_waxing = moon_phase in waxing_list
    percentage = int(moon_percentage.strip("%"))
    for start, end, waxing_moon, waning_moon in phase_list:
        if start <= percentage <= end:
            if is_waxing:
                return waxing_moon
            else:
                return waning_moon
            
    return ":face_with_raised_eyebrow:" # Error if the function retruns here

def order_to_hour(order: int) -> int:
    hour_order = [
        12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
    ]
    hour = hour_order[order]
    return hour

def print_max_time(method: str) -> list:
    data = get_data()
    time_and_qualities = []
    for d in data:
        time_and_qualities += d["time_and_quality"]
    
    head_day, current_day = 0, 0
    head_time, previous_time = 0, 0
    current_max_hour = 0
    is_first = True
    is_continue = False
    has_find_any = False

    find_list = []
    for time, quality in time_and_qualities:
        time = int(time)
        astro_dark_start = int(data[current_day]["astro_dark"][0])
        astro_dark_end = int(data[current_day]["astro_dark"][1])
        if (quality == "Good") and (time >= astro_dark_start or time <= astro_dark_end):
            if is_first:
                head_day = current_day
                head_time = time
                is_first = False
                has_find_any = True
            previous_time = time
            current_max_hour += 1
            is_continue = True
        else:
            need_storing: bool = (method == 'a') or (current_max_hour >= 5)
            if is_continue:
                if need_storing:
                    find_dict = {}
                    find_dict["start_day"] = data[head_day]["date"]
                    # find_dict["end_day"] = data[current_day]["date"]
                    find_dict["start_time"] = head_time
                    find_dict["end_time"] = previous_time
                    find_dict["max_hour"] = current_max_hour
                    find_dict["moon_phase"] = data[head_day]["moon_phase"]
                    find_dict["moon_percentage"] = data[head_day]["moon_percentage"]
                    find_list.append(find_dict)
                current_max_hour = 0
                is_first = True
                is_continue = False
            else:
                pass

        if time == 11:
            current_day += 1
    
    need_storing: bool = (method == 'a') or (current_max_hour >= 5)
    if is_continue and need_storing:
        find_dict = {}
        find_dict["start_day"] = data[head_day]["date"]
        # find_dict["end_day"] = data[current_day - 1]["date"]
        find_dict["start_time"] = head_time
        find_dict["end_time"] = previous_time
        find_dict["max_hour"] = current_max_hour
        find_dict["moon_phase"] = data[head_day]["moon_phase"]
        find_dict["moon_percentage"] = data[head_day]["moon_percentage"]
        find_list.append(find_dict)

    message_list = []
    quote = tools.get_quote()
    if not find_list:
        if not has_find_any:
            data_not_found_message = quote["print_max_time_data_not_found"]
            choose_message = randint(0, 1)
            message_list.append(data_not_found_message[choose_message])
        else: # has find data, but mode = "standard" => max hour < 5hr
            data_not_standard_message = quote["print_max_time_data_not_standard"]
            message_list.append(data_not_standard_message[0])
    else:
        for info in find_list:
            max_hour = "{:<2}hr".format(info["max_hour"])
            start_day = date_translation(info["start_day"])
            # end_day = day_translation(info["end_day"])
            start_time = "{:0>2}:00".format(info["start_time"])
            end_time = "{:0>2}:00".format(info["end_time"])
            moon_phase = moon_translation(info["moon_phase"], info["moon_percentage"])
            moon_percentage = info["moon_percentage"]
            max_time_message = (
                f"`{max_hour}` `{start_day} {start_time} ~ {end_time}` | {moon_phase} `{moon_percentage}`"
            )
            message_list.append(max_time_message)
    return message_list

def print_time_table(limit_days: int, method: str) -> list:
    data = get_data()
    print_days = [False] * limit_days
    if method == 's':
        for day, d in enumerate(data):
            time_and_quality = d["time_and_quality"]
            
            max_hour = 0
            is_standard = False
            for hour, quality in time_and_quality:
                hour = int(hour)
                astro_dark_start = int(data[day]["astro_dark"][0])
                astro_dark_end = int(data[day]["astro_dark"][1])
                if (quality == "Good") and (hour >= astro_dark_start or hour <= astro_dark_end):
                    max_hour += 1
                    if max_hour == 3:
                        is_standard = True
                        break
                else:
                    max_hour = 0
                    continue
            
            if is_standard:
                print_days[day] = True
                if 0 < day:
                    print_days[day - 1] = True
                if day < limit_days - 1:
                    print_days[day + 1] = True
    else:
        print_days = [True] * limit_days
    
    is_all_invisible = False
    if not any(print_days):
        is_all_invisible = True
    
    message_list = []
    quote = tools.get_quote()
    if is_all_invisible:
        message_list.append(quote["print_time_table_data_not_standard"][0])
        return message_list
    for today, d in enumerate(data):
        one_day_message = []
        
        #處理星期與日期
        translated_date = date_translation(d["date"])
        day_message = f">>> `{translated_date}`"
        #處理月亮
        translated_moon_phase = moon_translation(d["moon_phase"], d["moon_percentage"])
        moon_percentage = d["moon_percentage"]
        formatted_moon_percentage = "`{:0>3}`".format(moon_percentage)
        moon_message = " ".join([translated_moon_phase, formatted_moon_percentage])
        one_day_message.append(f"{day_message} | {moon_message}")

        if not print_days[today]:
            message_list += one_day_message
            continue
        
        astro_dark_start = int(data[today]["astro_dark"][0])
        astro_dark_end = int(data[today]["astro_dark"][1])
        #處理時間表
        # source: https://emoji.gg/pack/4123-keycap-emoji-11-to-42#
        time_table = []
        for hour in range(astro_dark_start, 24):
            translated_hour = hour_translation(hour)
            time_table.append(translated_hour)
        for hour in range(0, astro_dark_end + 1):
            translated_hour = hour_translation(hour)
            time_table.append(translated_hour)
        time_message = "  ".join(time_table)
        one_day_message.append(time_message)

        #處理品質
        quality_table = []
        if not d["time_and_quality"]:
            for _ in range(0, astro_dark_start - astro_dark_end + 1):
                quality_table.append(":cross_mark:")
        else:
            for time, quality in d["time_and_quality"]:
                time = int(time)
                if not (time >= astro_dark_start or time <= astro_dark_end):
                    continue
                if quality == "Bad":
                    quality_table.append(":red_circle:")
                elif quality == "OK":
                    quality_table.append(":orange_circle:")
                else:
                    quality_table.append(":green_circle:")
        quality_message = "  ".join(quality_table)
        one_day_message.append(quality_message)

        message_list.append("\n".join(one_day_message))
    return message_list
