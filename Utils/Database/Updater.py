from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from .Branch import DBWorkerBranch

if TYPE_CHECKING:
    from Classes import Position, Trainer, Trainee, Qualification, Training, TUser
    from Utils import RequirementLevel
################################################################################

__all__ = ("DatabaseUpdater",)

################################################################################
class DatabaseUpdater(DBWorkerBranch):
    """A utility class for updating records in the database."""

    def update_position(self, position: Position) -> None:

        with self.database as db:
            db.execute(
                "UPDATE positions SET name = %s, trainer_role = %s, trainee_role = %s "
                "WHERE _id = %s;",
                (
                    position.name, position.trainer_role.id, position.trainee_role.id, 
                    position.id
                )
            )
    
################################################################################
    def update_trainer(self, trainer: Trainer) -> None:
        
        with self.database as db:
            db.execute(
                "UPDATE trainers SET qualifications = %s WHERE user_id = %s;",
                (
                    [q.id for q in trainer.qualifications], trainer.user.id
                )
            )
    
################################################################################
    def update_trainee(self, trainee: Trainee) -> None:
        
        with self.database as db:
            db.execute(
                "UPDATE trainees SET name = %s, trainings = %s, notes = %s "
                "WHERE _id = %s;",
                (
                    trainee.name, [t.id for t in trainee.trainings], trainee.notes, 
                    trainee.id
                )
            )
            
################################################################################
    def update_qualification(self, q: Qualification) -> None:
        
        with self.database as db:
            db.execute(
                "UPDATE qualifications SET level = %s WHERE _id = %s;",
                (q.level.value, q.id)
            )
    
################################################################################
    def update_training(self, training: Training) -> None:
                
        with self.database as db:
            db.execute(
                "UPDATE trainings SET position = %s, trainee = %s, "
                "trainer = %s WHERE _id = %s;",
                (
                    training.position.id, training.trainee.id,
                    training.trainer.id if training.trainer else None,
                    training.id
                )
            )
            
        self.update_requirement_overrides(training.id, training.requirement_overrides)
    
################################################################################        
    def update_requirement_overrides(self, training_id: str, overrides: Dict[str, RequirementLevel]) -> None:
        
        with self.database as db:
            for requirement_id, level in overrides.items():
                db.execute(
                    "SELECT * FROM requirement_overrides WHERE training = %s "
                    "AND requirement = %s;",
                    (training_id, requirement_id)
                )
                match = db.fetchone()
                
                if match:
                    db.execute(
                        "UPDATE requirement_overrides SET level = %s "
                        "WHERE training = %s AND requirement = %s;",
                        (level.value, training_id, requirement_id)
                    )
                else:
                    db.execute(
                        "INSERT INTO requirement_overrides VALUES (%s, %s, %s);",
                        (training_id, requirement_id, level.value)
                    )

################################################################################
    def update_tuser(self, tuser: TUser) -> None:
        
        with self.database as db:
            db.execute(
                "UPDATE tusers SET name = %s, notes = %s WHERE user_id = %s;",
                (tuser.name, tuser.notes, tuser.user_id)
            )
                
################################################################################
    
    position        = update_position
    trainer         = update_trainer
    trainee         = update_trainee
    training        = update_training
    qualification   = update_qualification
    tuser           = update_tuser
    
################################################################################
    