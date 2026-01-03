from enum import Enum

class Role(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

    @classmethod
    def to_string(cls, role_code):
        if cls.is_supported(role_code):
            return cls[role_code].value
        raise ValueError(f"Role code '{role_code}' is not supported.")