from rest_framework import serializers
from platform_main.models import User, Campaign


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)
    balance = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'balance', 'name']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=100,
        style={'placeholder': 'Email', 'autofocus': True},
        required=True
    )
    password = serializers.CharField(
        max_length=100,
        style={'input_type': 'password', 'placeholder': 'Password'},
        required=True
    )


class CreateCampaignSerializer(serializers.ModelSerializer):
    start_after_moderation = serializers.BooleanField(default=False)

    class Meta:
        model = Campaign
        fields = [
            "name",
            "source",
            "type",
            "format",
            "link",
            "platform",
            "os",
            "geo",
            "price",
            "daily_budget",
            "start_after_moderation"
        ]


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = "__all__"
