from app.extensions import mongo
from app.models.chat_model import ChatModel
from pymongo.errors import PyMongoError, InvalidId
from bson import ObjectId

class ChatRepository:
    def __init__(self):
        self.collection = mongo.db.chats

    # save or update a chat
    def save(self, chat: ChatModel) -> str:

        payload = chat.to_dict()

        try:
            if chat._id:
                self.collection.replace_one(
                    {"_id": ObjectId(chat._id)},
                    payload
                )
                return chat._id
            else:
                payload.pop("_id", None)
                result = self.collection.insert_one(payload)
                return str(result.inserted_id)
        except PyMongoError as e:
            raise Exception(f"Error while trying to save chat: {e}")

    def find_all_by_user_id(self, user_id: str):
        try:
            chats = self.collection.find({"user_id": user_id})
            return [ChatModel.from_dict(chat) for chat in chats]
        except PyMongoError as e:
            raise Exception(f"Error while trying to find chats by user ID: {e}")

    def find_by_chat_id(self, chat_id: str):
        try:
            chat = self.collection.find_one({"_id": ObjectId(chat_id)})
            return ChatModel.from_dict(chat) if chat else None
        except InvalidId:
            return None
        except PyMongoError as e:
            raise Exception(f"Error while trying to find chat by ID: {e}")

    def add_message(self, chat_id: str, message_dict: dict):
        try:
            self.collection.update_one({"_id": ObjectId(chat_id)},
                                      {"$push": {"messages": message_dict}})
        except InvalidId:
            raise ValueError("Invalid ID.")
        except PyMongoError as e:
            raise Exception(f"Error while trying to connect to database: {e}")

    def delete_chat_by_id(self, chat_id: str):
        try:
            result = self.collection.delete_one({"_id": ObjectId(chat_id)})

            if result.deleted_count == 0:
                print("No chat found with the given ID. Nothing was deleted.")
        except InvalidId:
            raise ValueError("Invalid ID.")
        except PyMongoError as e:
            raise Exception(f"Error while trying to connect to database: {e}")

    def delete_chat_by_user_id(self, user_id: str):
        try:
            result = self.collection.delete_many({"user_id": user_id})

            if result.deleted_count == 0:
                print("No chats found for the given user ID. Nothing was deleted.")
        except InvalidId:
            raise ValueError("Invalid ID.")
        except PyMongoError as e:
            raise Exception(f"Error while trying to connect to database: {e}")