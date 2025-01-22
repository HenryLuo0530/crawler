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
    is_normal_shutdown: bool
    try:
        with open("last_log.log", "r", encoding="utf-8") as log_file:
            for line in log_file:
                pass
            last_log = line
            if "[I] Bot has been shutted down" in last_log:
                is_normal_shutdown = True
            else:
                is_normal_shutdown = False
    except OSError:
        logger.warning("[W] last_log not found")
        is_normal_shutdown = True
    except Exception as error:
        logger.exception(error)
        is_normal_shutdown = True

    setting = tools.get_setting()
    quote = tools.get_quote()
    channel = await bot.fetch_channel(setting["CHANNEL_ID"])
    if not is_normal_shutdown:
        logger.warning("[W] Bot shutted down unexpectedly during the last session")
        await channel.send("What just happend :dizzy_face:")
    logger.info("[I] Bot is online")
    logger.info(f"[I] Using {setting["Language"]} as bot language")
    await channel.send(quote["on_ready"])

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    try:
        os.replace("log.log", "last_log.log")
    except OSError:
        print("WARNING [W] log not found")
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(
        filename="log.log",
        mode='a',
        maxBytes=1024 * 2,
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