import os
import logging
from logging.handlers import RotatingFileHandler
import discord
from discord.ext import commands
import asyncio

from extension import tools

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
logger = logging.getLogger(__name__)

@bot.event
async def on_ready():
    setting = tools.get_setting()
    quote = tools.get_quote()
    logger.info("[I] Bot is online")
    logger.info(f"[I] Using {setting["Language"]} as bot language")
    channel = await bot.fetch_channel(setting["CHANNEL_ID"])
    await channel.send(quote["on_ready"])

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(
        filename="log.log",
        mode='a',
        maxBytes=1024 * 4,
        backupCount=0,
        encoding='utf-8',
        delay=False
    )
    handler.setLevel(logging.INFO)
    logging.basicConfig(
        format="%(name)s %(asctime)s %(levelname)s %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[handler]
    )

    setting = tools.get_setting()
    bot.owner_id = setting["OWNER_ID"]
    async with bot:
        await load()
        await bot.start(setting["TOKEN"])

if __name__ == "__main__":
    asyncio.run(main())