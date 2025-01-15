import discord
from discord.ext import commands
from random import randint

from extension import tools

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        quote = tools.get_quote()
        await ctx.send(quote["shutdown"])
        await self.bot.close()
        print("[I] Bot has been shutted down")

    @commands.command()
    async def language(self, ctx, set_language):
        set_language_status = tools.set_language(set_language)
        quote = tools.get_quote()
        language = tools.get_language()
        if set_language_status == 0:
            await ctx.send(quote["language"]["changed"])
            print(f"[S] Change bot language to {language}")
        else:
            await ctx.send(quote["language"]["failed"])
            print(f"[E] Fail to change the language, using {language} instead")

    @commands.command()
    async def ping(self, ctx):
        quote = tools.get_quote()
        message = " ".join([
            quote["ping"][0], f"{round(self.bot.latency*1000)}", quote["ping"][1]
        ])
        await ctx.send(message)
    
    @commands.command()
    async def coin(self, ctx):
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

async def setup(bot):
    await bot.add_cog(General(bot))