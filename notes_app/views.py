from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Notes
from .serializers import NotesSerializers
from notes_log import get_logger
from users_app.jwt_service import JwtService
from notes_app.utils import verify_token
from .utils import RedisNote

lg = get_logger(name="(Redis)",
                file_name="notes_log.log")

"""

"""


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
            # user_id = request.data.get("user")
            serializer = NotesSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # notes = serializer.data
            RedisNote().save_note(
                serializer.data, request.data.get("user"))
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
            # notes = Notes.objects.filter(user_id)
            # serializer = NotesSerializers(notes, many=True)
            get_data = RedisNote().get_note(request.data.get("user"))
            return Response({"message": "Note retrieved successfully", "data": get_data},
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
            notes_obj = Notes.objects.get(id=request.data.get(
                "id"), user=request.data.get("user"))
            serializer = NotesSerializers(notes_obj, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            RedisNote().save_note(serializer.data, request.data.get("user"))
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
            RedisNote().delete_note(request.data.get('user'), request.data.get('id'))
            notes_obj = Notes.objects.filter(id=request.data.get("id"))
            notes_obj.delete()
            return Response({"message": "Note deleted successfully", "data": {}},
                            status=status.HTTP_204_NO_CONTENT)  # serializer.data is used for de-serializer
        except Exception as e:
            print(e)
            lg.error(e)
            return Response({"message": str(e)}, status=400)
