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
class Trainers(Cog):
    
    def __init__(self, bot: "PartyBusBot"):
        
        self.bot: "PartyBusBot" = bot
        
################################################################################
    
    trainers = SlashCommandGroup(
        name="trainers",
        description="Commands for trainer management."
    )
    
################################################################################
    @trainers.command(
        name="update_trainee",
        description="Update a trainee's training status."
    )
    async def update_training(
        self, 
        ctx: ApplicationContext,
        user: Option(
            SlashCommandOptionType.user,
            name="user",
            description="The user whose trainer record to view.",
            required=True
        )
    ) -> None:
        
        await self.bot.update_training(ctx.interaction, user)

################################################################################
    @trainers.command(
        name="query_trainee",
        description="Check details about a prospective or active trainee."
    )
    async def query_trainee(
        self, 
        ctx: ApplicationContext,
        user: Option(
            SlashCommandOptionType.user,
            name="user",
            description="The user whose trainer record to view.",
            required=True
        )
    ) -> None:
        
        await self.bot.query_trainee(ctx.interaction, user)
        
################################################################################
def setup(bot: "PartyBusBot") -> None:

    bot.add_cog(Trainers(bot))
    
################################################################################
