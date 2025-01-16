import platform
from datetime import datetime
import discord
from discord.ext import commands

from extension import tools, video_search

class Question(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def who(self, ctx):
        quote = tools.get_quote()
        await ctx.send(quote["question"]["who"])

    @commands.command()
    async def what(self, ctx):
        quote = tools.get_quote()
        await ctx.send(quote["question"]["what"])

    @commands.command()
    async def when(self, ctx):
        now = datetime.now().strftime("%Y %m/%d %H:%M:%S")
        await ctx.send(f"{now}")

    @commands.command()
    async def where(self, ctx):
        machine = platform.platform()
        quote = tools.get_quote()
        message = " ".join([
            quote["question"]["where"][0], machine, quote["question"]["where"][1]
        ])
        await ctx.send(message)

    @commands.command()
    async def why(self, ctx):
        quote = tools.get_quote()
        await ctx.send(quote["question"]["why"])
    
    @commands.command()
    async def how(self, ctx, *arg):
        if len(arg) == 0:
            await ctx.send("How?")
            return
        keyword_list = ["How"] + list(arg)
        keywords = " ".join(keyword_list)
        video_link = video_search.youtube_search(keywords)
        await ctx.send(video_link)

async def setup(bot):
    await bot.add_cog(Question(bot))