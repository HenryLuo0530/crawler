import discord
from discord.ext import commands

from extension import tools

class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if(message.content in ["Migu", "ミグ"]):
            setting = tools.get_setting()
            quote = tools.get_quote()
            channel = await self.bot.fetch_channel(setting["CHANNEL_ID"])
            await channel.send(quote["on_message"]["Migu"])

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        setting = tools.get_setting()
        quote = tools.get_quote()
        channel = await self.bot.fetch_channel(setting["CHANNEL_ID"])
        message = " ".join([quote["on_message_delete"], message.content])
        await channel.send(message)

async def setup(bot):
    await bot.add_cog(Event(bot))