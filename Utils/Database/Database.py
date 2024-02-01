from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Dict

import psycopg2
from dotenv import load_dotenv
from psycopg2 import InterfaceError

from .Worker import DatabaseWorker

if TYPE_CHECKING:
    from psycopg2.extensions import connection, cursor

    from .Inserter import DatabaseInserter
    from .Updater import DatabaseUpdater
    from .Deleter import DatabaseDeleter
    from Classes.Bot import PartyBusBot
################################################################################

__all__ = ("Database", )

################################################################################
class Database:
    """Database class for handling all database interactions."""

    __slots__ = (
        "_state",
        "__connection",
        "_cursor",
        "_worker",
    )

################################################################################
    def __init__(self, bot: PartyBusBot):

        self._state: PartyBusBot = bot

        self.__connection: connection = None  # type: ignore
        self._connect()

        self._cursor: cursor = None  # type: ignore
        self._worker: DatabaseWorker = DatabaseWorker(bot)

################################################################################
    def _connect(self) -> None:
        
        print("Connecting to Database...")
        
        self.__connection = None
        self._cursor = None

        load_dotenv()
        self.__connection = psycopg2.connect(
            os.getenv("DATABASE_URL"), sslmode="require"
        )

        print("Connected successfully!")

################################################################################
    def __enter__(self) -> cursor:

        if not self.__connection:
            self._connect()

        self._get_cursor()
        return self._cursor

################################################################################
    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:

        self._commit()
        self._close_cursor()

################################################################################
    def _commit(self) -> None:

        try:
            self.__connection.commit()
        except InterfaceError:
            self._connect()
            self._commit()

################################################################################
    def _get_cursor(self) -> None:

        try:
            self._cursor = self.__connection.cursor()
        except InterfaceError:
            self._connect()
            self._get_cursor()

################################################################################
    def _close_cursor(self) -> None:

        try:
            self._cursor.close()
        except InterfaceError:
            pass

################################################################################
    @property
    def connection(self) -> connection:

        return self.__connection

################################################################################
    @property
    def cursor(self) -> None:

        raise Exception(
            "Cursor is not a property of Database. Use a context manager block instead."
        )

################################################################################
    @property
    def insert(self) -> DatabaseInserter:

        return self._worker._inserter

################################################################################
    @property
    def update(self) -> DatabaseUpdater:

        return self._worker._updater

################################################################################

    @property
    def delete(self) -> DatabaseDeleter:

        return self._worker._deleter

################################################################################
    def assert_structure(self) -> None:

        self._worker.build_all()

################################################################################
    def load_all(self) -> Dict[str, Any]:

        return self._worker.load_all()

################################################################################
