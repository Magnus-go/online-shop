from rest_framework.views import APIView
from .serializer import UserListSerializer
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()


class UserListView(APIView):

    def get(self, request):
        user = User.objects.all()
        ser_data = UserListSerializer(user, many=True)
        return Response(ser_data.data)
