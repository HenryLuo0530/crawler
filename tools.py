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
    translated_day = day_dictionary[day]
    date = time_list[1]
    formated_date = "{:0>2}".format(date)
    msg = " ".join([translated_day, formated_date])
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

def moon_translation(moon_phase: str) -> str:
    phase_dictionary = {
        "New Moon": ":new_moon:",
        "Waxing Crescent": ":waxing_crescent_moon:",
        "First Quarter": ":first_quarter_moon:",
        "Waxing Gibbous": ":waxing_gibbous_moon:",
        "Full Moon": ":full_moon:",
        "Waning Gibbous": ":waning_gibbous_moon:",
        "Last Quarter": ":last_quarter_moon:",
        "Waning Crescent": ":waning_crescent_moon:"
    }
    translated_moon_phase = phase_dictionary[moon_phase]
    return translated_moon_phase

def print_time_table(data: list) -> list:
    message_list = []
    for d in data:
        one_day_message = []
        
        #處理星期與日期
        translated_day = day_translation(d["dates"])
        day_message = f"`{translated_day}`"
        #處理月亮
        translated_moon_phase = moon_translation(d["moon_phase"])
        moon_percentage = d["moon_percentage"]
        formated_moon_percentage = "`{:0>3}`".format(moon_percentage)
        moon_message = " ".join([translated_moon_phase, formated_moon_percentage])
        one_day_message.append(day_message + " | " + moon_message)

        #處理時間表
        # source: https://emoji.gg/pack/4123-keycap-emoji-11-to-42#
        time_table = ["|"]
        for hour in range(0, 24):
            translated_hour = hour_translation(hour)
            time_table.append(translated_hour)
        time_message = "  ".join(time_table)
        one_day_message.append(time_message)

        #處理品質
        quality_table = ["|"]
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
