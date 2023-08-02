from django.contrib import admin
from django.template.defaulttags import register

from work.models import ToDo, Comment, Gift, Awards, Activity, Pause, TaskPause

admin.site.register(Gift)
admin.site.register(Awards)
admin.site.register(ToDo)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'text', 'todo', 'timestamp']


@admin.register(Pause)
class PauseAdmin(admin.ModelAdmin):
    list_display = ['user', 'start_time', 'end_time']


@admin.register(TaskPause)
class TaskPauseAdmin(admin.ModelAdmin):
    list_display = ['task', 'start_time', 'end_time']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'start_time', 'end_time']
