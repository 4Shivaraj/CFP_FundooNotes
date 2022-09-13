from telnetlib import STATUS
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.forms import model_to_dict
from notes_log import get_logger
import json

lg = get_logger(name="(auth models)", file_name="notes_log.log")


def registration(request):
    """registering user details to the database, method must be POST

    Args:
        request : accepting the request, and load the body with user details in a postman

    Returns:
        returning json response with success message
    """
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            user_details = User.objects.create_user(username=data.get("user_name"), password=data.get("pass_word"), email=data.get(
                "email"))
            lg.debug(f" User {user_details.username} registered successfully")
            return JsonResponse({"message": "registred successfully", "data": model_to_dict(user_details)})
        else:
            lg.info("Invalid HTTP method")
            return JsonResponse({"message": "Invalid HTTP method"}, status=500)

    except Exception as e:
        lg.error(e)
        return JsonResponse({"message": str(e)}, status=400)


def login(request):
    """login to the user app, method must be POST

    Args:
        request : accepting the request load the body with user name and pass word

    Returns:
        returning json response with success message
    """
    try:
        if request.method == "POST":

            data = json.loads(request.body)
            login_details = authenticate(username=data.get(
                "user_name"), password=data.get("pass_word"))
            if login_details is not None:
                lg.debug(
                    f"User {login_details.username} logged in successfully")
                return JsonResponse({"message": f"{login_details.username} logged in successfully"})
            else:
                return JsonResponse({"message": "Invalid Credentials"}, status=400)
        else:
            return JsonResponse({"message": "Invalid HTTP method"}, status=500)

    except Exception as e:
        lg.error(e)
        return JsonResponse({"message": str(e)}, status=400)
