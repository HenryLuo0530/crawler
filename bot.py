import discord
from discord.ext import commands
import json
import crawler

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
async def seeing(ctx, days=3, latitude=25.02, longitude=121.54):
    if(days >= 7): days = 7
    data = crawler.crawl(days, latitude, longitude)
    for d in data:
        await ctx.send(f'**{d["date"]}**')
        await ctx.send("=> 00    01   02    03   04   05   06    07   08   09   10     11     12    13    14    15    16     17    18    19    20    21    22   23")
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