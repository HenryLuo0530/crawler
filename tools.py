import json

def get_setting() -> dict:
    with open("./json_file/setting.json", "r", encoding="utf-8") as file:
        setting = json.load(file)
    return setting

def get_language() -> str:
    setting = get_setting()
    language = setting["Language"]
    return language

def set_language(language: str) -> int:
    language_list = ["English", "Japanese"]
    if language in language_list:
        setting = get_setting()
        setting["Language"] = language
        with open("./json_file/setting.json", "w", encoding="utf-8") as file:
            json.dump(setting, file, ensure_ascii=False, indent=4)
        return 0
    else:
        return 1

def get_quote() -> dict:
    language = get_language()
    with open(f"./json_file/{language}_quote.json", "r", encoding="utf-8") as file:
        quote = json.load(file)
    return quote
