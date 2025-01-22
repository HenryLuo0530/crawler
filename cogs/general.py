from random import randint
import logging
import discord
from discord.ext import commands

from extension import tools

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)
    
    @commands.command(hidden=True)
    async def shutdown(self, ctx):
        setting = tools.get_setting()
        quote = tools.get_quote()
        if ctx.author.id != setting["OWNER_ID"]:
            await ctx.send(quote["shutdown"]["denied"])
            return
        await ctx.send(quote["shutdown"]["succeeded"])
        await self.bot.close()
        self.logger.info("[I] Bot has been shutted down")

    @commands.command()
    async def language(self, ctx, set_language):
        set_language_status = tools.set_language(set_language)
        quote = tools.get_quote()
        language = tools.get_language()
        if set_language_status == 0:
            await ctx.send(quote["language"]["changed"])
            self.logger.info(f"[I] Change bot language to {language}")
        else:
            await ctx.send(quote["language"]["failed"])
            self.logger.info(f"[I] Fail to change the language, using {language} instead")

    @commands.command()
    async def ping(self, ctx):
        quote = tools.get_quote()
        message = " ".join([
            quote["ping"][0], f"{round(self.bot.latency*1000)}", quote["ping"][1]
        ])
        await ctx.send(message)
    
    @commands.command()
    async def coin(self, ctx):
        flip = randint(0, 100)
        coin = [
            ( 0,   0, "coin_angry.png", "by Migu",       "Anggy"),
            ( 1,  50, "coin_head.png",  "by @kyomu_305", "Head"),
            (51, 100, "coin_tail.png",  "by Migu",       "Tail")
        ]
        
        colour = discord.Colour.gold()
        title = str("Migu help you flip a coin")
        embed = discord.Embed(colour=colour, title=title)
        for start, end, file_name, image_author, coin_type in coin:
            if start <= flip <= end:
                file_path = f"./image/{file_name}"
                file = discord.File(file_path)
                embed.description = coin_type
                embed.set_thumbnail(url=f"attachment://{file_name}")
                embed.set_footer(text=image_author)
                await ctx.send(file=file, embed=embed)
                break

async def setup(bot):
    await bot.add_cog(General(bot))