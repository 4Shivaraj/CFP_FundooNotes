from rest_framework.reverse import reverse
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserSerializer
from notes_log import get_logger
from .jwt_service import JwtService
from .models import User
from fundoo_notes import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

lg = get_logger(name="(Class Based view with serialisation)",
                file_name="notes_log.log")


class UserRegistration(APIView):
    """
    inheriting from APIView class this class allows you to access below methods, overiding post method
    """
    @swagger_auto_schema(request_body=UserSerializer, responses={201: 'CREATED', 400: 'BAD REQUEST'})
    def post(self, request):
        """
        Args:
            request: accepting the user details from client server or postman 
            encoding username and user id with Jwt, generating token, and sending this token to the mail
        Returns:
            response with success message
        """
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()  # serializing the data after validation
            # jwt_encode = JwtService()
            token = JwtService().encode({"user_id": serializer.data.get(
                "id"), "username": serializer.data.get("username")})
            send_mail(
                subject='Json Web Token For User Registration',
                message=settings.BASE_URL +
                reverse('verify_token', kwargs={"token": token}),
                from_email=None,
                recipient_list=[serializer.data.get('email')],
                fail_silently=False,
            )

            return Response({"message": "Registered successfully", "data": serializer.data},
                            status=status.HTTP_201_CREATED)  # serializer.data is used for de-serializer

        except Exception as e:
            lg.error(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    """
    inheriting from APIView class
    """
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING)
        }),
        responses={202: 'ACCEPTED', 400: 'BAD REQUEST'})
    def post(self, request):
        """
        Args:
            request: accepting the user details from client server or postman
        Returns:
            response with success message
        """
        try:
            user = authenticate(**request.data)
            if not user:
                raise Exception("User is Invalid")
            if not user.is_verified:
                raise Exception("User Not Verified")
            # user.token we are generating directly in User model itself
            return Response({"message": f"{user.username} logged in successfully", "data": {"token": user.token}},
                            status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            lg.error(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class VerifyToken(APIView):
    def get(self, request, token):
        """
        request: sending request from the browsable api  
        after generating the token from registraion process, this function will decode with username and return
        with success message
        """
        try:
            decoded_data = JwtService().decode(token)
            if "username" not in decoded_data:
                raise Exception("Invalid Token")
            user = User.objects.get(username=decoded_data.get("username"))
            user.is_verified = True
            user.save()
            return Response({"message": "User verified"})
        except Exception as e:
            lg.error
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
