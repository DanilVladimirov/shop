from django.urls import path
from accounts.views import *


urlpatterns = [
    path('register/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('is_user_exist/', is_user_exist, name='is_user_exist'),
    path('user-page/', user_page, name='user_page')
]
