from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),   #/accounts/login → settings.LOGIN_URL
    path('logout/',views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('edit/', views.profile_edit, name='profile_edit'),
]
