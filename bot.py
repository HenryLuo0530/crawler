import discord
from discord.ext import commands
import json
import crawler
import tools

with open("setting.json", "r", encoding="utf-8") as file:
    setting = json.load(file)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print("[S] Bot is online")

@bot.command()
async def ping(ctx):
    await ctx.send(f'{round(bot.latency*1000)} (ms)')

@bot.command()
async def seeing(ctx, limit_days=3, mode=1, latitude=25.17, longitude=121.56):
    if(limit_days >= 7): limit_days = 7
    elif(limit_days <= 1): limit_days = 1

    ststus_code = crawler.crawl(limit_days, latitude, longitude)
    if (ststus_code == 1):
        await ctx.send("Sorrgy accident... Migu broke the web")
        return
    with open("seeings.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    if mode == 0:
        day_and_dates = []
        time_and_qualities = []
        for d in data:
            day_and_dates.append(d["dates"])
            time_and_qualities += d["time_and_quality"]
        print(day_and_dates)
        print(time_and_qualities)
        
        current_day = 0
        head_day = 0

        head_time = 0
        previous_time = 0

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
            
            if (time == 23):
                current_day += 1
        
        if is_continue:
            find_dict = {}
            find_dict["start_day"] = day_and_dates[head_day]
            find_dict["end_day"] = day_and_dates[current_day - 1]
            find_dict["start_time"] = head_time
            find_dict["end_time"] = previous_time
            find_dict["max_hour"] = current_max_hour
            find_list.append(find_dict)

        if not find_list:
            await ctx.send("Oh no! Migu canNOT find good hours!")
        else:
            for info in find_list:
                msg = f'{info["start_day"]} {info["start_time"]}:00 ~ {info["end_day"]} {info["end_time"]}:00 max {info["max_hour"]}hr'
                await ctx.send(msg)

    elif mode == 1:
        for d in data:
            translated_day_date = tools.dayTranslation(d["dates"])
            await ctx.send(translated_day_date)
            time_table = "=> 00    01   02    03   04   05   06    07   08   09   10     11     12    13    14    15    16     17    18    19    20    21    22   23"
            await ctx.send(time_table)
            msg = "=> "
            for tq in d["time_and_quality"]:
                time_and_quality = tq.split(" ")
                time = time_and_quality[1]
                quality = time_and_quality[2]
                if quality == "Bad":
                    msg += ":red_circle:  "
                elif quality == "OK":
                    msg += ":orange_circle:  "
                else:
                    msg += ":green_circle:  "
            await ctx.send(msg)

bot.run(setting["TOKEN"])