import os

from discord import Bot, Intents
from dotenv import load_dotenv

from CommandsCog import CommandsCog
from EventsCog import EventsCog

intents = Intents.default()
intents.presences = True
intents.members = True
intents.message_content = True
bot = Bot(command_prefix="/", intents=intents)


def setup(bot: Bot):
    bot.add_cog(CommandsCog(bot))
    bot.add_cog(EventsCog(bot))


def main():
    load_dotenv()
    token = os.getenv("TOKEN")
    assert (
        token != None
    ), 'Set the bot token in a .env file in the project root in the form `TOKEN="XXXXXXXX..."`'
    setup(bot)
    bot.run(token)


if __name__ == "__main__":
    main()
