from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from apps.users.serializers.user_serializers import LoginUserSerializer
from apps.users.utils.cookies import set_jwt_cookies


class LoginAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            response = Response(status=status.HTTP_200_OK)
            set_jwt_cookies(response, user)
            return response
        else:
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED)