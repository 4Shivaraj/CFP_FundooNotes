from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serialisation is conversion of user readable data into computer understandable language 
    Args:
        Serializers is a module
        A `ModelSerializer` is a class is just a regular `Serializer`, except that:
    * A set of default fields are automatically populated.
    * A set of default validators are automatically populated.
    * Default `.create()` and `.update()` implementations are provided.
    """

    def create(self, validated_data):
        """
        User.objects.create_user method is inheriting 
        from User ----> AbstractUser ----> objects=UserManager() ---> create_user
        validated data is data getting after validating from serializer.save() method
        """
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ['id', 'username', 'password',
                  'email', 'phone_number', 'location']
        read_only_fields = ["id"]
        extra_kwargs = {"password": {"write_only": True}}
