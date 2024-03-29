from discord import (
    ApplicationContext,
    Cog,
    SlashCommandGroup,
    Option, 
    SlashCommandOptionType
)
from typing import TYPE_CHECKING

from Utils import Hours

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
        name="add_trainer",
        description="Add a user as a trainer."
    )
    async def add_trainer(
        self,
        ctx: ApplicationContext,
        user: Option(
            SlashCommandOptionType.user,
            name="user",
            description="The user to add as a trainer.",
            required=True
        )
    ) -> None:

        await self.bot.tuser_admin_status(ctx.interaction, user)
        
################################################################################
    @admin.command(
        name="user_status",
        description="View and edit the trainer/trainee profile & status of a user."
    )
    async def user_status(
        self, 
        ctx: ApplicationContext,
        user: Option(
            SlashCommandOptionType.user,
            name="user",
            description="The user whose trainer record to view.",
            required=True
        )
    ) -> None:
        
        await self.bot.tuser_admin_status(ctx.interaction, user)

################################################################################
    @admin.command(
        name="post_signup",
        description="Post the trainer signup message."
    )
    async def post_signup_message(
        self, 
        ctx: ApplicationContext,
        channel: Option(
            SlashCommandOptionType.channel,
            name="channel",
            description="The channel to set as the trainer signup message channel.",
            required=True
        )
    ) -> None:
        
        await self.bot.post_signup_message(ctx.interaction, channel)
    
################################################################################
    @admin.command(
        name="trainer_management",
        description="Manage trainer assignments."
    )
    async def trainer_management(self,  ctx: ApplicationContext) -> None:
        
        await self.bot.manage_trainers(ctx.interaction)
        
################################################################################        
    @admin.command(name="test")
    async def test(self, ctx: ApplicationContext) -> None:
        
        await self.bot.job_manager.create_post(ctx.interaction)
        
################################################################################
def setup(bot: "PartyBusBot") -> None:

    bot.add_cog(Admin(bot))
    
################################################################################
