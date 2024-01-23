from discord import (
    ApplicationContext,
    Cog,
    SlashCommandGroup,
    Option, 
    SlashCommandOptionType
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Classes.Bot import PartyBusBot
################################################################################
class Jobs(Cog):
    
    def __init__(self, bot: "PartyBusBot"):
        
        self.bot: "PartyBusBot" = bot
        
################################################################################
    
    trainers = SlashCommandGroup(
        name="jobs",
        description="Commands for job search-related tasks and queries"
    )
    
################################################################################
    @trainers.command(
        name="post",
        description="Post a new permanent or temporary job opening."
    )
    async def job_post(self, ctx: ApplicationContext) -> None:
        
        await self.bot.job_post(ctx.interaction)
        
################################################################################
def setup(bot: "PartyBusBot") -> None:

    bot.add_cog(Jobs(bot))
    
################################################################################
