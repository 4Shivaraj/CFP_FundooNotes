from django.http import JsonResponse
from users_app.models import User
from notes_log import get_logger
import json

lg = get_logger(name="(custom models)", file_name="notes_log.log")


def registration(request):
    """registering user details to the database method must be POST

    Args:
        request : accepting the request, and load the body with user details in a postman

    Returns:
        returning json response with success message
    """
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            user_details = User(user_name=data.get("user_name"), pass_word=data.get("pass_word"), email=data.get(
                "email"), phone_number=data.get("phone_number"), location=data.get("location"))
            user_details.save()
            lg.debug(f" user {user_details.user_name} registred successfully")
            return JsonResponse({"message": f" User {user_details.user_name} registred successfully"})
        else:
            lg.info("Invalid HTTP method")
    except Exception as e:
        lg.error(e)


def login(request):
    """login to the user app,method must be POST

    Args:
        request : accepting the request load the body with user name and pass word

    Returns:
        returning json response with success message
    """
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            login_details = User.objects.filter(user_name=data.get(
                "user_name"), pass_word=data.get("pass_word"))
            if login_details is not None:
                lg.debug("User is successfully logged in")
                return JsonResponse({"message": "User is successfully logged in"})
            else:
                return JsonResponse({"message": "Invalid Credentials"})
        else:
            lg.info("Invalid HTTP method")
    except Exception as e:
        lg.error(e)
