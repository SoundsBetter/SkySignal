from rest_framework import serializers

from web.apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
