from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Tuple

from discord import Interaction, Embed
from UI import SelectPositionView, CollectJobDetailsView
from Utils import Utilities as U

if TYPE_CHECKING:
    from Classes import Position, Job
################################################################################

__all__ = ("JobDetails",)

################################################################################
class JobDetails:

    __slots__ = (
        "_parent",
        "_position",
        "_venue",
        "_description",
    )

################################################################################
    def __init__(
        self, 
        parent: Job, 
        position: Optional[Position] = None, 
        venue: Optional[str] = None, 
        description: Optional[str] = None
    ) -> None:

        self._parent: Job = parent

        self._position: Position = position
        self._venue: Optional[str] = venue
        self._description: Optional[str] = description

################################################################################
    @property
    def position(self) -> Position:
        
        return self._position
    
    @position.setter
    def position(self, value: Position) -> None:
        
        self._position = value
        self.update()
        
################################################################################
    @property
    def venue(self) -> str:
        
        return self._venue
    
    @venue.setter
    def venue(self, value: str) -> None:
        
        self._venue = value
        self.update()
        
################################################################################
    @property
    def description(self) -> Optional[str]:
        
        return self._description
    
    @description.setter
    def description(self, value: Optional[str]) -> None:
        
        self._description = value
        self.update()
        
################################################################################
    def update(self) -> None:
        
        self._parent.update()
        
################################################################################
    async def collect_all_details(self, interaction: Interaction) -> None:
        
        embed = self.status()
        view = CollectJobDetailsView(interaction.user, self._parent)
        
        await interaction.respond(embed=embed, view=view)
        await view.wait()
    
################################################################################
    def status(self) -> Embed:
        
        position_str = f"`{self.position.name}`" if self.position is not None else "`Not Set`"
        venue_str = f"`{self.venue}`" if self.venue is not None else "`Not Set`"
        description_str = f"`{self.description}`" if self.description is not None else "`Not Set`\n*(Optional)*"
        
        return U.make_embed(
            title="Job Details",
            description=(
                f"**Position:** {position_str}\n"
                f"**Venue Name:** {venue_str}\n"
                f"**Description:** {description_str}\n"
                f"{U.draw_line(extra=25)}\n\n"
                
                "Please complete the above details before continuing."
            ),
        )
    
################################################################################
    async def set_position(self, interaction: Interaction) -> None:
        
        embed = U.make_embed(
            title="Set Job Position",
            description="Please select a position from the drop-down below.",
        )
        
        options = self._parent.bot.position_manager.select_options()
        view = SelectPositionView(interaction.user, options)
        
        await interaction.respond(embed=embed, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return

        self.position = self._parent.bot.get_position(view.value)
        
################################################################################
        