from django.urls import path, include
from .views import *


urlpatterns = [

    # Time TrackerLog
    path('login', user_login_view, name='user_login_view'),
    path('signup', User_signup_view, name='User_signup_view'),
    path('profiles/add/<int:id>',create_profile),
    path('profiles/<int:pk>/',profile_detail),

]