from rest_framework import serializers
from .models import Notes


class NotesSerializers(serializers.ModelSerializer):
    """Serialisation is conversion of user readable data into computer understandable language 
    Args:
        Serializers is a module
        A `ModelSerializer` is a class is just a regular `Serializer`, except that:
    * A set of default fields are automatically populated.
    * A set of default validators are automatically populated.
    * Default `.create()` and `.update()` implementations are provided.
    """

    class Meta:
        model = Notes
        fields = ['id', 'title', 'description', 'user']
        read_only_fields = ["id"]
