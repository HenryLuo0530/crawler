import discord
from discord.ext import commands

class HelpCommand(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        colour = discord.Colour.from_str("#86cecb")
        embed = discord.Embed(title="Migu is helping you", colour=colour)
        for cog, commands in mapping.items():
            if cog is None or commands is None:
                continue

            cog_name = getattr(cog, 'qualified_name', 'No Category')  # 默認名稱
            command_list = [cmd.name for cmd in commands if not cmd.hidden]
            if not command_list:
                continue

            command_str = ", ".join(command_list)
            if len(command_str) > 1024:  # 避免字段內容超過 Discord 限制
                command_str = command_str[:1021] + "..."

            embed.add_field(name=cog_name, value=command_str, inline=False)

        # 確認嵌入是否超出總字符限制
        if len(embed.fields) == 0:
            embed.description = "No commands available."
        elif len(embed.to_dict()) > 6000:
            embed.clear_fields()
            embed.description = "Too many commands to display. Please specify a category."

        await self.context.send(embed=embed)

    async def send_command_help(self, command):
        """This is triggered when !help <command> is invoked."""
        await self.context.send("This is the help page for a command")

    async def send_group_help(self, group):
        """This is triggered when !help <group> is invoked."""
        await self.context.send("This is the help page for a group command")

    async def send_cog_help(self, cog: commands.Cog):
        colour = discord.Colour.from_str("#137a7f")
        title = cog.qualified_name
        description = ""
        if not cog.description:
            description = "No description"
        else:
            description = cog.description 
        embed = discord.Embed(title=title, colour=colour, description=description)
        command_list = [cmd.name for cmd in cog.walk_commands()]
        command_str = ""
        if not command_list:
            command_str = "No command"
        else:
            command_str = ", ".join(command_list)
        embed.add_field(name="command(s):", value=command_str, inline=False)
        await self.context.send(embed=embed)

    async def send_error_message(self, error):
        """If there is an error, send a embed containing the error."""
        channel = self.get_destination() # this defaults to the command context channel
        await channel.send(error)

async def setup(bot):
    bot.help_command = HelpCommand()