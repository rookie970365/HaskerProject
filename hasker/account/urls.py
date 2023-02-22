from django.urls import path
from .views import LogIn, LogOut, AccountDetail, SignUp

# app_name = "account"

urlpatterns = [
    path("login/", LogIn.as_view(), name="login"),
    path("logout/", LogOut.as_view(), name="logout"),
    path("detail/", AccountDetail.as_view(), name="detail"),
    path("signup/", SignUp.as_view(), name="signup"),
]
