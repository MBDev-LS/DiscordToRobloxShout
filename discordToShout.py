from ro_py import Client
import discord
from discord.ext import commands
from discord_slash import SlashCommand # Importing the newly installed library.
from discord_slash.utils.manage_commands import create_option

from purgo_malum import client as filterClient

import config
client = Client(config.robloxAccountCookie)

bot = commands.Bot(command_prefix='?', help_command=None)
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
                )], guild_ids=[534404907315494972])
async def shout(ctx, text: str, filter_override: bool=False):
    if filterClient.contains_profanity(text) == True and not (filter_override == True and ctx.author.guild_permissions.administrator):
        await ctx.send(content='Shout failed, profanity detected.', hidden=True)
        return
    try:
        group = await client.get_group(config.groupId)
        if group.shout == None:
            await group.update_shout(text)
        else:
            await group.shout(text)
    except:
        await ctx.send(content='Shout failed.', hidden=True)
    else:
        await ctx.send(content='Shout success.', hidden=True)

bot.run(config.developmentDiscordToken)