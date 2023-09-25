from app.config import database
from .repository.auth_repository import AuthRepository
from .repository.transcription_repository import TranscriptionRepository

class Service:
    def __init__(self):
        self.auth_repository = AuthRepository(database)
        self.transcription_repository = TranscriptionRepository(database)  


def get_service():
    return Service()

def check_words_in_text(words, text):
    word_set = set(words)
    text_words = set(text.lower().split())  # Convert to lowercase to perform case-insensitive search
    return bool(word_set.intersection(text_words))
    