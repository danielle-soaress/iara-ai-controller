from datetime import datetime
from app.models.enum.role import Role

class MessageModel:
    def __init__(self, role: Role, content: str, _id = None):
        self._id = _id
        self.role = role
        self.content = content
        self.created_at = datetime.datetime.utcnow()
    
    def to_dict(self):
        return {
            "_id": self._id,
            "role": self.role.value if isinstance(self.role, Role) else self.role,
            "content": self.content,
            "timestamp": self.created_at
        }