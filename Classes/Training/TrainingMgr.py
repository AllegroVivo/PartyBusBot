from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Any, Dict

from discord import Interaction, User, TextChannel, EmbedField

from Classes.Training.SignUpMessage import SignUpMessage
from Classes.Training.TUser import TUser
from Classes.Training.Trainee import Trainee
from Classes.Training.Training import Training
from Classes.Training.Trainer import Trainer
from UI import TrainerStatusView, TUserStatusView, TUserAdminStatusView
from Utils import Utilities as U, TraineeExistsError, TraineeNotFoundError

if TYPE_CHECKING:
    from Classes import PartyBusBot, Position
################################################################################

__all__ = ("TrainingManager",)

################################################################################
class TrainingManager:

    __slots__ = (
        "_state",
        "_tusers",
        "_message",
        "_trainings",
    )

################################################################################
    def __init__(self, state: PartyBusBot) -> None:

        self._state: PartyBusBot = state
        
        self._tusers: List[TUser] = []
        self._trainings: List[Training] = []
        
        self._message: SignUpMessage = SignUpMessage(self._state)
    
################################################################################
    def __getitem__(self, user_id: int) -> Optional[TUser]:
        
        if not isinstance(user_id, int):
            raise TypeError("TrainingManager[user_id] | user_id must be an int.")
        
        for tuser in self._tusers:
            if tuser.user_id == user_id:
                return tuser
        
################################################################################
    @property
    def bot(self) -> PartyBusBot:
        
        return self._state
    
################################################################################
    @property
    def tusers(self) -> List[TUser]:
        
        return self._tusers
    
################################################################################
    @property
    def trainer_signup_message(self) -> SignUpMessage:
        
        return self._message
    
################################################################################
    @property
    def all_trainings(self) -> List[Training]:
        
        return self._trainings
    
################################################################################
    @property
    def unmatched_trainings(self) -> List[Training]:

        return [t for t in self.all_trainings if t.trainer is None]
    
################################################################################
    async def load_all(self, data: Dict[str, Any]) -> None:
        
        tuser_data = data["tusers"]
        config_data = data["configs"]
        availability_data = data["availabilities"]
        trainers = data["trainers"]
        trainees = data["trainees"]
        qdata = data["qualifications"]
        trainings = data["trainings"]
        messages = data["messages"]
        
        user_dict: Dict[int, Dict[str, Any]] = {}
        
        for user in tuser_data:
            user_dict[user[0]] = {
                "tuser": user,
                "availability": [],
                "qualifications": [],
                "trainings": [],
                "requirement_overrides": [],
            }
        for config in config_data:
            user_dict[config[0]]["config"] = config
        for trainer in trainers:
            user_dict[trainer[0]]["trainer"] = trainer
        for trainee in trainees:
            user_dict[trainee[0]]["trainee"] = trainee
        for a in availability_data:
            try:
                user_dict[a[0]]["availability"].append(a)
            except KeyError:  # Should only happen if there's no primary TUser record
                pass
        for q in qdata:
            try:
                user_dict[q[1]]["qualifications"].append(q)
            except KeyError:
                pass
            
        overrides = {}
        for o in data["requirement_overrides"]:
            try:
                overrides[o[1]].append((o[2], o[3]))
            except KeyError:
                overrides[o[1]] = [(o[2], o[3])]
             
        for _, data in user_dict.items():
            tuser = await TUser.load(self, data)
            if tuser is not None:
                self._tusers.append(tuser)
                
        for t in trainings:
            training = Training.load(self.get_trainee(t[1]), t, overrides.get(t[0], []))
            if training is not None:
                self._trainings.append(training)
                
        await self._message.load(messages["trainer_message"])
        
################################################################################
    def get_trainee(self, user_id: int) -> Optional[Trainee]:
        
        return self[user_id].trainee if self[user_id] is not None else None
        
################################################################################
    def get_trainer(self, user_id: Optional[int]) -> Optional[Trainer]:
        
        if user_id is None:
            return

        return self[user_id].trainer if self[user_id] is not None else None
           
################################################################################
    def get_training(self, trainee_user_id: int, pos_id: str) -> Optional[Training]:
    
        for t in self._trainings:
            if t.trainee.user_id == trainee_user_id and t.position.id == pos_id:
                return t
    
################################################################################        
    def get_trainings_by_user(self, user_id: int) -> List[Training]:
        
        return [t for t in self._trainings if t.trainee.user_id == user_id]
    
################################################################################
    def get_positions(self, position_ids: List[str]) -> List[Position]:
        
        ret = []
        for position_id in position_ids:
            position = self._state.position_manager.get_position(position_id)
            if position is not None:
                ret.append(position)
                
        return ret            
    
################################################################################
    def get_trainings_by_position(self, position_id: str) -> List[Training]:
        
        return [t for t in self._trainings if t.position.id == position_id]
    
################################################################################        
    def add_tuser(self, user: User) -> TUser:
        
        tuser = TUser.new(self.bot, user)
        self._tusers.append(tuser)
        
        return tuser
    
################################################################################
    async def trainer_status(self, interaction: Interaction, user: User) -> None:
        
        trainer = self.get_trainer_by_user_id(user.id)
        if trainer is None:
            trainer = Trainer.new(self.bot, user)
            self._trainers.append(trainer)
        
        status = trainer.status()
        view = TrainerStatusView(interaction.user, trainer)
        
        await interaction.respond(embed=status, view=view)
        await view.wait()
        
################################################################################
    async def tuser_status(self, interaction: Interaction) -> None:

        tuser = self[interaction.user.id]
        if tuser is None:
            tuser = self.add_tuser(interaction.user)

        status = tuser.trainee_status()
        view = TUserStatusView(interaction.user, tuser)

        await interaction.respond(embed=status, view=view)
        await view.wait()

################################################################################
    async def update_training(self, interaction: Interaction, user: User) -> None:

        trainee = self.get_trainee(user.id)
        if trainee is None:
            error = TraineeNotFoundError(user)
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        await trainee.update_training(interaction)

################################################################################
    async def tuser_admin_status(self, interaction: Interaction, user: User) -> None:
        
        tuser = self[user.id]
        if tuser is None:
            tuser = self.add_tuser(user)
        
        status = tuser.status()
        view = TUserAdminStatusView(interaction.user, tuser)
        
        await interaction.respond(embed=status, view=view)
        await view.wait()

################################################################################
    async def post_signup_message(self, interaction: Interaction, channel: TextChannel) -> None:
        
        await self._message.post_signup_message(interaction, channel)

################################################################################
    def add_training(self, training: Training) -> None:
        
        self._trainings.append(training)
        
################################################################################
    def remove_training(self, training_id: str) -> None:
        
        for t in self._trainings:
            if t.id == training_id:
                self._trainings.remove(t)
                t.delete()
                return

################################################################################
    async def manage_trainers(self, interaction: Interaction) -> None:
        
        status = U.make_embed(
            title="Manage Trainers",
            description="Manage trainer assignments.",
            fields=self.all_position_fields(),
        )
        
        await interaction.respond(embed=status)

################################################################################
    def all_position_fields(self) -> List[EmbedField]:
        
        ret = []
        
        for pos in self.bot.position_manager.positions:
            pos_trainings = self.get_trainings_by_position(pos.id)
            pos_str = ""
            
            if not pos_trainings:
                pos_str = "`No Trainees`"
            else:
                for t in pos_trainings:
                    trainer_str = f"`{t.trainer.name}`" if t.trainer is not None else "`No Trainer Assigned`"
                    pos_str += f"* {t.trainee.name}\n{trainer_str}\n"
                
            ret.append(
                EmbedField(
                    name=pos.name,
                    value=pos_str,                        
                    inline=True
                )
            )
            
        return ret
    
################################################################################
