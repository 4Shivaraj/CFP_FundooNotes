from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserSerializer
from notes_log import get_logger

lg = get_logger(name="(Class Based view with serialisation)",
                file_name="notes_log.log")


class UserRegistration(APIView):
    """
    inheriting from APIView class this class allows you to access below methods, overiding post method
    """

    def post(self, request):
        """
        Args:
            request: accepting the user details from client server or postman
        Returns:
            response with success message
        """
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()  # serializing the data after validation
            return Response({"message": "Registered successfully", "data": serializer.data},
                            status=status.HTTP_201_CREATED)  # serializer.data is used for de-serializer

        except Exception as e:
            lg.error(e)
            return Response({"message": str(e)}, status=400)


class UserLogin(APIView):
    """
    inheriting from APIView class
    """

    def post(self, request):
        """
        Args:
            request: accepting the user details from client server or postman
        Returns:
            response with success message
        """
        try:
            login_details = authenticate(**request.data)
            if login_details is not None:
                lg.debug(
                    f"User {login_details.username} logged in successfully")
                return Response({"message": f"{login_details.username} logged in successfully"},
                                status=status.HTTP_202_ACCEPTED)
            else:
                return Response({"message": "Invalid Credentials"}, status=400)
        except Exception as e:
            lg.error(e)
            return Response({"message": str(e)}, status=400)
