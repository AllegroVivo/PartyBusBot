from __future__ import annotations

from discord import EmbedField
from typing import TYPE_CHECKING, Optional, Type, TypeVar, Tuple, Any

from discord import Interaction, Embed

from Assets import BotEmojis
from Utils import Utilities as U, Timezone, TraineeNotFoundError

if TYPE_CHECKING:
    from Classes import TUser
################################################################################

__all__ = ("UserConfiguration",)

UC = TypeVar("UC", bound="UserConfiguration")

################################################################################
class UserConfiguration:

    __slots__ = (
        "_parent",
        "_image",
        "_job_pings",
    )
    
################################################################################
    def __init__(
        self, 
        parent: TUser,
        image: Optional[str] = None, 
        job_pings: bool = True
    ):
        
        self._parent: TUser = parent
        
        self._image: Optional[str] = image
        self._job_pings: bool = job_pings
        
################################################################################
    @classmethod
    def load(cls: Type[UC], parent: TUser, data: Tuple[Any, ...]) -> UC:
        
        return cls(parent,  data[1],  data[2])

################################################################################
    @property
    def job_pings(self) -> bool:
        
        return self._job_pings
    
################################################################################    
    @job_pings.setter
    def job_pings(self, value: bool) -> None:
        
        self._job_pings = value
        self.update()
        
################################################################################
    @property
    def image(self) -> Optional[str]:
        
        return self._image
    
################################################################################
    async def menu(self, interaction: Interaction) -> None:

        embed = self.status()
        # view = TUserConfigView(interaction.user, self)
        
        await interaction.respond(embed=embed)
    
################################################################################
    def status(self) -> Embed:
        
        fields = [
            EmbedField(
                name="__Job Pings__",
                value=f"{BotEmojis.Check if self._job_pings else BotEmojis.Cross}",
                inline=True
            )
        ]
        
        return U.make_embed(
            title=f"User Configuration for __{self._parent.name}__",
            description=U.draw_line(extra=35),
            fields=fields
        )
    
################################################################################
    def toggle_job_pings(self) -> None:
        
        self._job_pings = not self._job_pings
        self._parent.update()
        
################################################################################
    def update(self) -> None:
        
        self._parent.bot.update_tuser_config(self)
    
################################################################################
