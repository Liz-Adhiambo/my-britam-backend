from django.urls import path, include
from .views import *


urlpatterns = [

    # Time TrackerLog
    path('login', user_login_view, name='user_login_view'),
    path('signup', User_signup_view, name='User_signup_view'),
    path('profiles/add/<int:id>',create_profile),
    path('profiles/<int:pk>/',profile_detail),
    path('policy/type/create',create_policy_type, name='policy_create'),
    path('policy/type/get/<int:pk>',get_policy_type, name='get_policy_type'),
    path('policy/type/update/<int:pk>',update_policy_type, name='update_policy_type'),
    path('policy/type/delete/<int:pk>',delete_policy_type, name='delete_policy_type'),
    path('policy/create',create_policy, name='create_policy'),
    path('policy/get/<int:pk>',get_policy, name='get_policy'),
    path('policy/update/<int:pk>',update_policy, name='update_policy'),
    path('policy/delete/<int:pk>',delete_policy, name='delete_policy'),
    path('policy/get_all/',get_all_policy, name='get_all_policy'),
    path('policy/buy',user_policy_create_view, name='user_policy_create_view'),
    path('policy/user/list/<int:pk>',get_users_policy, name='get_users_policy'),
    path('signup/<str:code>',User_signup_referral_view, name='User_signup_referral_view'),
    path('user/loyalty/points/<int:pk>',referral_points, name='referral_points'),
    path('user/details/<int:pk>',get_user_details, name='get_user_details'),
    

]