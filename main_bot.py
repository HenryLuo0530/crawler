import os
import discord
from discord.ext import commands
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from extension import tools, seeings, crawler

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

async def report():
    setting = tools.get_setting()
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
    scheduler.add_job(report, CronTrigger(hour="23"))
    scheduler.start()

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    setting = tools.get_setting()
    async with bot:
        await load()
        await bot.start(setting["TOKEN"])

if __name__ == "__main__":
    asyncio.run(main())