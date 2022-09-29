from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Notes
from .serializers import NotesSerializers
from notes_log import get_logger
from users_app.jwt_service import JwtService
from notes_app.utils import verify_token
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

lg = get_logger(name="(Swagger API)",
                file_name="notes_log.log")


class NoteAV(APIView):
    """
    inheriting from APIView class this class allows you to access below methods, overiding post method
    """
    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                     properties={
                                                         'title': openapi.Schema(type=openapi.TYPE_STRING),
                                                         'description': openapi.Schema(
                                                             type=openapi.TYPE_STRING), },
                                                     required=['title', 'description']),
                         responses={201: 'CREATED', 400: 'BAD REQUEST'},
                         operation_summary='create Notes')
    @ verify_token
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

    @ verify_token
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

    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                     properties={'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                                                 'title': openapi.Schema(type=openapi.TYPE_STRING),
                                                                 'description': openapi.Schema(
                                                                     type=openapi.TYPE_STRING),
                                                                 },
                                                     responses={
                                                         202: 'ACCEPTED', 400: 'BAD REQUEST'},
                                                     required=['id', 'title', 'description']),
                         operation_summary='Update Notes')
    @ verify_token
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

    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                     properties={
                                                         'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                                     },
                                                     required=['id']),
                         responses={204: 'NO CONTENT', 400: 'BAD REQUEST'},
                         operation_summary='delete Notes')
    @ verify_token
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
            return Response({"message": "Note deleted successfully", "data": {}},
                            status=status.HTTP_204_NO_CONTENT)  # serializer.data is used for de-serializer
        except Exception as e:
            print(e)
            lg.error(e)
            return Response({"message": str(e)}, status=400)
