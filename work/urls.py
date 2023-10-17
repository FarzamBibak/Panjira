from django.urls import path
from .views import *

urlpatterns = [
    path('drop_management/', drop, name="drop_management"),
    path('add_comment/', add_comment, name="add_comment"),
    path('open_comments/', open_comments, name="open_comments"),
    path('activity/', activity, name="activity"),
    path('task_activity/', task_activity, name="task_activity"),
    path('task_pause_check/', task_pause_check, name="task_activity_check"),
    path('usefulness/', usefulness_calculate, name="usefulness"),
    path('lottery/', gift_lottery, name="lottery"),
]
