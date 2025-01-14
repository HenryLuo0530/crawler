import os
import discord
from discord.ext import commands
import asyncio

from extension import tools

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    setting = tools.get_setting()
    quote = tools.get_quote()
    print("[I] Bot is online")
    print(f"[I] Using {setting["Language"]} as bot language")
    channel = await bot.fetch_channel(setting["CHANNEL_ID"])
    await channel.send(quote["on_ready"])

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    setting = tools.get_setting()
    bot.owner_id = setting["OWNER_ID"]
    async with bot:
        await load()
        await bot.start(setting["TOKEN"])

if __name__ == "__main__":
    asyncio.run(main())