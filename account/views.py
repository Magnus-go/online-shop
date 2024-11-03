from rest_framework.views import APIView
from .seriaizers import UserRegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()


class UserRegisterView(APIView):

    def post(self, reqeust):
        ser_data = UserRegisterSerializer(data=reqeust.POST)
        if ser_data.is_valid():
            User.objects.create_user(
                fullname=ser_data.validated_data['fullname'],
                email=ser_data.validated_data['email'],
                phone_number=ser_data.validated_data['phone_number'],
                password=ser_data.validated_data['password'],
            )
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

