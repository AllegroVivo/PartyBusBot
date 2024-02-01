from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Any, Tuple

from discord import Interaction, Embed

from Utils import Utilities as U, CompensationType

if TYPE_CHECKING:
    from Classes import Job
################################################################################

__all__ = ("Compensation",)

################################################################################
class Compensation:

    __slots__ = (
        "_parent",
        "_rate",
        "_type",
    )
    
################################################################################
    def __init__(
        self, 
        parent: Job,
        rate: Optional[int] = None,
        _type: Optional[CompensationType] = None
    ) -> None:
        
        self._parent: Job = parent
        
        self._rate: int = rate
        self._type: CompensationType = _type
        
################################################################################
    @classmethod
    def load(cls, parent: Job, data: Tuple[Any, ...]) -> Compensation:
        
        return cls(parent, data[0], CompensationType(data[1]) if data[1] else None)
    
################################################################################
    @property
    def pay_rate(self) -> int:
        
        return self._rate
    
    @pay_rate.setter
    def pay_rate(self, value: int) -> None:
        
        self._rate = value
        self.update()
        
################################################################################
    @property
    def pay_type(self) -> CompensationType:
        
        return self._type
    
    @pay_type.setter
    def pay_type(self, value: CompensationType) -> None:
        
        self._type = value
        self.update()
        
################################################################################
    def update(self) -> None:
        
        self._parent.update()
        
################################################################################
    def status(self) -> Embed:

        return U.make_embed(
            title="Job Compensation",
            description=(
                "Finally, we just need to know how much you'll be paying:\n\n"
                
                "**Compensation:** "
                f"{U.draw_line(extra=25)}\n\n"

                "Please complete the above details to finish your post."
            ),
        )
    
################################################################################
    async def set_all(self, interaction: Interaction) -> None:

        embed = self.status()
        view = CollectJobCompensationView(interaction.user, self._parent)

        await interaction.respond(embed=embed, view=view)
        await view.wait()

################################################################################
