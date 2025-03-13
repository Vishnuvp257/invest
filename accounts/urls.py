from django.urls import path
from .views import register, login_user, logout_user, get_user, update_user_type

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('user/', get_user, name='get-user'),
    path('update-type/', update_user_type, name='update-user-type'),  # New API for updating type
]

