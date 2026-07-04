from django.urls import path
from accounts.views import UserLoginView, UserLogoutView, RegisterView, UserDetailView

app_name = 'accounts'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('<int:pk>/', UserDetailView.as_view(), name='profile'),
]