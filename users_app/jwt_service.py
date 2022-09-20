from asyncio import exceptions
import jwt
# from jwt import exceptions


class JwtService:
    def encode(self, data):
        """
        encoding after checking if instance is dictionary using jwt encode
        """
        if not isinstance(data, dict):
            raise Exception("data should be dictionary")
        return jwt.encode(data, "secret", algorithm="HS256")

    def decode(self, token):
        try:
            return jwt.decode(token, "secret", algorithms="HS256")
        except jwt.exceptions.PyJWTError as e:
            raise e
