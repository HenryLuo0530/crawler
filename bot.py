import discord
from discord.ext import commands
from random import randint
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

import crawler
import tools
import seeings

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

async def report():
    crawler_ststus_code = crawler.seeing_crawl(7, 25.17, 121.56)
    message_list = seeings.print_max_time("s")
    message_list.insert(0, "This is a Migu auto report")
    channel = await bot.fetch_channel(setting["CHANNEL_ID"])
    for message in message_list:
        await channel.send(message)

@bot.event
async def on_ready():
    setting = tools.get_setting()
    quote = tools.get_quote()
    print("[I] Bot is online")
    print(f"[I] Using {setting["Language"]} as bot language")
    channel = await bot.fetch_channel(setting["CHANNEL_ID"])
    await channel.send(quote["on_ready"])

    scheduler = AsyncIOScheduler()
    scheduler.add_job(report, CronTrigger(minute="0"))
    scheduler.start()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if(message.content in ["Migu", "ミグ"]):
        quote = tools.get_quote()
        channel = await bot.fetch_channel(setting["CHANNEL_ID"])
        await channel.send(quote["on_message"]["Migu"])
    await bot.process_commands(message)

@bot.event
async def on_message_delete(message):
    setting = tools.get_setting()
    quote = tools.get_quote()
    channel = await bot.fetch_channel(setting["CHANNEL_ID"])
    message = " ".join([quote["on_message_delete"], message.content])
    await channel.send(message)

@bot.command()
async def language(ctx, set_language):
    set_language_status = tools.set_language(set_language)
    quote = tools.get_quote()
    language = tools.get_language()
    if set_language_status == 0:
        await ctx.send(quote["language"]["changed"])
        print(f"[S] Change bot language to {language}")
    else:
        await ctx.send(quote["language"]["failed"])
        print(f"[E] Fail to change the language, using {language} instead")

@bot.command()
async def ping(ctx):
    quote = tools.get_quote()
    message = " ".join([
        quote["ping"][0], f"{round(bot.latency*1000)}", quote["ping"][1]
    ])
    await ctx.send(message)

@bot.command()
async def seeing(ctx, limit_days="7", types="1", method="s", latitude="25.17", longitude="121.56"):
    quote = tools.get_quote()
    input_status_code = seeings.check_input(limit_days, types, method, latitude, longitude)
    if input_status_code > 0:
        await ctx.send(quote["seeing_input_status_code"][input_status_code])
        return
    else:
        limit_days, types = int(limit_days), int(types)
        method = str(method)
        latitude, longitude = float(latitude), float(longitude)

    crawler_ststus_code = crawler.seeing_crawl(limit_days, latitude, longitude)
    if crawler_ststus_code > 0:
        await ctx.send(quote["seeing_crawler_status_code"][1])
        return
    
    match types:
        case 0:
            message_list = seeings.print_max_time(method)
            for message in message_list:
                await ctx.send(message)
        case 1:
            message_list = seeings.print_time_table(limit_days, method)
            for message in message_list:
                await ctx.send(message)

@bot.command()
async def coin(ctx):
    coin = randint(0, 100)
    coin_file: discord.File 
    if coin == 0:
        coin_file = discord.File('./image/coin_angry.jpg')
    elif 1 <= coin <= 50:
        coin_file = discord.File('./image/coin_head.jpg')
    else: # 51 <= coin <= 100:
        coin_file = discord.File('./image/coin_tail.jpg')
    await ctx.send(str(coin))
    await ctx.send(file = coin_file)

if __name__ == "__main__":
    setting = tools.get_setting()
    bot.run(setting["TOKEN"])