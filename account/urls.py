from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_logic, name="login"),
    path('dashboard/admin/', admin_dashboard, name="admin_dashboard"),
    path('dashboard/user/', user_dashboard, name="user_dashboard"),
    path('logout/', user_logout, name="logout"),
]
