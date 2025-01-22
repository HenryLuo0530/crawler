import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from extension import tools, seeings, crawler

class Astronomical(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.description = "Migu is watching the sky."

    async def report(self):
        setting = tools.get_setting()
        quote = tools.get_quote()
        channel = await self.bot.fetch_channel(setting["CHANNEL_ID"])
        crawler_ststus = crawler.seeing_crawl(7, 25.17, 121.56)
        if crawler_ststus > 0:
            await channel.send(quote["seeing_crawler_status_code"][1])
            return
        message_list = seeings.print_max_time("s")
        message_list.insert(0, quote["report"])
        message = "\n".join(message_list)
        await channel.send(message)

    @commands.Cog.listener()
    async def on_ready(self):
        scheduler = AsyncIOScheduler()
        scheduler.add_job(self.report, CronTrigger(hour="8, 16"))
        scheduler.start()
    
    @commands.command()
    async def seeing(self, ctx, limit_days="3", types="1", method="a", latitude="25.17", longitude="121.56"):
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

async def setup(bot):
    await bot.add_cog(Astronomical(bot))