from enum import Enum
import random

class ChatThemes(Enum):
    TA = "Travel and Adventures"
    DD = "Day by Day"
    BT = "Business and Tech"
    PC = "Pop culture"
    F  = "Free conversation"
    C  = "Challenge"

    @classmethod
    def list_themes(cls):
        return [theme for theme in cls]
    
    @classmethod
    def is_valid_theme(cls, theme_code):
        return theme_code in cls.__members__

    @classmethod
    def from_string(cls, theme_code):
        try:
            return cls[theme_code]
        except KeyError:
            print("Invalid theme code")
            return None
    
    @classmethod
    def challenge_theme(cls):
        themes = [tema for tema in ChatThemes if tema != ChatThemes.F]
        return random.choice(themes)
