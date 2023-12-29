from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Type, TypeVar, Any, Tuple

from discord import Interaction, User, SelectOption

from Classes.Training.Availability import Availability
from Classes.Training.Training import Training
from UI.Views import AddTrainingView, RemoveTrainingView
from Utils import Utilities as U

if TYPE_CHECKING:
    from Classes import PartyBusBot, TUser
################################################################################

__all__ = ("Trainee", )

T = TypeVar("T", bound="Trainee")

################################################################################
class Trainee:
    
    __slots__ = (
        "_parent",
        "_trainings",
        "_availability",
    )
    
################################################################################
    def __init__(
        self,
        parent: TUser,
        availabilities: Optional[List[Availability]] = None,
        trainings: Optional[List[Training]] = None,
    ) -> None:
        
        self._parent: TUser = parent
        
        self._availability: List[Availability] = availabilities or []
        self._trainings: List[Training] = trainings or []
        
################################################################################
    def __eq__(self, other: Trainee) -> bool:
        
        return self._parent == other.parent
        
################################################################################
    @classmethod
    def new(cls: Type[T], bot: PartyBusBot, user: User) -> T:
        
        new_id = bot.database.insert.trainee(user.id)
        return cls(bot.training_manager, new_id, user)
    
################################################################################
    @classmethod
    def load(
        cls: Type[T],
        parent: TUser,
        training_data: List[Tuple[Any, ...]]
    ) -> T:
        
        self: T = cls.__new__(cls)
        
        self._parent = parent
        
        self._availability = []
        self._trainings = [Training.load(parent._manager, t) for t in training_data]
        
        return self
    
################################################################################
    @property
    def bot(self) -> PartyBusBot:
        
        return self._parent.bot
        
################################################################################
    @property
    def user_id(self) -> int:
        
        return self._parent.user_id
    
################################################################################
    @property
    def parent(self) -> TUser:
        
        return self._parent
        
################################################################################
    @property
    def trainings(self) -> List[Training]:
        
        return self._trainings

################################################################################
    def update(self) -> None:
        
        self.bot.database.update.trainee(self)
        
################################################################################
    async def add_training(self, interaction: Interaction) -> None:
        
        embed = U.make_embed(
            title="Add Training",
            description=(
                "Please select a training to add.\n"
                f"{U.draw_line(extra=25)}"
            ),
        )

        base_options = self.bot.position_manager.select_options()
        options = [
            o for o in base_options
            if o.value not in [t.position.id for t in self._trainings]
        ]
        
        view = AddTrainingView(interaction.user, options)
        
        await interaction.respond(embed=embed, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        for pos_id in view.value:
            self._trainings.append(Training.new(self, pos_id))
    
################################################################################
    async def remove_training(self, interaction: Interaction) -> None:
        
        embed = U.make_embed(
            title="Remove Training",
            description=(
                "Please select a training to remove.\n"
                f"{U.draw_line(extra=25)}"
            ),
        )

        options = self.training_select_options()
        
        view = RemoveTrainingView(interaction.user, options)
        
        await interaction.respond(embed=embed, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
    
        for t in self.trainings:
            if t.id == view.value:
                self._trainings.remove(t)
                t.delete()
            
################################################################################
    def training_select_options(self) -> List[SelectOption]:
        
        return [
            SelectOption(
                label=t.position.name,
                value=str(t.id),
            )
            for t in self._trainings
        ]
    
################################################################################
