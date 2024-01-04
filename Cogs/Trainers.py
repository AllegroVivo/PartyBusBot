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
    async def trainer_status(
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
def setup(bot: "PartyBusBot") -> None:

    bot.add_cog(Trainers(bot))
    
################################################################################
