from __future__ import annotations

from .Branch import DBWorkerBranch
################################################################################

__all__ = ("DatabaseBuilder",)

################################################################################
class DatabaseBuilder(DBWorkerBranch):
    """A utility class for building and asserting elements of the database."""

    def build_all(self) -> None:

        self.build_positions_tables()
        self.build_training_tables()
        
        print("Database lookin' good!")
    
################################################################################
    def build_positions_tables(self) -> None:

        with self.database as db:
            db.execute(
                "CREATE TABLE IF NOT EXISTS positions ("
                "_id TEXT PRIMARY KEY,"
                "name TEXT,"
                "trainer_role BIGINT,"
                "trainee_role BIGINT"
                ");"
            )
            db.execute(
                "CREATE TABLE IF NOT EXISTS requirements ("
                "_id TEXT PRIMARY KEY,"
                "position TEXT,"
                "description TEXT"
                ");"
            )
 
################################################################################
    def build_training_tables(self) -> None:
        
        with self.database as db:
            db.execute(
                "CREATE TABLE IF NOT EXISTS tusers ("
                "user_id BIGINT PRIMARY KEY ,"
                "name TEXT,"
                "notes TEXT"
                ");"
            )
            db.execute(
                "CREATE TABLE IF NOT EXISTS tuser_config ("
                "user_id BIGINT PRIMARY KEY,"
                "image_url TEXT,"
                "timezone INTEGER"
                ");"
            )
            db.execute(
                "CREATE TABLE IF NOT EXISTS availability ("
                "user_id BIGINT,"
                "day INTEGER,"
                "start_time INTEGER,"
                "end_time INTEGER"
                ");"
            )
            db.execute(
                "CREATE TABLE IF NOT EXISTS trainers ("
                "user_id BIGINT PRIMARY KEY"
                ");"
            )
            db.execute(
                "CREATE TABLE IF NOT EXISTS trainees ("
                "user_id BIGINT PRIMARY KEY"
                ");"
            )
            db.execute(
                "CREATE TABLE IF NOT EXISTS qualifications ("
                "_id TEXT PRIMARY KEY,"
                "user_id BIGINT,"
                "position TEXT,"
                "level INTEGER"
                ");"
            )
            db.execute(
                "CREATE TABLE IF NOT EXISTS trainings ("
                "_id TEXT PRIMARY KEY,"
                "user_id BIGINT,"
                "position TEXT,"
                "trainer BIGINT"
                ");"
            )
            
################################################################################