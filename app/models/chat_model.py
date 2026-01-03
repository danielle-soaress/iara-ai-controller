from datetime import datetime
from app.models.enum.chat_themes import ChatThemes
from app.models.enum.language import Language

class ChatModel:
    def __init__(self, user_id: str, theme: ChatThemes, target_language: Language, feedback_language: Language, messages=None, _id=None):
        self._id = _id
        self.user_id = user_id
        self.theme = theme
        self.target_language = target_language
        self.feedback_language = feedback_language
        self.created_at = datetime.datetime.utcnow()
        self.messages = []

        if messages:
            for message in messages:
                self.add_message(message)
    
    def to_dict(self):
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "theme": self.theme,
            "target_language": self.target_language.value if isinstance(self.target_language, Language) else self.target_language,
            "feedback_language": self.feedback_language.value if isinstance(self.feedback_language, Language) else self.feedback_language,
            "messages": [message.to_dict() if hasattr(message, "to_dict") else message for message in self.messages]
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            user_id=data.get("user_id"),
            theme=data.get("theme"),
            target_language=data.get("target_language"),
            feedback_language=data.get("feedback_language"),
            messages=data.get("messages", []),
            _id=data.get("_id")
        )