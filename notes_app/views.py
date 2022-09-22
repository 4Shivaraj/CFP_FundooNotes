from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Notes
from .serializers import NotesSerializers
from notes_log import get_logger
from users_app.jwt_service import JwtService

lg = get_logger(name="(CRUD Operation for Note)",
                file_name="notes_log.log")

"""
Instead of writing the separate function we are using decorator
decoraters allows to preprocess the function and perform some sort of operation, before the function is executed,
we are passing the function whatever we written in decorater as a parameter, inside that wrapper function, with
this we are accessing to the parameter of the functon below the decorater(child function),in this case it is 
(self and request), when request comes it will hit the decorator first, inside decorator whatever preposseing
required that will happens and finally it will call the fuction
"""


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


class NoteAV(APIView):
    """
    inheriting from APIView class this class allows you to access below methods, overiding post method
    """
    @verify_token
    def post(self, request):
        """
        Args:
            request: accepting the note details from client server or postman
        Returns:
            response with success message
        """
        try:
            serializer = NotesSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            lg.info(serializer.data)
            lg.debug({"message": "Note created successfully"})
            return Response({"message": "Note created successfully", "data": serializer.data},
                            status=status.HTTP_201_CREATED)  # serializer.data is used for de-serializer
        except Exception as e:
            print(e)
            lg.error(e)
            return Response({"message": str(e)}, status=400)

    @verify_token
    def get(self, request):
        """
        Args:
            request: accepting the user id from client server or postman
        Returns:
            response with success message
        """
        try:
            notes = Notes.objects.filter(user_id=request.data.get("user"))
            serializer = NotesSerializers(notes, many=True)
            lg.info(serializer.data)
            lg.debug({"message": "Note retrieved successfully"})
            return Response({"message": "Note retrieved successfully", "data": serializer.data},
                            status=status.HTTP_200_OK)  # serializer.data is used for de-serializer
        except Exception as e:
            print(e)
            lg.error(e)
            return Response({"message": str(e)}, status=400)

    @verify_token
    def put(self, request):
        """
        Args:
            request: accepting the note details from client server or postman
        Returns:
            response with success message
        """
        try:
            notes_obj = Notes.objects.get(id=request.data.get("id"))
            serializer = NotesSerializers(notes_obj, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            lg.info(serializer.data)
            lg.debug({"message": "Note updated successfully"})
            return Response({"message": "Note updated successfully", "data": serializer.data},
                            status=status.HTTP_202_ACCEPTED)  # serializer.data is used for de-serializer
        except Exception as e:
            print(e)
            lg.error(e)
            return Response({"message": str(e)}, status=400)

    @verify_token
    def delete(self, request):
        """
        Args:
            request: accepting the note id from client server or postman
        Returns:
            response with success message
        """
        try:
            notes_obj = Notes.objects.get(id=request.data.get("id"))
            notes_obj.delete()
            lg.debug({"message": "Note deleted successfully"})
            return Response({"message": "Note deleted successfully", "data": {" "}},
                            status=status.HTTP_204_NO_CONTENT)  # serializer.data is used for de-serializer
        except Exception as e:
            print(e)
            lg.error(e)
            return Response({"message": str(e)}, status=400)
