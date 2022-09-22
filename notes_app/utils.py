from users_app.jwt_service import JwtService


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
