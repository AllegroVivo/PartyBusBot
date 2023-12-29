from __future__ import annotations

from discord import Interaction, SelectOption, Embed, EmbedField
from typing import TYPE_CHECKING, List, Tuple, Optional, Dict, Any
from Classes.Positions.Position import Position
from Classes.Positions.Requirement import Requirement
from UI.Positions import (
    PositionGeneralStatusView,
    PositionStatusView,
    GlobalRequirementModal,
    GlobalRequirementsView,
    RemoveRequirementView
)
from Utils import Utilities as U
from Utils import PositionExistsError, RoleNotFoundError, PositionNotFoundError

if TYPE_CHECKING:
    from Classes import PartyBusBot
################################################################################

__all__ = ("PositionManager", )

################################################################################
class PositionManager:

    __slots__ = (
        "_state",
        "_positions",
        "_requirements",
    )
    
################################################################################
    def __init__(self, state: PartyBusBot) -> None:
        
        self._state: PartyBusBot = state
        
        self._positions: List[Position] = []
        self._requirements: List[Requirement] = []
    
################################################################################
    @property
    def bot(self) -> PartyBusBot:
        
        return self._state
    
################################################################################
    @property
    def positions(self) -> List[Position]:
        
        self._positions.sort(key=lambda p: p.name)
        return self._positions
    
################################################################################
    @property
    def global_requirements(self) -> List[Requirement]:
        
        return self._requirements
    
################################################################################
    async def load_all(self, data: Dict[str, Any]) -> None:
        
        position_data = data["positions"]
        requirement_data = data["requirements"]
        
        requirements = {"0": []}
        for req in requirement_data:
            if req[1] not in requirements.keys():
                requirements[req[1]] = []
            requirements[req[1]].append(req)
            
        self._requirements.extend(
            [Requirement.load(self.bot, r) for r in requirements["0"]]
        )
        
        for pos in position_data:
            reqs = requirements.get(pos[0], [])
            self._positions.append(await Position.load(self, pos, reqs))
        
################################################################################
    def select_options(self) -> List[SelectOption]:
    
        return [p.select_option for p in self.positions]
    
################################################################################
    def get_position(self, position_id: str) -> Position:
        
        for position in self.positions:
            if position.id == position_id:
                return position
            
################################################################################
    def get_position_by_name(self, position_name: Optional[str]) -> Optional[Position]:
        
        if position_name is None:
            return None
        
        for position in self.positions:
            if position.name.lower() == position_name.lower():
                return position
          
################################################################################
    def get_global_requirement(self, req_id: str) -> Requirement:
    
        for r in self.global_requirements:
            if r.id == req_id:
                return r
        
################################################################################
    async def add_position(self, interaction: Interaction, position_name: str) -> None:
        
        position = self.get_position_by_name(position_name)
        if position is not None:
            error = PositionExistsError(position_name)
            await interaction.respond(embed=error, ephemeral=True)
            return

        position = Position.new(self, position_name.title())
        self._positions.append(position)

        await position.menu(interaction)
        
################################################################################
    async def position_status(self, interaction: Interaction, pos_name: Optional[str]) -> None:

        position = self.get_position_by_name(pos_name)
        if pos_name is not None and position is None:
            error = PositionNotFoundError(pos_name)
            await interaction.respond(embed=error, ephemeral=True)
            return
        elif position is not None:
            await position.menu(interaction)
            return
            
        status = self.general_status()
        view = PositionGeneralStatusView(interaction.user, self.select_options())
        
        await interaction.respond(embed=status, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        position = self.get_position(view.value)
        await position.menu(interaction)
        
################################################################################
    def general_status(self) -> Embed:
        
        return U.make_embed(
            title="Position Status",
            description=(
                "To view or edit info on specific position,\n"
                "select that job from the dropdown below.\n"
                f"{U.draw_line(extra=25)}"
            ),
            fields=[
                EmbedField(
                    name="__Current Registered Jobs__",
                    value="* " + "\n* ".join([p.name for p in self.positions]) or "None",
                    inline=False
                )
            ]
        )
    
################################################################################
    def global_requirements_status(self) -> Embed:
        
        return U.make_embed(
            title="Global Job Training Requirements",
            description=(
                "These requirements are applied to all jobs.\n"
                f"{U.draw_line(extra=25)}"
            ),
            fields=[
                EmbedField(
                    name="__Current Global Requirements__",
                    value=(
                        ("* " + "\n* ".join([r.description for r in self.global_requirements]))
                        if self.global_requirements else "`None`"
                    ),
                    inline=False
                )
            ]
        )
    
################################################################################
    async def global_requirements_menu(self, interaction: Interaction) -> None:
        
        status = self.global_requirements_status()
        view = GlobalRequirementsView(interaction.user, self)
        
        await interaction.respond(embed=status, view=view)
        await view.wait()
        
################################################################################
    async def add_global_requirement(self, interaction: Interaction) -> None:
        
        modal = GlobalRequirementModal()
        
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        if not modal.complete:
            return
        
        requirement = Requirement.new(self.bot, "0", modal.value)
        self._requirements.append(requirement)
    
################################################################################
    async def remove_global_requirement(self, interaction: Interaction) -> None:

        embed = U.make_embed(
            title="Remove Requirement",
            description=(
                "Select the global job requirement you'd like to remove.\n"
                f"{U.draw_line(extra=30)}"
            )
        )
        view = RemoveRequirementView(interaction.user, self.global_requirement_select_options())
        
        await interaction.response.send_message(embed=embed, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        requirement = self.get_global_requirement(view.value)
        requirement.delete()

        self._requirements.remove(requirement)

################################################################################    
    def global_requirement_select_options(self) -> List[SelectOption]:

        return [r.select_option for r in self._requirements]
    
################################################################################
