from rest_framework import serializers

from apps.users.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    subscriptions = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='subscription-detail'
    )

    class Meta:
        model = User
        fields = ["url", "username", "email", "subscriptions"]
