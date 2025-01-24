import sys
import os
import logging
import asyncio

import discord
from discord.ext import commands

from extension import tools, bot_logger

sys.path.append('.')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
logger = logging.getLogger(__name__)

@bot.event
async def on_ready():
    is_normal_shutdown = bot_logger.check_shutdown(logger)

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
    bot_logger.log_setup()

    setting = tools.get_setting()
    bot.owner_id = setting["OWNER_ID"]
    async with bot:
        await load()
        await bot.start(setting["TOKEN"])

if __name__ == "__main__":
    asyncio.run(main())