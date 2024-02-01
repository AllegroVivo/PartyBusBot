from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Type, TypeVar, Any, Dict

from discord import Interaction, User, Embed, EmbedField, NotFound

from Classes.Training import Trainee, Trainer
from Classes.Training.Availability import Availability
from Classes.Training.Training import Training
from Classes.Training.UserConfig import UserConfiguration
from UI.Common import NameModal, NotesModal
from UI import TimeSelectView, WeekdaySelectView
from Utils import Utilities as U, ViewType, Weekday

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
        
        self._manager = bot.training_manager
        
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
        self._availability = [Availability.load(self, a) for a in availability]
        
        self._trainer = Trainer.load(self, qdata)
        self._trainee = Trainee.load(self)
        
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
    def image(self) -> Optional[str]:
    
        return self._config.image
    
################################################################################
    @property
    def config(self) -> UserConfiguration:
        
        return self._config
    
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
    @property
    def availability(self) -> List[Availability]:
        
        self._availability.sort(key=lambda a: a.day.value)
        return self._availability
    
################################################################################
    @property
    def trainings(self) -> List[Training]:
        
        return self._manager.get_trainings_by_user(self.user_id)
    
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
                self.availability_field(),
                self.notes_field(),
            ]
        )
        
################################################################################
    def trainee_status(self) -> Embed:
        
        return U.make_embed(
            title=f"User Status for: {self.name}",
            description=(
                f"{U.draw_line(extra=25)}"
            ),
            fields=[
                self.training_requested_field(),
                self.availability_field(),
            ],
            footer_text=(
                "If the availability times above are different than what\n"
                "you specified, try adjusting your personal timezone\n"
                "using the `/training config` command."
            )
        )
    
################################################################################
    def training_requested_field(self) -> EmbedField:        
        
        trainings = self._manager.get_trainings_by_user(self.user_id)
        training_str = "`None`" if not trainings else ""
        
        for t in trainings:
            if training_str == "":
                training_str = f"* {t.position.name}\n-- Trainer: "
                
            training_str += f"`{t.trainer.name}`\n" if t.trainer else "None... (Yet!)"
            
        return EmbedField(
            name="__Trainings Requested__",
            value=training_str,
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
    def availability_field(self) -> EmbedField:
        
        return EmbedField(
            name="__Availability__",
            value=Availability.availability_status(self.availability),
            inline=False
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
    async def set_notes(self, interaction: Interaction) -> None:

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
    async def set_availability(self, interaction: Interaction) -> None:
        
        status = U.make_embed(
            title="Set Availability",
            description=(
                "Please select the appropriate day from the initial\n"
                "selector, followed by your available time frame.\n\n"
                
                "Please note, you can set your timezone\n"
                "by using the `/training config` command.\n"
                f"{U.draw_line(extra=25)}"
            )
        )
        view = WeekdaySelectView(interaction.user)
        
        await interaction.respond(embed=status, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        weekday = view.value
        
        prompt = U.make_embed(
            title="Set Availability Start",
            description=(
                f"Please select the beginning of your availability for `{weekday.proper_name}`..."
            )
        )
        view = TimeSelectView(interaction.user, ViewType.StartTimeSelect)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        start_time = view.value if view.value != -1 else None
        end_time = None
        
        if start_time is not None:
            prompt = U.make_embed(
                title="Set Availability End",
                description=(
                    f"Please select the end of your availability for `{weekday.proper_name}`..."
                )
            )
            view = TimeSelectView(interaction.user, ViewType.EndTimeSelect)
    
            await interaction.respond(embed=prompt, view=view)
            await view.wait()
    
            if not view.complete or view.value is False:
                return
            
            end_time = view.value
            
        if self.get_availability_for(weekday):
            self.remove_availability(weekday)
        
        availability = Availability.new(self, weekday, start_time, end_time)
        self._availability.append(availability)
        
################################################################################
    def get_availability_for(self, day: Weekday) -> Optional[Availability]:
        
        for a in self.availability:
            if a.day == day:
                return a
    
################################################################################
    def remove_availability(self, day: Weekday) -> None:
        
        for a in self.availability:
            if a.day == day:
                self._availability.remove(a)
                a.delete()
                
################################################################################
