from datetime import datetime
from typing import Optional

from bson.objectid import ObjectId
from pymongo.database import Database


class TranscriptionRepository:
    def __init__(self, database: Database):
        self.database = database

    def add_new_transcription(self, user_id: str, transcription: str):
        transcription_data = {
            "transcription": transcription.transcription,
            "timestamp": transcription.timestamp,
        }

        self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={"$push": {"transcriptions": transcription_data}},
        )