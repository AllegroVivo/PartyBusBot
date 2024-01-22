from __future__ import annotations

import json

from discord import Embed, Interaction, Message, TextChannel, HTTPException, NotFound, EmbedField, SelectOption
from discord.ui import View
from typing import TYPE_CHECKING, Optional, Any, Tuple, List

from UI import ConfirmCancelView, TrainerMessageSelectView, SelectPositionView
from Utils import Utilities as U, TraineeMissingError, UnqualifiedError, ChannelNotSetError

if TYPE_CHECKING:
    from Classes import PartyBusBot, TrainingManager
    from UI import FroggeView
################################################################################

__all__ = ("SignUpMessage",)

################################################################################
class SignUpMessage:
    
    __slots__ = (
        "_state",
        "_channel",
        "_message",
    )
    
################################################################################
    def __init__(self, state: PartyBusBot):
    
        self._state: PartyBusBot = state
        
        self._channel: Optional[TextChannel] = None
        self._message: Optional[Message] = None
        
################################################################################
    async def load(self, data: Tuple[Any, ...]) -> None:
        
        channel_id = data[0]
        message_id = data[1]
        
        if channel_id is None:
            return
        
        try:
            self._channel = await self._state.fetch_channel(channel_id)
        except (HTTPException, NotFound):
            self._channel = None
            self._message = None
            self.update()
            return
            
        if message_id is None:
            return
        
        try:
            self._message = await self._channel.fetch_message(message_id)
        except (HTTPException, NotFound):
            self._message = None
            self.update()
            return
            
        await self.update_components()
        
################################################################################
    def update(self) -> None:

        self._state.database.update.trainer_message(self)
    
################################################################################
    @property
    def channel_id(self) -> Optional[int]:
        
        return self._channel.id if self._channel is not None else None
    
################################################################################
    @property
    def message_id(self) -> Optional[int]:
        
        return self._message.id if self._message is not None else None
    
################################################################################
    @property
    def channel(self) -> Optional[TextChannel]:
        
        return self._channel
    
################################################################################
    @channel.setter
    def channel(self, value: Optional[TextChannel]) -> None:
        
        self._channel = value       
        self.message = None
        
################################################################################
    @property
    def message(self) -> Optional[Message]:
        
        return self._message
    
################################################################################
    @message.setter
    def message(self, value: Optional[Message]) -> None:
        
        self._message = value        
        self.update()
        
################################################################################
    @property
    def training_manager(self) -> TrainingManager:
        
        return self._state.training_manager
    
################################################################################
    def status(self) -> Embed:
        
        return U.make_embed(
            title="__TRAINER/TRAINEE MATCHING__",
            description=(
                "This is the sign up message for the trainer/trainee matching system. "
                "If you are a trainer and wish to pick up a trainee, please select the "
                "trainee's name from the selector below.\n\n"
                
                "Please consider your selection carefully. Once you have selected a "
                "trainee, you will be unable to change your selection without consulting "
                "a member of management.\n"
                f"{U.draw_line(extra=35)}"
            ),
            fields=self.available_trainee_fields(),
        )
    
################################################################################
    def status_view(self) -> View:

        unmatched_trainings = [
            t for t in self._state.training_manager.all_trainings
            if t.trainer is None
        ]
        
        options = []
        for t in unmatched_trainings:
            options.append(
                SelectOption(
                    label=t.trainee.user.name,
                    description=f"({t.position.name})",
                    value=str(t.user_id),
                )
            )
        
        return TrainerMessageSelectView(self, options)
    
################################################################################
    def available_trainee_fields(self) -> List[EmbedField]:
        
        position_dict = { p.name: [] for p in self._state.position_manager.positions }
        
        for training in self._state.training_manager.unmatched_trainings:
            position_dict[training.position.name].append(training)
        
        fields = []
        for position_name, trainings in position_dict.items():
            if len(trainings) == 0:
                continue
            
            value = "\n".join(
                [f"`{t.trainee.user.name}` - {t.trainee.user.mention}" for t in trainings]
            )
            fields.append(EmbedField(name=position_name, value=value))
            
        return fields

################################################################################
    async def post_signup_message(self, interaction: Interaction, channel: Optional[TextChannel] = None) -> None:
        
        if self.channel is None and channel is None:
            error = ChannelNotSetError()
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        if channel is not None:
            self.channel = channel
        
        view = self.status_view() 
        if self._message is not None:
            try:
                await self.message.delete()
            except (HTTPException, NotFound):
                pass
            
        self._message = await self.channel.send(
            embed=self.status(),
            view=view,
        )
        
        await interaction.respond("**Thinking...**", delete_after=0.1)
        await view.wait()
        
        await self.handle_trainee_assignment(interaction, view.value)

################################################################################
    async def update_components(self) -> None:
        
        if self._message is None:
            return
        
        view = self.status_view()
        
        await self._message.edit(embed=self.status(), view=view)
        await view.wait()

################################################################################
    async def handle_trainee_assignment(self, interaction: Interaction, value: int) -> None:
        
        trainee = self._state.training_manager.get_trainee(value)
        if trainee is None:
            error = TraineeMissingError(value)
            await self.channel.send(embed=error, delete_after=30)
            return
        
        trainer = self._state.training_manager.get_trainer(interaction.user.id)
        
        trainee_positions = [t.position for t in trainee.trainings]
        trainer_positions = [t.position for t in trainer.qualifications]
        common_positions = [pos for pos in trainer_positions if pos in trainee_positions]
        
        if not common_positions:
            error = UnqualifiedError(trainer.user)
            await self.channel.send(embed=error, delete_after=30)
            return
        
        position_options = [
            SelectOption(label=pos.name, value=pos.id)
            for pos in common_positions
        ]
        pos_id = position_options[0].value
        if len(position_options) > 1:
            embed = U.make_embed(
                title="__SELECT POSITION__",
                description=(
                    "You are qualified to train this trainee in multiple positions. "
                    "Please select the position you wish to train them in."
                ),
            )
            view = SelectPositionView(interaction.user, position_options)
            
            await self.channel.send(embed=embed, view=view)
            await view.wait()
            
            if not view.complete:
                return
            
            pos_id = view.value
        
        confirm = U.make_embed(
            title="__CONFIRM TRAINEE ASSIGNMENT__",
            description=(
                f"Are you sure you want to assign `{trainee.name}`\n"
                f"({trainee.user.mention})\n"
                f"to the trainer `{trainer.name}`?"
            ),
        )
        view = ConfirmCancelView(interaction.user)
        
        await self.channel.send(embed=confirm, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        training = self._state.training_manager.get_training(trainee.user.id, pos_id)
        training.set_trainer(trainer)
        
        await trainee.notify_of_selection(training)
        await self.post_signup_message(interaction)

################################################################################
