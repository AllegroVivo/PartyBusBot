from discord import (
    ApplicationContext, 
    Cog,
    SlashCommandGroup,
    Option,
    SlashCommandOptionType,
    Role
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Classes.Bot import PartyBusBot
################################################################################
class Positions(Cog):

    def __init__(self, bot: "PartyBusBot"):

        self.bot: "PartyBusBot" = bot

################################################################################

    positions = SlashCommandGroup(
        name="positions",
        description="Commands for trainer management."
    )

################################################################################
    @positions.command(
        name="add",
        description="Add a new position to the database."
    )
    async def add_position(
        self, 
        ctx: ApplicationContext,
        position_name: Option(
            type=SlashCommandOptionType.string,
            name="name",
            description="The name of the position to add.",
            required=True
        )
    ) -> None:

        await self.bot.add_position(ctx.interaction, position_name)

################################################################################
    @positions.command(
        name="status",
        description="View and edit the status of a given job position."
    )
    async def position_status(
        self, 
        ctx: ApplicationContext,
        position: Option(
            type=SlashCommandOptionType.string,
            name="position",
            description="The position to view.",
            required=False
        )
    ) -> None:

        await self.bot.position_status(ctx.interaction, position)
        
################################################################################
    @positions.command(
        name="global_reqs",
        description="View and edit the global requirements for all positions."
    )
    async def global_requirements(self, ctx: ApplicationContext) -> None:

        await self.bot.position_manager.global_requirements_menu(ctx.interaction)
        
################################################################################
def setup(bot: "PartyBusBot") -> None:

    bot.add_cog(Positions(bot))

################################################################################
