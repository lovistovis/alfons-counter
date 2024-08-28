from discord import ApplicationContext as Context
from discord import Bot, Member, Option, guild_only, slash_command
from discord.ext.commands import Cog, CommandError

from models import ChannelData

test_guilds = []


class CommandsCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(
        name="count",
        description="Se siffran för en användare.",
        test_guilds=test_guilds,
    )
    @guild_only()
    async def count(
        self,
        ctx: Context,
        member: Option(
            Member,
            required=False,
            default=None,
            name="user",
            description="Användaren (default dig själv).",
        ),
    ):
        if member_was_none := member == None:
            member = ctx.user

        channel_data = await ChannelData.fetch(ctx.channel.id)
        if channel_data == None:
            await ctx.respond("Kanalen har inga registrerade siffror.")
            return

        nick = "Du" if member_was_none else member.nick

        if member.id not in channel_data.counts.counts:
            await ctx.respond(f"{nick} har ingen siffra.")
            return
        count = channel_data.counts.counts[member.id]

        await ctx.respond(f"{nick} har siffran {count}.")

    async def cog_command_error(self, ctx: Context, error: CommandError):
        raise error  # Here we raise other errors to ensure they aren't ignored
