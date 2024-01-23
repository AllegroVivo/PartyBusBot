from discord import (
    ApplicationContext,
    Cog,
    SlashCommandGroup,
    Option, 
    SlashCommandOptionType
)
from typing import TYPE_CHECKING

from UI.Training import ScheduleSelectView

if TYPE_CHECKING:
    from Classes.Bot import PartyBusBot
################################################################################
class Training(Cog):
    
    def __init__(self, bot: "PartyBusBot"):
        
        self.bot: "PartyBusBot" = bot
        
################################################################################
    
    training = SlashCommandGroup(
        name="training",
        description="Commands for training-related tasks and queries."
    )
        
################################################################################
    @training.command(
        name="profile",
        description="View and edit your training registration profile & status."
    )
    async def training_profile(self, ctx: ApplicationContext) -> None:
        
        await self.bot.tuser_status(ctx.interaction)
      
################################################################################  
    @training.command(
        name="config",
        description="View and edit user configuration."
    )
    async def training_config(self, ctx: ApplicationContext) -> None:
        
        await self.bot.tuser_config(ctx.interaction)
        
################################################################################
def setup(bot: "PartyBusBot") -> None:

    bot.add_cog(Training(bot))
    
################################################################################
