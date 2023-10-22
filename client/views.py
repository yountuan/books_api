from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import RegistrationSerializer, ActivationSerializer, LoginSerializer
from .models import CustomUser
from django.contrib.auth import login, authenticate
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from .serializers import PasswordResetRequestSerializer, PasswordResetConfirmSerializer



class RegistrationView(APIView):

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()
            user.create_activation_code()
            user.send_activation_code(user.email, user.activation_code)
            return Response({'message': 'Registration successful. Check your email for activation code.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivationView(APIView):
    def post(self, request):
        serializer = ActivationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            activation_code = serializer.validated_data['activation_code']
            try:
                user = CustomUser.objects.get(email=email, activation_code=activation_code)
                user.is_active = True
                user.activation_code = ''
                user.save()
                login(request, user)
                return Response({'message': 'Account activated successfully.'}, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response({'message': 'Invalid activation code or email.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return Response({'detail': 'Authentication successful.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)


class PasswordResetRequestView(GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user_model = get_user_model()
            try:
                self.user = user_model.objects.get(email=email)
                return Response(status=status.HTTP_200_OK)
            except user_model.DoesNotExist:
                return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(PasswordResetRequestView):
    permission_classes = [IsAuthenticated]

    def form_valid(self):
        serializer = PasswordResetConfirmSerializer(data=self.request.data)
        if serializer.is_valid():
            user = self.user
            if user:
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                return Response({'detail': ('Password has been reset successfully.')}, status=status.HTTP_200_OK)
            return Response({'detail': ('Invalid data.')}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

