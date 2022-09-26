import json
from users_app.jwt_service import JwtService
from .redis_service import RedisService
from notes_log import get_logger


lg = get_logger(name="(Redis)",
                file_name="notes_log.log")


def verify_token(function):
    def wrapper(self, request):
        token = request.headers.get("Token")
        if not token:
            raise Exception("Token is invalid")
        decode = JwtService().decode(token=token)
        user_id = decode.get("user_id")
        if not user_id:
            raise Exception("Invalid user")
        request.data.update({"user": user_id})
        return function(self, request)
    return wrapper


class RedisNote:
    def __init__(self):
        self.redis = RedisService()

    def save_note(self, notes, user_id):
        try:
            note_dict = self.get_note(user_id)
            note_id = notes.get("id")  # 67
            note_dict.update({note_id: notes})
            self.redis.setter(user_id, json.dumps(note_dict))
            # 36: {'67': {'id': 67, 'title': 'cluster the pinacle', 'description': 'the concurrent close to nostalgia', 'user': 36}}
        except Exception as e:
            lg.error(e)

    def get_note(self, user_id):
        try:
            payload = self.redis.getter(user_id)
            # b'{"67": {"id": 67, "title": "cluster the pinacle", "description": "the concurrent close to nostalgia", "user": 36}}'
            return json.loads(payload) if payload else {}
            # {'67': {'id': 67, 'title': 'cluster the pinacle', 'description': 'the concurrent close to nostalgia', 'user': 36}}
        except Exception as e:
            lg.error(e)

    def delete_note(self, user_id, note_id):
        try:
            note_dict = self.get_note(user_id)
            notes = note_dict.get(note_id)
            if notes is not None:
                note_dict.pop(note_id)
                self.redis.setter(user_id, json.dumps(note_dict))
        except Exception as e:
            lg.error(e)
