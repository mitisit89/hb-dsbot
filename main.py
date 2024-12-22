from datetime import datetime
import os

import discord
from dotenv import load_dotenv

from bot.db import Q
from bot.utils import validate_date

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    Q("bot.db").create_tables()
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message: discord.Message) -> None:
    if message.author == client.user:
        return

    if message.content.startswith("!hb"):
        if Q("bot.db").check_user_happy_birthday_is_exists(message.author.name):
            await message.channel.send("Your happy birthday is added to update use !rewrite")
        elif validate_date(message.content.split()[1]):
            Q("bot.db").add_user_hb(message.author.name, datetime.strptime(message.content.split()[1], "%d.%m.%y"))
            await message.channel.send("Your happy birthday is added")
        else:
            await message.channel.send("date format in not correct use dd.mm.yy")
    if message.content.startswith("!get-hb"):
        await message.channel.send(
            "Your happy birthday in %s. %s left until your happy birthday"
            % Q("bot.db").get_user_hb(message.author.name)
        )
    if message.content.startswith("!rewrite"):
        Q("bot.db").update_user_hb(message.author.name, datetime.strptime(message.content.split()[1], "%d.%m.%y"))
        await message.channel.send("Your happy birthday is updated")
    if message.content.startswith("!help"):
        await message.channel.send(
            "To add your happy birthday use !hb \n"
            "To get your happy birthday use !get-hb\n"
            "To update your happy birthday use !rewrite dd.mm.yy\n"
        )


if __name__ == "__main__":
    load_dotenv()
    client.run(token=os.getenv("TOKEN"))
