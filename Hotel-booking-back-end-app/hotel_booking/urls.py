from django.urls import path
from apps.users.views import LoginAPIView,RegisterView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # user_apps
    path('api/users/register/', RegisterView.as_view(), name='register'),
    path("api/users/login/", LoginAPIView.as_view(), name="token_obtain_custom"),

]
