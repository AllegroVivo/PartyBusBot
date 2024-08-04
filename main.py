from __future__ import annotations

import os

from discord import Intents
from dotenv import load_dotenv

from Classes.Bot import PartyBusBot
################################################################################

load_dotenv()
debug_guilds = [955933227372122173] if os.getenv("DEBUG") else None

bot = PartyBusBot(
    description="Toot toot, bitches!",
    intents=Intents.all(),
    debug_guilds=debug_guilds
)

################################################################################

for filename in os.listdir("Cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        bot.load_extension(f"Cogs.{filename[:-3]}")

################################################################################

load_dotenv()
bot.run(os.getenv("DISCORD_TOKEN"))

################################################################################
