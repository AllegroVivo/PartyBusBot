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
class Admin(Cog):
    
    def __init__(self, bot: "PartyBusBot"):
        
        self.bot: "PartyBusBot" = bot
        
################################################################################
    
    admin = SlashCommandGroup(
        name="admin",
        description="Administrator commands for user/system configuration & management."
    )
    
################################################################################
    @admin.command(
        name="user_status",
        description="View and edit the trainer/trainee profile & status of a user."
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
        
        await self.bot.tuser_status(ctx.interaction, user)

################################################################################
def setup(bot: "PartyBusBot") -> None:

    bot.add_cog(Admin(bot))
    
################################################################################
