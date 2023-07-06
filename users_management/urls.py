from django.urls import path

from users_management.views import UserRegistration, UserLogin, UserLogOut, \
                                    GetUserInfo


urlpatterns = [
    path('register/', UserRegistration.as_view(), name='user_registration'),
    path('login/', UserLogin.as_view(), name='user_login'),
    path('logout/', UserLogOut.as_view(), name='user_logout'),
    path('get-info/', GetUserInfo.as_view(), name='get_user_info'),
]


app_name = 'user_management'


