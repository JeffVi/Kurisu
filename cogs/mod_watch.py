import discord

from discord.ext import commands
from utils import utils, crud
from utils.checks import is_staff
from textwrap import wrap


class Modwatch(commands.Cog):
    """
    User watch management commands.
    """

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if ctx.guild is None:
            raise commands.NoPrivateMessage()
        return True

    @is_staff("Helper")
    @commands.command()
    async def watch(self, ctx, member: discord.Member, *, reason=""):
        if await crud.is_watched(member.id):
            await ctx.send("User is already being watched!")
            return
        await crud.add_watch(member.id)
        await ctx.send(f"{member.mention} is being watched.")
        msg = f"👀 **Watch**: {ctx.author.mention} put {member.mention} on watch | {member}"
        if reason != "":
            # much \n
            msg += "\n✏️ __Reason__: " + reason
        signature = utils.command_signature(ctx.command)
        await self.bot.channels['mod-logs'].send(msg + (
            f"\nPlease add an explanation below. In the future, it is recommended to use `{signature}` as the reason is very useful for saving time." if reason == "" else ""))
        await self.bot.channels['watch-logs'].send(msg + (
            "\nNo reason provided." if reason == "" else ""))

    @is_staff("Helper")
    @commands.command()
    async def unwatch(self, ctx, member: discord.Member):
        if not await crud.is_watched(member.id):
            await ctx.send("This user was not being watched.")
            return
        await crud.remove_watch(member.id)
        await ctx.send(f"{member.mention} is no longer being watched.")
        msg = f"❌ **Unwatch**: {ctx.author.mention} removed {member.mention} from watch | {self.bot.escape_text(member)}"
        await self.bot.channels['mod-logs'].send(msg)
        await self.bot.channels['watch-logs'].send(msg)

    @is_staff("Helper")
    @commands.command()
    async def listwatch(self, ctx):
        watchlist = await crud.get_watch_list()
        lines = []
        for db_member in watchlist:
            member = ctx.guild.get_member(db_member.id)
            lines.append(f"{f'{member.name}' if member else f'<@{db_member.id}>'} ({db_member.id})")
        messages = wrap('\n'.join(lines), 1810, break_long_words=False, replace_whitespace=False)
        if not messages:
            await ctx.send("The watchlist is empty!")
            return
        if (n_messages := len(messages)) > 1:
            for n, message in enumerate(messages, start=1):
                await ctx.author.send(f"**Watchlist contents {n}/{n_messages}**\n{message}")
        else:
            await ctx.author.send(f"**Watchlist contents**\n{messages[0]}")

    @is_staff("OP")
    @commands.command()
    async def watch_cleanup(self, ctx):
        removed = 0
        watchlist = await crud.get_watch_list()
        for member in watchlist:
            if not ctx.guild.get_member(member.id):
                await crud.remove_watch(member.id)
                removed += 1
        await ctx.send(f"Watch list cleanup complete. Removed {removed} entries.")


def setup(bot):
    bot.add_cog(Modwatch(bot))
