from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from .Branch import DBWorkerBranch

if TYPE_CHECKING:
    from Classes import Position, Trainer, Trainee, Qualification, Training, TUser, SignUpMessage, Job
    from Utils import RequirementLevel
################################################################################

__all__ = ("DatabaseUpdater",)

################################################################################
class DatabaseUpdater(DBWorkerBranch):
    """A utility class for updating records in the database."""

    def update_position(self, position: Position) -> None:
        
        trainer_role_id = position.trainer_role.id if position.trainer_role else None
        trainee_role_id = position.trainee_role.id if position.trainee_role else None

        with self.database as db:
            db.execute(
                "UPDATE positions SET name = %s, trainer_role = %s, trainee_role = %s "
                "WHERE _id = %s;",
                (
                    position.name, trainer_role_id, trainee_role_id, position.id
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
                "UPDATE trainings SET position = %s, trainer = %s WHERE _id = %s;",
                (
                    training.position.id, training.trainer.user.id if training.trainer else None,
                    training.id
                )
            )
            
        self.update_requirement_overrides(training)
    
################################################################################        
    def update_requirement_overrides(self, training: Training) -> None:
        
        with self.database as db:
            for requirement_id, level in training.requirement_overrides.items():
                db.execute(
                    "SELECT * FROM requirement_overrides WHERE training_id = %s "
                    "AND requirement_id = %s;",
                    (training.id, requirement_id)
                )
                match = db.fetchone()
                
                if match:
                    db.execute(
                        "UPDATE requirement_overrides SET level = %s "
                        "WHERE training_id = %s AND requirement_id = %s;",
                        (level.value, training.id, requirement_id)
                    )
                else:
                    db.execute(
                        "INSERT INTO requirement_overrides VALUES (%s, %s, %s, %s);",
                        (training.user_id, training.id, requirement_id, level.value)
                    )

################################################################################
    def update_tuser(self, tuser: TUser) -> None:
        
        with self.database as db:
            db.execute(
                "UPDATE tusers SET name = %s, notes = %s WHERE user_id = %s;",
                (tuser.name, tuser.notes, tuser.user_id)
            )
            db.execute(
                "UPDATE tuser_config SET image_url = %s, job_pings = %s "
                "WHERE user_id = %s;",
                (tuser.config.image, tuser.config.job_pings, tuser.user_id)
            )
    
################################################################################      
    def update_trainer_signup_message(self, message: SignUpMessage) -> None:
    
        with self.database as db:
            db.execute(
                "UPDATE messages SET channel_id = %s, message_id = %s "
                "WHERE _id = 'trainer_signup_message';",
                (message.channel_id, message.message_id)
            )
    
################################################################################
    def update_job(self, job: Job) -> None:
        
        with self.database as db:
            db.execute(
                "UPDATE jobs SET position = %s, venue = %s, description = %s, "
                "date = %s, start_time = %s, end_time = %s, pay_rate = %s,"
                "pay_type = %s, applicant = %s, requester = %s WHERE _id = %s;",
                (
                    job.position.id if job.position is not None else None,
                    job.venue, job.description, job.job_date, job.start_time, 
                    job.end_time, job.pay_rate, 
                    job.pay_type.value if job.pay_type is not None else None,
                    job.requestor.id, job.applicant.id if job.applicant is not None else None,
                    job.id
                )
            )
            
################################################################################
    
    position        = update_position
    trainer         = update_trainer
    trainee         = update_trainee
    training        = update_training
    qualification   = update_qualification
    tuser           = update_tuser
    trainer_message = update_trainer_signup_message
    job             = update_job
    
################################################################################
    