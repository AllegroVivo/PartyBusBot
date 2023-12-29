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
        name="status",
        description="View and edit your training registration profile & status."
    )
    async def trainee_status(self,  ctx: ApplicationContext) -> None:
        
        await self.bot.user_status(ctx.interaction)

################################################################################
    @training.command(
        name="update",
        description="Update an individual's training progress."
    )
    async def update_training(
        self, 
        ctx: ApplicationContext,
        trainee: Option(
            SlashCommandOptionType.user,
            name="user",
            description="The user whose training(s) to update.",
            required=True
        )
    ) -> None:
        
        await self.bot.update_training(ctx.interaction, trainee)
        
################################################################################
    @training.command(
        name="test",
        description="Test command."
    )
    async def test(self, ctx: ApplicationContext) -> None:
        
        trainee = self.bot.training_manager.get_trainee_by_user_id(ctx.author.id)
        await trainee.add_schedule(ctx.interaction)
        
################################################################################
def setup(bot: "PartyBusBot") -> None:

    bot.add_cog(Training(bot))
    
################################################################################
