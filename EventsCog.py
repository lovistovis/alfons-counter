from discord import Bot, Message
from discord.ext.commands import Cog

from db import create_db
from models import ChannelData


def is_float(string: any) -> bool:
    try:
        float(string)
        return True
    except ValueError:
        return False


def parse_message(message: str) -> int | None:
    sign, num = message[0], message[1:]

    if ((negative := sign == "-") or sign == "+") and is_float(num):
        num = float(num)
        return -num if negative else num
    return None


class EventsCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} has connected to Discord!")

        await create_db()

    @Cog.listener()
    async def on_message(self, message: Message):
        # Only run on messages from non-bot users in a guild
        if message.guild == None or message.author.bot:
            return

        channel_data = await ChannelData.fetch(message.channel.id)
        if channel_data is None:
            channel_data = await ChannelData.create(id=message.channel.id)

        if message.author.id not in channel_data.counts.counts:
            channel_data.counts.counts[message.author.id] = 0
        if (num := parse_message(message.content)) is not None:
            channel_data.counts.counts[message.author.id] += num

        await channel_data.update()
