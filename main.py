from datetime import datetime
import os

import discord
from dotenv import load_dotenv
from discord import app_commands
from bot.db import Q
from bot.utils import validate_date

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@tree.command(
    name="add",
    description="Add your happy birthday",
)
async def add_happy_birthday(interaction: discord.Interaction, date: str):
    if Q("bot.db").check_user_happy_birthday_is_exists(interaction.user.name):
        await interaction.response.send_message("Your happy birthday is added to update use !rewrite")
    elif validate_date(date):
        Q("bot.db").add_user_hb(interaction.user.name, datetime.strptime(date, "%d.%m.%y"))
        await interaction.response.send_message("Your happy birthday is added")
    else:
        await interaction.response.send_message("date format in not correct use dd.mm.yy")


@tree.command(
    name="get",
    description="Get your happy birthday",
)
async def get_happy_birthday(interaction: discord.Interaction):
    await interaction.response.send_message(
        "Your happy birthday in %s. %s left until your happy birthday" % Q("bot.db").get_user_hb(interaction.user.name)
    )


@tree.command(
    name="rewrite",
    description="Rewrite your happy birthday",
)
async def rewrite_happy_birthday(interaction: discord.Interaction, date: str):
    if not validate_date(date):
        await interaction.response.send_message("date format in not correct use dd.mm.yy")
        return
    else:
        Q("bot.db").update_user_hb(interaction.user.name, datetime.strptime(date, "%d.%m.%y"))
        await interaction.response.send_message("Your happy birthday is updated")


@client.event
async def on_ready():
    Q("bot.db").create_tables()
    await tree.sync()
    print(f"We have logged in as {client.user}")


if __name__ == "__main__":
    load_dotenv()
    client.run(token=os.getenv("TOKEN"))
