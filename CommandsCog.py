from discord import ApplicationContext as Context
from discord import Bot, Member, Option, guild_only, slash_command
from discord.ext.commands import Cog, CommandError

from models import ChannelData

test_guilds = [1218937664351240232]


def get_nick_or_name(member: Member):
    if member.nick is not None:
        return member.nick
    return member.name


class CommandsCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(
        name="count",
        description="Se timmar för en användare.",
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
            await ctx.respond("Kanalen har inga registrerade timmar.")
            return

        nick = "Du" if member_was_none else get_nick_or_name(member)

        if member.id not in channel_data.counts.counts:
            await ctx.respond(f"{nick} har inga timmar.")
            return
        count = channel_data.counts.counts[member.id]

        await ctx.respond(f"{nick}, {count:.2f} timmar.")

    @slash_command(
        name="counts",
        description="Se allas timmar för en kanal.",
        test_guilds=test_guilds,
    )
    @guild_only()
    async def counts(
        self,
        ctx: Context,
    ):
        channel_data = await ChannelData.fetch(ctx.channel.id)
        if channel_data == None:
            await ctx.respond("Kanalen har inga registrerade timmar.")
            return

        rows = []
        for member_id, count in channel_data.counts.counts.items():
            nick = get_nick_or_name(ctx.guild.get_member(member_id))
            rows.append(f"{nick}, {count:.2f} timmar")

        await ctx.respond("\n".join(rows))

    async def cog_command_error(self, ctx: Context, error: CommandError):
        raise error  # Here we raise other errors to ensure they aren't ignored
