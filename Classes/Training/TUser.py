from __future__ import annotations

from discord import Interaction, User, Embed, EmbedField, NotFound
from typing import TYPE_CHECKING, List, Optional, Tuple, Type, TypeVar, Any, Dict

from Classes.Training import Trainee, Trainer
from Classes.Training.UserConfig import UserConfiguration
from Classes.Training.Availability import Availability
from Classes.Training.Training import Training
from UI.Common import NameModal, NotesModal
from UI.Positions import (
    MultiPositionSelectView,
    SinglePositionSelectView,
    RequirementStatusSelectView
)
from UI.Training import ScheduleSelectView, TraineeStatusView
from Utils import Utilities as U, RequirementLevel

if TYPE_CHECKING:
    from Classes import PartyBusBot, TrainingManager, Qualification
################################################################################

__all__ = ("TUser",)

TU = TypeVar("TU", bound="TUser")

################################################################################
class TUser:
    
    __slots__ = (
        "_manager",
        "_user",
        "_name",
        "_notes",
        "_availability",
        "_config",
        "_trainer",
        "_trainee",
    )
    
################################################################################
    def __init__(
        self,
        mgr: TrainingManager,
        user: User,
        trainee: Trainee,
        trainer: Trainer,
        name: Optional[str] = None,
        notes: Optional[str] = None,
        availabilities: Optional[List[Availability]] = None,
        configuration: Optional[UserConfiguration] = None
    ) -> None:
        
        self._manager: TrainingManager = mgr
        
        self._user: User = user
        self._name: str = name or user.name
        self._notes: Optional[str] = notes
        
        self._config: UserConfiguration = configuration or UserConfiguration(self)
        self._availability: List[Availability] = availabilities or []
        
        self._trainee: Trainee = trainee
        self._trainer: Trainer = trainer
        
################################################################################
    def __eq__(self, other: TUser) -> bool:
        
        return self.user_id == other.user_id
        
################################################################################
    @classmethod
    def new(cls: Type[TU], bot: PartyBusBot, user: User) -> TU:
        
        bot.database.insert.tuser(user.id)
        
        self: TU = cls.__new__(cls)
        
        self._user = user
        self._name = user.name
        self._notes = None
        
        self._config = UserConfiguration(self)
        self._availability = []
        
        self._trainee = Trainee(self)
        self._trainer = Trainer(self)
        
        return self
    
################################################################################
    @classmethod
    async def load(cls: Type[TU], mgr: TrainingManager, data: Dict[str, Any]) -> Optional[TU]:
        
        tuser = data["tuser"]
        config = data["config"]
        availability = data["availability"]
        qdata = data["qualifications"]
        trainings = data["trainings"]
        
        try:
            user = await mgr.bot.fetch_user(tuser[0])
        except NotFound:
            return None
        
        self: TU = cls.__new__(cls)
        
        self._manager = mgr
        self._user = user
        
        self._name = tuser[1]
        self._notes = tuser[2]
        
        self._config = UserConfiguration.load(self, config)
        self._availability = [Availability.load(a) for a in availability]
        
        self._trainer = Trainer.load(self, qdata)
        self._trainee = Trainee.load(self, trainings)
        
        return self
    
################################################################################
    @property
    def bot(self) -> PartyBusBot:
        
        return self._manager.bot
        
################################################################################
    @property
    def user(self) -> User:
        
        return self._user
    
################################################################################
    @property
    def user_id(self) -> int:
        
        return self._user.id
    
################################################################################
    @property
    def trainer(self) -> Trainer:
        
        return self._trainer
    
################################################################################
    @property
    def trainee(self) -> Trainee:
        
        return self._trainee
    
################################################################################
    @property
    def name(self) -> str:
        
        return self._name
    
################################################################################
    @name.setter
    def name(self, value: str) -> None:
        
        self._name = value
        self.update()
        
################################################################################
    @property
    def trainings(self) -> List[Training]:
        
        return self._trainings
    
################################################################################    
    @property
    def notes(self) -> Optional[str]:
        
        return self._notes
    
################################################################################
    @notes.setter
    def notes(self, value: Optional[str]) -> None:
        
        self._notes = value
        self.update()
    
################################################################################    
    @property
    def qualifications(self) -> List[Qualification]:
        
        return self.trainer.qualifications
    
################################################################################
    def status(self) -> Embed:
        
        return U.make_embed(
            title=f"User Status for: {self.name}",
            description=(
                f"{U.draw_line(extra=25)}"
            ),
            fields=[
                self.qualifications_field(),
                self.training_requested_field(),
                self.notes_field(),
            ]
        )
        
################################################################################
    def training_requested_field(self) -> EmbedField:        
        
        return EmbedField(
            name="__Trainings Requested__",
            value=(
                (
                    "* " + "\n* ".join(
                        [
                            f"{t.position.name}"
                            for t in self.trainee.trainings
                        ]
                    ) if self.trainee.trainings else "`None`"
                )
            ),
            inline=True
        )

################################################################################
    def qualifications_field(self) -> EmbedField:

        return EmbedField(
            name="__Trainer Qualifications__",
            value=(
                ( 
                    "* " + "\n* ".join(
                        [
                            f"{q.position.name}\n-- *({q.level.proper_name})*\n" 
                            for q in self.trainer.qualifications
                        ]
                    ) if self.trainer.qualifications else "`None`"
                )
            ),
            inline=True
        )

################################################################################
    def notes_field(self) -> EmbedField:

        return EmbedField(
            name="__Internal Notes__",
            value=self.notes if self.notes else "`None`",
            inline=False
        )
        
################################################################################
    def update(self) -> None:
        
        self._manager.bot.database.update.tuser(self)
        
################################################################################    
    async def set_name(self, interaction: Interaction) -> None:
        
        modal = NameModal(self.name)
        
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        if not modal.complete:
            return
        
        self.name = modal.value
        
################################################################################
    async def edit_notes(self, interaction: Interaction) -> None:

        modal = NotesModal(self._notes)

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.notes = modal.value   

################################################################################
    async def add_qualification(self, interaction: Interaction) -> None:
        
        await self.trainer.add_qualification(interaction)
    
################################################################################
    async def modify_qualification(self, interaction: Interaction) -> None:
        
        await self.trainer.modify_qualification(interaction)
        
################################################################################
    async def remove_qualification(self, interaction: Interaction) -> None:
        
        await self.trainer.remove_qualification(interaction)
        
################################################################################
    async def add_training(self, interaction: Interaction) -> None:
        
        await self.trainee.add_training(interaction)
        
################################################################################
    async def remove_training(self, interaction: Interaction) -> None:
        
        await self.trainee.remove_training(interaction)
        
################################################################################
