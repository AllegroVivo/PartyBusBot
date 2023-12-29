from __future__ import annotations

from discord import Role, SelectOption, Interaction, Embed, EmbedField, HTTPException
from typing import TYPE_CHECKING, List, Optional, Type, TypeVar, Tuple

from Assets import BotEmojis
from Classes.Positions.Requirement import Requirement
from UI.Positions import (
    PositionStatusView, 
    PositionNameModal,
    PositionRequirementModal,
    PositionRoleModal,
    RemoveRequirementView
)
from Utils import Utilities as U, InvalidRoleIDError, InvalidNumberError

if TYPE_CHECKING:
    from Classes import PartyBusBot, PositionManager, Qualification
################################################################################

__all__ = ("Position", )

GUILD_ID = 303742308874977280
P = TypeVar("P", bound="Position")

################################################################################
class Position:

    __slots__ = (
        "_manager",
        "_id",
        "_name",
        "_trainer_role",
        "_trainee_role",
        "_requirements"
    )
    
################################################################################
    def __init__(
        self,
        mgr: PositionManager,
        _id: str, 
        name: str,
        trainer_role: Optional[Role] = None,
        trainee_role: Optional[Role] = None,
        reqs: Optional[List[str]] = None
    ) -> None:
        
        self._manager: PositionManager = mgr
        self._id: str = _id
        self._name: str = name
        
        self._trainer_role: Optional[Role] = trainer_role
        self._trainee_role: Optional[Role] = trainee_role
        
        self._requirements: List[Requirement] = reqs or []
        
################################################################################
    def __eq__(self, other: Position) -> bool:
        
        return self.id == other.id
    
################################################################################
    @classmethod
    def new(cls: Type[P], mgr: PositionManager, name: str) -> P:
        
        new_id = mgr.bot.database.insert.position(name)
        return cls(mgr, new_id, name)
    
################################################################################
    @classmethod
    async def load(
        cls: Type[P], 
        mgr: PositionManager, 
        data: Tuple[str, str, int, int],
        requirements: List[Tuple[str, str, str]]
    ) -> P:
        
        guild = mgr.bot.get_guild(GUILD_ID)
        
        trainer_role = trainee_role = None
        if data[2] is not None:
            try:
                trainer_role = await guild._fetch_role(data[2])
            except HTTPException:
                trainer_role = None
        if data[3] is not None:
            try:
                trainee_role = await guild._fetch_role(data[3])
            except HTTPException:
                trainee_role = None
        
        reqs = [Requirement.load(mgr.bot, r) for r in requirements]
        
        return cls(mgr, data[0], data[1], trainer_role, trainee_role, reqs)
        
################################################################################
    @property
    def bot(self) -> PartyBusBot:
        
        return self._manager.bot
    
################################################################################
    @property
    def id(self) -> str:
        
        return self._id
    
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
    def trainer_role(self) -> Optional[Role]:
        
        return self._trainer_role

################################################################################
    @trainer_role.setter
    def trainer_role(self, value: Optional[Role]) -> None:
        
        self._trainer_role = value
        self.update()
        
################################################################################    
    @property
    def trainee_role(self) -> Optional[Role]:
        
        return self._trainee_role

################################################################################
    @trainee_role.setter
    def trainee_role(self, value: Optional[Role]) -> None:
        
        self._trainee_role = value
        self.update()
    
################################################################################    
    @property
    def requirements(self) -> List[Requirement]:
        
        return self._requirements
    
################################################################################
    @property
    def select_option(self) -> SelectOption:
        
        return SelectOption(label=self.name, value=self.id)
    
################################################################################
    def get_requirement(self, req_id: str) -> Requirement:
            
        for r in self.requirements:
            if r.id == req_id:
                return r
            
################################################################################
    def format_qualification(self, qualifications: List[Qualification]) -> str:
        
        emoji = BotEmojis.Cross
        training_level = "Not Trained"
        
        for q in qualifications:
            if q.position == self:
                emoji = q.level.emoji
                training_level = q.level.proper_name
                break
        
        return f"{emoji} | **({training_level})** | {self.name}"
    
################################################################################
    def status(self) -> Embed:
        
        trainer_role_str = (
            f"**Trainer Role:** {self.trainer_role.mention}" if self.trainer_role is not None
            else "**LINKED TRAINER ROLE NOT FOUND**"
        )
        trainee_role_str = (
            f"**Trainee Role:** {self.trainee_role.mention}" if self.trainee_role is not None
            else "**LINKED TRAINEE ROLE NOT FOUND**"
        )
        description = (
            f"{trainer_role_str}\n"
            f"{trainee_role_str}\n"
            f"{U.draw_line(extra=25)}"
        )
        
        reqs_list = [r.description for r in self.requirements]
        reqs_list.extend(
            [f"{r.description} - **(Global)**" for r in self._manager.global_requirements]
        )
        field_value = ("* " + "\n* ".join(reqs_list)) if reqs_list else "`None`"
          
        return U.make_embed(
            title=f"Position Status for: {self.name}",
            description=description,
            fields=[
                EmbedField(
                    name="Training Requirements",
                    value=field_value,
                    inline=False
                )
            ]
        )
    
################################################################################
    async def menu(self, interaction: Interaction) -> None:
        
        status = self.status()
        view = PositionStatusView(interaction.user, self)
        
        await interaction.respond(embed=status, view=view)
        await view.wait()
        
################################################################################
    async def edit_name(self, interaction: Interaction) -> None:
        
        modal = PositionNameModal(self.name)
        
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        if not modal.complete:
            return
        
        self.name = modal.value
    
################################################################################    
    async def edit_role(self, interaction: Interaction, operation: str) -> None:
        
        modal = PositionRoleModal()
        
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        if not modal.complete:
            return
        
        try:
            role_id = int(modal.value)
        except ValueError:
            error = InvalidNumberError(modal.value)
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        try:
            role = await interaction.guild._fetch_role(role_id)
        except HTTPException:
            error = InvalidRoleIDError(modal.value)
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        if operation == "Trainer":
            self.trainer_role = role
        elif operation == "Trainee":
            self.trainee_role = role
            
        self.update()
        
################################################################################
    async def add_requirement(self, interaction: Interaction) -> None:
        
        modal = PositionRequirementModal()
        
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        if not modal.complete:
            return
        
        self._requirements.append(Requirement.new(self.bot, self.id, modal.value))
        self.update()
        
################################################################################
    async def remove_requirement(self, interaction: Interaction) -> None:
        
        embed = U.make_embed(
            title="Remove Requirement",
            description=(
                "Select the requirement you'd like to remove.\n"
                f"{U.draw_line(extra=25)}"
            )
        )
        view = RemoveRequirementView(interaction.user, self.requirement_select_options())
        
        await interaction.response.send_message(embed=embed, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        requirement = self.get_requirement(view.value)
        requirement.delete()
        
        self.requirements.remove(requirement)
        self.update()
    
################################################################################    
    def requirement_select_options(self) -> List[SelectOption]:
        
        return [r.select_option for r in self.requirements]
    
################################################################################
    def update(self) -> None:
        
        self.bot.database.update.position(self)
    
################################################################################
    