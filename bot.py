from ro_py import Client # Roblox API library

# Discord API Wrapper
import discord
from discord.ext import commands

# Discord.py Extention for Slash Commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option

from purgo_malum import client as filterClient # Profanity filter library

import config
client = Client(config.robloxAccountCookie)

bot = commands.Bot(command_prefix=config.discordBotPrefix, help_command=None)
slash = SlashCommand(bot, sync_commands=True)

@slash.slash(name="shout",
                description="Shout to the Southlink roblox group.",
                options=[
                create_option(
                name="text",
                description="The text you would like to post to the shout.",
                option_type=3,
                required=True
                ),
                create_option(
                name="filter_override",
                description="If you are an admin you may use this to override the profanity filter.",
                option_type=5,
                required=False
                )], guild_ids=config.guildIds)
@commands.has_permissions(manage_guild=True) # This determines what permission(s) a user requires to use the command, more info: https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#discord.ext.commands.has_permissions & https://discordpy.readthedocs.io/en/stable/api.html#discord.Permissions
async def shout(ctx, text: str, filter_override: bool=False):
    if filterClient.contains_profanity(text) == True and not (filter_override == True and ctx.author.guild_permissions.administrator) and config.profanityFilterOn == True:
        await ctx.send(content='Shout failed, profanity detected.', hidden=True)
        return
    try:
        group = await client.get_group(config.groupId)
        if group.shout == None:
            await group.update_shout(text) # This is outdated, but used if a shout is not present as group.shout() returns an error. There might be a better way of doing this, but this works consistently, at least according to my testing.
        else:
            await group.shout(text)
    except:
        await ctx.send(content='Shout failed.', hidden=True)
    else:
        await ctx.send(content='Shout success.', hidden=True)

bot.run(config.developmentDiscordToken)