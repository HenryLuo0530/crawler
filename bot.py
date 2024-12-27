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
    print("Bot is online")

@bot.command()
async def ping(ctx):
    await ctx.send(f'{round(bot.latency*1000)} (ms)')

@bot.command()
async def seeing(ctx, limit_days=3, mode=1, latitude=25.17, longitude=121.56):
    if(limit_days >= 7): limit_days = 7
    elif(limit_days <= 1): limit_days = 1
    data = crawler.crawl(limit_days, latitude, longitude)
    for d in data:
        day_and_date = d["dates"].split(" ")
        day = day_and_date[0]
        date = day_and_date[1]
        translated_day = tools.dayTranslation(day)
        day_and_date_message = translated_day + " " + date
        await ctx.send(day_and_date_message)
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