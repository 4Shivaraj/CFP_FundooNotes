from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Notes
from .serializers import NotesSerializers
from notes_log import get_logger

lg = get_logger(name="(CRUD Operation for Note)",
                file_name="notes_log.log")


class NoteAV(APIView):
    """
    inheriting from APIView class this class allows you to access below methods, overiding post method
    """

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
