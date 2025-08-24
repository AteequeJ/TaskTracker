from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
import requests

API_URL = "http://127.0.0.1:8000/api/auth/" 

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(email=response.data["email"])
        
        # auto-issue tokens
        refresh = RefreshToken.for_user(user)
        response.data["tokens"] = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        return Response(response.data, status=status.HTTP_201_CREATED)

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

def register_page(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            response = requests.post(API_URL + "register/", json=data)
            if response.status_code == 201:
                return redirect("login_page")
            else:
                form.add_error(None, response.json())
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def login_page(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            response = requests.post(API_URL + "login/", json=data)
            if response.status_code == 200:
                tokens = response.json()
                request.session["access"] = tokens["access"]
                request.session["refresh"] = tokens["refresh"]
                return redirect("dashboard")  # a protected page
            else:
                form.add_error(None, response.json())
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})

