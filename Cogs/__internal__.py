from __future__ import annotations

from discord import Cog
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Classes.Bot import PartyBusBot
################################################################################
class Internal(Cog):
    
    def __init__(self, bot: PartyBusBot):

        self.bot: PartyBusBot = bot
        
################################################################################
    @Cog.listener("on_ready")
    async def load_internals(self) -> None:

        print("Loading internals...")
        await self.bot.load_all()
        
################################################################################
def setup(bot: PartyBusBot) -> None:

    bot.add_cog(Internal(bot))
    
################################################################################
