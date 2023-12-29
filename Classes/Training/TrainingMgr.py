from __future__ import annotations

from discord import Interaction, User, NotFound
from typing import TYPE_CHECKING, List, Optional, Tuple, Any, Dict, Union

from Classes.Training.Qualification import Qualification
from Classes.Training.Trainee import Trainee
from Classes.Training.Trainer import Trainer
from Classes.Training.Training import Training
from Classes.Training.TUser import TUser
from UI import TrainerStatusView, TraineeStatusView, UpdateTraineeView, TUserStatusView
from Utils import TrainerExistsError, TrainerNotFoundError, TraineeExistsError, TraineeNotFoundError

if TYPE_CHECKING:
    from Classes import PartyBusBot, Position
################################################################################

__all__ = ("TrainingManager",)

################################################################################
class TrainingManager:

    __slots__ = (
        "_state",
        "_tusers",
    )

################################################################################
    def __init__(self, state: PartyBusBot) -> None:

        self._state: PartyBusBot = state
        self._tusers: List[TUser] = []
    
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
    async def load_all(self, data: Dict[str, Any]) -> None:
        
        tuser_data = data["tusers"]
        config_data = data["configs"]
        availability_data = data["availabilities"]
        trainers = data["trainers"]
        trainees = data["trainees"]
        qdata = data["qualifications"]
        trainings = data["trainings"]
        
        user_dict: Dict[int, Dict[str, Any]] = {}
        
        for user in tuser_data:
            user_dict[user[0]] = {
                "tuser": user,
                "availability": [],
                "qualifications": [],
                "trainings": [],
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
        for t in trainings:
            try:
                user_dict[t[1]]["trainings"].append(t)
            except KeyError:
                pass
                
        temp = []
        for _, data in user_dict.items():
            tuser = await TUser.load(self, data)
            if tuser is not None:
                temp.append(tuser)
                self._tusers.append(tuser)
        
################################################################################
    def get_trainee(self, user_id: int) -> Optional[Trainee]:
        
        tuser = self[user_id]
        if tuser is not None:
            return tuser.trainee
        
################################################################################
    def get_trainer(self, user_id: Optional[int]) -> Optional[Trainer]:
        
        if user_id is None:
            return
        
        tuser = self[user_id]
        if tuser is not None:
            return tuser.trainer
            
################################################################################
    def get_positions(self, position_ids: List[str]) -> List[Position]:
        
        ret = []
        for position_id in position_ids:
            position = self._state.position_manager.get_position(position_id)
            if position is not None:
                ret.append(position)
                
        return ret            
    
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
    async def add_trainee(self, interaction: Interaction) -> None:
        
        match = self.get_trainee_by_user_id(interaction.user.id)
        if match is not None:
            error = TraineeExistsError(interaction.user)
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        trainee = Trainee.new(self.bot, interaction.user)
        self._trainees.append(trainee)
        
        await self.trainee_status(interaction)
        
################################################################################
    async def trainee_status(self, interaction: Interaction) -> None:
        
        trainee = self.get_trainee_by_user_id(interaction.user.id)
        if trainee is None:
            error = TraineeNotFoundError(interaction.user)
            await interaction.respond(embed=error, ephemeral=True)
            return
    
        await trainee.menu(interaction)

################################################################################
    async def update_training(self, interaction: Interaction, user: User) -> None:

        trainee = self.get_trainee_by_user_id(user.id)
        if trainee is None:
            error = TraineeNotFoundError(user)
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        status = trainee.status()
        view = UpdateTraineeView(interaction.user, trainee)
        
        await interaction.respond(embed=status, view=view)
        await view.wait()

################################################################################
    async def tuser_status(self, interaction: Interaction, user: User) -> None:
        
        tuser = self[user.id]
        if tuser is None:
            tuser = self.add_tuser(user)
        
        status = tuser.status()
        view = TUserStatusView(interaction.user, tuser)
        
        await interaction.respond(embed=status, view=view)
        await view.wait()
        
################################################################################
