import discord
from discord.ext import commands
import json
import crawler
import tools
import random

with open("setting.json", "r", encoding="utf-8") as file:
    setting = json.load(file)
with open("quote.json", "r", encoding="utf-8") as file:
    quote = json.load(file)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print("[S] Bot is online")
    channel = await bot.fetch_channel(setting["CHANNEL_ID"])
    await channel.send(quote["on_ready"])

"""
@bot.event
async def on_message(message):
    if(message.content == "Migu"):
        channel = await bot.fetch_channel(setting["CHANNEL_ID"])
        await channel.send("Migu!")
"""

@bot.event
async def on_message_delete(message):
    channel = await bot.fetch_channel(setting["CHANNEL_ID"])
    await channel.send(f"Migu saw you deleted the message:\n >>> {message.content}")

@bot.command()
async def ping(ctx):
    await ctx.send(f'Migu is {round(bot.latency*1000)} years old')

@bot.command()
async def seeing(ctx, limit_days="3", mode="1-s", latitude="25.17", longitude="121.56"):
    input_status_code = 0
    try:
        limit_days = int(limit_days)
        mode = str(mode)
        latitude, longitude = float(latitude), float(longitude)
        input_status_code = tools.check_input(limit_days, mode, latitude, longitude)
    except:
        input_status_code = 10 
    if input_status_code > 0:
        await ctx.send(quote["seeing_input_status_code"][input_status_code])
        return

    crawler_ststus_code = crawler.seeing_crawl(limit_days, latitude, longitude)
    if crawler_ststus_code > 0:
        await ctx.send(quote["seeing_crawler_status_code"][1])
        return
    
    with open("seeings.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    type_and_method = mode.split("-")
    types = int(type_and_method[0])
    method = type_and_method[1]
    match types:
        case 0:
            message_list = tools.find_max_time(data, method)
            for message in message_list:
                await ctx.send(message)
        case 1:
            message_list = tools.print_time_table(data)
            for message in message_list:
                await ctx.send(message)

@bot.command()
async def coin(ctx):
    coin = random.randint(0, 1)
    if coin:
        coin_head = discord.File('./image/coin_head.jpg')
        await ctx.send(file = coin_head)
    else:
        coin_tail = discord.File('./image/coin_tail.jpg')
        await ctx.send(file = coin_tail)

bot.run(setting["TOKEN"])