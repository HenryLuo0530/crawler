from random import randint

def day_translation(day_and_date: str) -> str:
    day_dictionary = {
        "Monday"   : "星期一",
        "Tuesday"  : "星期二",
        "Wednesday": "星期三",
        "Thursday" : "星期四",
        "Friday"   : "星期五",
        "Saturday" : "星期六",
        "Sunday"   : "星期日"
    }
    time_list = day_and_date.split(" ")
    day = time_list[0]
    date = time_list[1]
    translated_day = day_dictionary[day]
    msg = translated_day + " " + date
    return msg

def check_input(limit_days: int, mode: int, latitude: float, longitude: float) -> int:
    if (limit_days < 1):
        return 1
    elif (limit_days > 7):
        return 2

    if not(0 <= mode <= 1):
        return 3
    
    return 0

def find_max_time(data: list) -> list:
    day_and_dates = []
    time_and_qualities = []
    for d in data:
        day_and_dates.append(d["dates"])
        time_and_qualities += d["time_and_quality"]
    
    current_day, head_day = 0, 0
    head_time, previous_time = 0, 0
    current_max_hour = 0
    is_first = True
    is_continue = False

    find_list = []
    for tq in time_and_qualities:
        time_and_quality = tq.split(" ")
        time = int(time_and_quality[1])
        quality = time_and_quality[2]
        if (quality == "Good") and (not (6 <= time <= 17)):
            if is_first:
                head_day = current_day
                head_time = time
                is_first = False
            previous_time = time
            current_max_hour += 1
            is_continue = True
        else:
            if is_continue:
                find_dict = {}
                find_dict["start_day"] = day_and_dates[head_day]
                find_dict["end_day"] = day_and_dates[current_day]
                find_dict["start_time"] = head_time
                find_dict["end_time"] = previous_time
                find_dict["max_hour"] = current_max_hour
                find_list.append(find_dict)
                current_max_hour = 0
                is_first = True
                is_continue = False
            else:
                pass

        if time == 23:
            current_day += 1
    
    if is_continue:
        find_dict = {}
        find_dict["start_day"] = day_and_dates[head_day]
        find_dict["end_day"] = day_and_dates[current_day - 1]
        find_dict["start_time"] = head_time
        find_dict["end_time"] = previous_time
        find_dict["max_hour"] = current_max_hour
        find_list.append(find_dict)

    message_list = []
    if not find_list:
        data_not_found_message = [
            "Oh no! Migu canNOT find good hours!",
            "Oh wow! Migu see beautiful clouds!"
        ]
        choose_message = randint(0, 1)
        message_list.append(data_not_found_message[choose_message])
    else:
        for info in find_list:
            translated_start_day = day_translation(info["start_day"])
            translated_end_day = day_translation(info["end_day"])
            max_time_message = f"{translated_start_day} {info["start_time"]}:00 ~ {translated_end_day} {info["end_time"]}:00 max {info["max_hour"]}hr"
            message_list.append(max_time_message)
    return message_list

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

def print_time_table(data: list) -> list:
    message_list = []
    for d in data:
        one_day_message = []
        translated_day = day_translation(d["dates"])
        one_day_message.append(translated_day)
        # source: https://emoji.gg/pack/4123-keycap-emoji-11-to-42#
        time_table = ["=>"]
        for hour in range(0, 24):
            translated_hour = hour_translation(hour)
            time_table.append(translated_hour)
        time_message = "  ".join(time_table)
        one_day_message.append(time_message)

        quality_table = ["=>"]
        if not d["time_and_quality"]:
            for _ in range(0, 24):
                quality_table.append(":cross_mark:")
        else:
            for tq in d["time_and_quality"]:
                time_and_quality = tq.split(" ")
                # time = time_and_quality[1]
                quality = time_and_quality[2]
                if quality == "Bad":
                    quality_table.append(":red_circle:")
                elif quality == "OK":
                    quality_table.append(":orange_circle:")
                else:
                    quality_table.append(":green_circle:")
        quality_message = "  ".join(quality_table)
        one_day_message.append(quality_message)
        message_list += one_day_message
    return message_list
