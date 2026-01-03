from enum import Enum

class Language(Enum):
    EN = "English"
    PT = "Portuguese"
    ES = "Spanish"
    FR = "French"
    IT = "Italian"

    @classmethod
    def is_supported(cls, lang_code):
        return lang_code in cls.__members__
    
    @classmethod
    def to_string(cls, lang_code):
        if cls.is_supported(lang_code):
            return cls[lang_code].value
        raise ValueError(f"Language code '{lang_code}' is not supported.")