from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Type, TypeVar, Any, Tuple

from discord import Interaction, User, SelectOption, Embed, EmbedField

from Assets import BotEmojis
from Classes.Training.Availability import Availability
from Classes.Training.Training import Training
from UI.Views import AddTrainingView, RemoveTrainingView, UpdateTrainingView
from Utils import Utilities as U, RequirementLevel

if TYPE_CHECKING:
    from Classes import PartyBusBot, TUser
################################################################################

__all__ = ("Trainee", )

T = TypeVar("T", bound="Trainee")

################################################################################
class Trainee:
    
    __slots__ = (
        "_parent",
        "_availability",
    )
    
################################################################################
    def __init__(self, parent: TUser, availabilities: Optional[List[Availability]] = None) -> None:
        
        self._parent: TUser = parent
        self._availability: List[Availability] = availabilities or []
        
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
    def load(cls: Type[T], parent: TUser) -> T:
        
        self: T = cls.__new__(cls)
        
        self._parent = parent
        self._availability = []
        
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
    def name(self) -> str:
        
        return self._parent.name
    
################################################################################    
    @property
    def user(self) -> User:
        
        return self._parent.user
    
################################################################################
    @property
    def trainings(self) -> List[Training]:
        
        return [t for t in self.bot.training_manager.all_trainings if t.trainee == self]

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
            if o.value not in [t.position.id for t in self.trainings]
        ]
        
        view = AddTrainingView(interaction.user, options)
        
        await interaction.respond(embed=embed, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        for pos_id in view.value:
            self.bot.training_manager.add_training(Training.new(self, pos_id))
    
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
    
        self.bot.training_manager.remove_training(view.value)
            
################################################################################
    def training_select_options(self) -> List[SelectOption]:
        
        return [
            SelectOption(
                label=t.position.name,
                value=str(t.id),
            )
            for t in self.trainings
        ]
    
################################################################################
    def training_status(self) -> Embed:
        
        return U.make_embed(
            title="Trainings",
            description=(
                "Here are this trainee's current in-progress trainings.\n\n"
                
                "Please choose a job to update from the selector below.\n"
                "Another selector will appear to choose which\n"
                "requirement has been completed.\n"
                f"{U.draw_line(extra=33)}"
            ),
            fields=[t.embed_field for t in self.trainings]
        )
    
################################################################################
    async def update_training(self, interaction: Interaction) -> None:

        status = self.training_status()
        view = UpdateTrainingView(interaction.user, self)

        await interaction.respond(embed=status, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        training = self.get_training(view.value[0])
        training.add_requirement_override(view.value[1], RequirementLevel(view.value[2]))
        
        await self.update_training(interaction)
        
################################################################################
    def get_training(self, training_id: str) -> Optional[Training]:
        
        for t in self.trainings:
            if t.id == training_id:
                return t
            
################################################################################
    async def notify_of_selection(self, training: Training) -> None:
        
        embed = U.make_embed(
            title="You've Been Matched!",
            description=(
                f"Congratulations! You have been paired with a trainer for "
                f"`{training.position.name}`.\n\n"
                
                f"Your trainer will be... {BotEmojis.Drum} ***drumroll...*** {BotEmojis.Drum}\n"
                f"`{training.trainer.name}`! ({training.trainer.user.mention})\n\n"
                
                "Your trainer will contact you shortly to schedule a training "
                "session based on the availability that you provided in your "
                "trainee profile.\n"

                f"{U.draw_line(extra=35)}"
            )
        )
        
        await self.user.send(embed=embed)
    
################################################################################
