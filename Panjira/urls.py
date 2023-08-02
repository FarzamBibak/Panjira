"""
URL configuration for Panjira project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from work import views
from account import views as acc
from work import views as work

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='login/')),
    path('login/', acc.login_logic),
    path('admin_dashboard/', acc.admin_dashboard),
    path('user_dashboard/', acc.user_dashboard),
    path('logout/', acc.user_logout),
    path('drop_management/', work.drop),
    path('add_comment/', work.comment),
    path('open_comments/', work.open_comments),
    path('pause_activity/', acc.pause_activity),
    path('continue_activity/', acc.continue_activity),
    path('pause_task_activity/', work.pause_task_activity),
    path('continue_task_activity/', work.continue_task_activity),
    path('task_pause_check/', work.task_pause_check),
    path('usefulness/', work.usefulness_calculate)
]
