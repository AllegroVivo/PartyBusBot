from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Tuple, Type, TypeVar, Any

from discord import Interaction, User, Embed, EmbedField, SelectOption

from Classes.Training.Qualification import Qualification
from UI.Views import AddQualificationView, ModifyQualificationView, RemoveQualificationView
from Utils import Utilities as U, TrainingLevel

if TYPE_CHECKING:
    from Classes import PartyBusBot, TUser, Position
################################################################################

__all__ = ("Trainer", )

T = TypeVar("T", bound="Trainer")

################################################################################
class Trainer:
    
    __slots__ = (
        "_parent",
        "_qualifications",
        # "_trainees",
    )
    
################################################################################
    def __init__(
        self,
        parent: TUser,
        qlist: List[Qualification] = None,
    ) -> None:
        
        self._parent: TUser = parent
        
        self._qualifications: List[Qualification] = qlist or []
    
################################################################################
    @classmethod
    def load(
        cls: Type[T],
        parent: TUser,
        qualifications_data: List[Tuple[Any, ...]],
    ) -> T:
        
        qlist = [
            Qualification.load(parent.bot.training_manager, q) 
            for q in qualifications_data
        ]
        
        return cls(parent, qlist)
    
################################################################################
    @property
    def bot(self) -> PartyBusBot:
        
        return self._parent.bot

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
    def qualifications(self) -> List[Qualification]:

        return self._qualifications
        
    @property
    def select_option(self) -> SelectOption:
        
        return SelectOption(
            label=self.name,
            value=str(self.user.id)
        )
    
################################################################################
    def qualifications_field(self) -> EmbedField:
        
        value = ""
        positions = self.bot.position_manager.positions
        
        for position in positions:
            value += (position.format_qualification(self._qualifications) + "\n")
            
        if not value:
            value = "None"
        
        return EmbedField(
            name="__Qualifications__",
            value=value,
            inline=True
        )
    
################################################################################
    def notes_field(self) -> EmbedField:

        return EmbedField(
            name="__Internal Notes__",
            value=self._notes or "`None`",
            inline=True
        )
    
################################################################################
    def status(self) -> Embed:
        
        fields = [
            self.qualifications_field(),
            self.notes_field()
        ]
        
        return U.make_embed(
            title=f"Trainer Status for __{self.name}__",
            description=U.draw_line(extra=25),
            fields=fields
        )
    
################################################################################        
    def get_qualification(self, position: Position) -> Optional[Qualification]:
        
        for q in self._qualifications:
            if q.position == position:
                return q
    
################################################################################
    def update(self) -> None:
        
        self.bot.database.update.trainer(self)
        
################################################################################
    async def add_qualification(self, interaction: Interaction) -> None:
        
        embed = U.make_embed(
            title="Add Qualification",
            description=(
                "Select the position you would like to add a qualification\n"
                "for. Subsequently, a second selector will appear to\n"
                "allow you to select the new qualification level.\n"
                f"{U.draw_line(extra=25)}"
            )
        )
        
        base_options = self.bot.position_manager.select_options()
        options = [
            o for o in base_options 
            if o.value not in [q.position.id for q in self._qualifications]
        ]        
        
        view = AddQualificationView(interaction.user, options)
        
        await interaction.respond(embed=embed, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        position = self.bot.get_position(view.value[0])
        level = TrainingLevel(int(view.value[1]))
        
        qualification = Qualification.new(self.bot, self.user, position, level)
        self._qualifications.append(qualification)
        
        # No need to update here.
        
################################################################################
    async def modify_qualification(self, interaction: Interaction) -> None:
        
        embed = U.make_embed(
            title="Modify Qualification",
            description=(
                "Select the position you would like to modify a qualification\n"
                "for. Subsequently, a second selector will appear to\n"
                "allow you to select the individual qualification to modify.\n"
                f"{U.draw_line(extra=25)}"
            )
        )
        view = ModifyQualificationView(interaction.user, self.qualification_options())
        
        await interaction.respond(embed=embed, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        pos = self.bot.get_position(view.value[0])
        qualification = self.get_qualification(pos)
        qualification.update(TrainingLevel(int(view.value[1])))

################################################################################
    async def remove_qualification(self, interaction: Interaction) -> None:
        
        embed = U.make_embed(
            title="Remove Qualification",
            description=(
                "Select the position you would like to remove a qualification\n"
                "for. Subsequently, a second selector will appear to\n"
                "allow you to select the individual qualification to remove.\n"
                f"{U.draw_line(extra=25)}"
            )
        )
        view = RemoveQualificationView(interaction.user, self.qualification_options())
        
        await interaction.respond(embed=embed, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        qualification = self.get_qualification(self.bot.get_position(view.value))
        
        qualification.delete()
        self._qualifications.remove(qualification)
        
        # No need to update here.
    
################################################################################
    def qualification_options(self) -> List[SelectOption]:
        
        options = []
        
        for q in self._qualifications:
            options.append(
                SelectOption(
                    label=q.position.name,
                    value=q.position.id
                )
            )
            
        return options

################################################################################
    def is_qualified(self, position_id: str) -> bool:
        
        for q in self._qualifications:
            if q.position.id == position_id:
                return True
            
        return False

################################################################################
