from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=200, write_only=True)

    class Meta:
        model = User
        fields = ('fullname', 'email', 'phone_number', 'password', 'password2')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] and data['password2'] and data['password'] != data['password2']:
            raise serializers.ValidationError('passwords most match')
        return data
