from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from .models import CustomUser
from books.models import Book
from .serializers import RegistrationSerializer, ActivationSerializer, LoginSerializer, ChangePasswordSerializer, \
    CustomUserSerializer
from django.contrib.auth import get_user_model
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .permissions import IsActivePermission
from rest_framework.permissions import IsAuthenticated

User = get_user_model()


class RegistrationView(APIView):

    def post(self, request):
        serializer = RegistrationSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Аккаунт успешно создан', status=201)


class ActivationView(APIView):

    def post(self, request):
        serializer = ActivationSerializer(
            data=request.data
        )
        if serializer.is_valid(raise_exception=True):
            serializer.activate()
            return Response(
                'Аккаунт успешно активирован',
                status=200
            )


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [IsActivePermission]

    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response(
            'Вы успешно вышли из своего аккаунта'
        )


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response(
                'Пароль успешно обнавлен', status=200
            )


class CustomUserView(RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


def add_to_wishlist(request, book_id):
    # Get the currently logged-in user or handle user authentication as needed.
    print(request)
    user = request.user

    # Check if the user is authenticated and is a CustomUser.
    if not user.is_authenticated or not isinstance(user, CustomUser):
        return JsonResponse({'message': 'Unauthorized'}, status=401)

    try:
        book_id = int(book_id)
    except ValueError:
        return JsonResponse({'message': 'Invalid book ID'}, status=400)

    user.add_book_to_wishlist(book_id)
    return JsonResponse({'message': 'Book added to wishlist'})


def remove_from_wishlist(request, book_id):
    # Get the currently logged-in user or handle user authentication as needed.
    user = request.user

    # Check if the user is authenticated and is a CustomUser.
    if not user.is_authenticated or not isinstance(user, CustomUser):
        return JsonResponse({'message': 'Unauthorized'}, status=401)

    try:
        book_id = int(book_id)
    except ValueError:
        return JsonResponse({'message': 'Invalid book ID'}, status=400)

    user.remove_book_from_wishlist(book_id)
    return JsonResponse({'message': 'Book removed from wishlist'})


def auth(request):
    return render(request, 'oauth2.html')