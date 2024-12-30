from random import randint

def day_translation(day_and_date: str) -> str:
    dict = {
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
    translated_day = dict[day]
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

def print_time_table(data: list) -> list:
    message_list = []
    for d in data:
        one_day_message = []
        translated_day = day_translation(d["dates"])
        one_day_message.append(translated_day)

        time_table = "=> 00    01   02    03   04   05   06    07   08   09   10     11     12    13    14    15    16     17    18    19    20    21    22   23"
        one_day_message.append(time_table)

        quality_table = "=> "
        for tq in d["time_and_quality"]:
            time_and_quality = tq.split(" ")
            time = time_and_quality[1]
            quality = time_and_quality[2]
            if quality == "Bad":
                quality_table += ":red_circle:  "
            elif quality == "OK":
                quality_table += ":orange_circle:  "
            else:
                quality_table += ":green_circle:  "
        one_day_message.append(quality_table)
        message_list += one_day_message
    return message_list
