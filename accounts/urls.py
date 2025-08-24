from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, CustomTokenObtainPairView, login_page, register_page

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),  # use custom
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register-page/", register_page, name="register_page"),
    path("login-page/", login_page, name="login_page"),
]
