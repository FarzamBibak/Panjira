from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, Http404
from django.urls import reverse

from work.models import ToDo, Comment, TaskPause, Pause
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User
import random, os
from account.forms import *
from django.shortcuts import redirect
from django.conf import settings


def activity(request, *args, **kwargs):
    status = int(request.POST.get('status'))
    if status == 0:
        time_now = datetime.now()
        pause_db = Pause.objects.create(user=request.user, start_time=time_now)
        pause_db.save()
        return HttpResponse('Pause')
    elif status == 1:
        pause_db = Pause.objects.filter(user=request.user).last()
        if pause_db:
            pause_db.end_time = datetime.now()
            pause_db.save()
        return HttpResponse('Play')


def drop(request, *args, **kwargs):
    id_api = request.POST.get('id')
    db = ToDo.objects.get(id=id_api)
    position_db = db.stage
    position_api = request.POST['position']
    if position_db != position_api:
        if position_db == 'd' and position_api == 'p':
            if not db.user:
                db.user = request.user
            db.stage = position_api
            db.start_time = datetime.now()
            db.save()
        elif position_db == 'p' and position_api == 'c':
            db.stage = position_api
            db.done_time = datetime.now()
            db.save()
        else:
            return HttpResponse('')
        return HttpResponse(position_db)
    else:
        return HttpResponse('')


def open_comments(request, *args, **kwargs):
    todo_response = []
    todo_request_id = request.POST['id']
    author = request.user.username
    todo_selected = Comment.objects.filter(todo__id=todo_request_id)
    for i in range(len(todo_selected)):
        todo_response.append(
            {
                'author': todo_selected[i].author,
                'text': todo_selected[i].text,
                'timestamp': todo_selected[i].timestamp,
                'id': todo_request_id
            }
        )
    return JsonResponse(todo_response, safe=False)


def add_comment(request, *args, **kwargs):
    author = request.user.username
    comment_text = request.POST.get('text')
    todo_request_id = request.POST.get('id')
    print(todo_request_id)
    todo_db = ToDo.objects.get(id=todo_request_id)
    comment_db = Comment(
        author=author,
        text=comment_text,
        todo=todo_db
    )
    comment_db.save()
    com = comment_db.timestamp
    data = {
        'author': author,
        'text': comment_text,
        'time': com
    }
    return JsonResponse(data)


def task_activity(request, *args, **kwargs):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.user:
            if request.user.is_authenticated:
                status = int(request.POST.get('status'))
                if status == 0:
                    id_api = request.POST.get('id')
                    time_now = datetime.now()
                    db_Todo = ToDo.objects.get(id=int(id_api))
                    task_pause_db = TaskPause.objects.create(task=db_Todo, start_time=time_now)
                    task_pause_db.save()
                    return HttpResponse('Pause')
                elif status == 1:
                    id_api = request.POST.get('id')
                    db_Todo = ToDo.objects.get(id=int(id_api))
                    task_pause_db = TaskPause.objects.filter(task=db_Todo).last()
                    if task_pause_db:
                        task_pause_db.end_time = datetime.now()
                        task_pause_db.save()
                    return HttpResponse('Play')


def task_pause_check(request, *args, **kwargs):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        id_api = request.POST.get('id')
        task_pause = TaskPause.objects.filter(task_id=id_api).last()
        if task_pause:
            if not task_pause.end_time and task_pause.start_time:
                return HttpResponse('Play')
        return HttpResponse('None')


def usefulness_calculate(request, *args, **kwargs):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        wrong_times = []
        wrong_times_pause = []
        get_condition = request.POST.get('task', None)
        if get_condition:
            task = request.POST['task']
            current_task = ToDo.objects.filter(title=task).first()
            current_task_pause = TaskPause.objects.filter(task=current_task).all()
            if current_task.done_time > current_task.start_time:
                current_task_time = (current_task.done_time - current_task.start_time).total_seconds()
            elif current_task.done_time > current_task.start_time:
                print("wrong time add in '" + current_task.title + "' todo, end time smaller than start time")
                wrong_times.append(current_task.title)
            current_task_pause_time = 0
            current_task_point = current_task.point

            for index in current_task_pause:
                if index.end_time > index.start_time:
                    current_task_pause_time += (index.end_time - index.start_time).total_seconds()
                elif index.end_time > index.start_time:
                    print("wrong pause time add in '" + current_task.title + "' todo, end time smaller than start time")
                    wrong_times_pause.append(current_task.title)

            usefulness = current_task_point / (current_task_time - current_task_pause_time)

            return JsonResponse({
                'usefulness': usefulness,
                'todo_time': wrong_times,
                'todo_pause_time': wrong_times_pause
            })
        task_time = 0
        task_time_pause = 0
        user = request.user
        todo = ToDo.objects.filter(user=user).all()
        todo_pause = TaskPause.objects.filter(task__user=user).all()
        point = 0

        for index in todo:
            if index.done_time > index.start_time:
                task_time += (index.done_time - index.start_time).total_seconds()
                point += index.point
            elif index.done_time < index.start_time:
                print("wrong time add in '" + index.title + "' todo, end time smaller than start time")
                wrong_times.append(index.title)

        for index in todo_pause:
            if index.end_time > index.start_time:
                task_time_pause += (index.end_time - index.start_time).total_seconds()
            elif index.end_time < index.start_time:
                print("wrong pause time add in '" + index.task.title + "' todo, end time smaller than start time")
                wrong_times_pause.append(index.task.title)

        print(task_time_pause)
        usefulness = point / (task_time - task_time_pause)

        return JsonResponse({
            'usefulness': usefulness,
            'todo_time': wrong_times,
            'todo_pause_time': wrong_times_pause
        })


def gift_lottery(request, *args, **kwargs):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.user:
            if request.user.is_authenticated and request.user.is_staff:
                users = User.objects.all()
                users_pk_list = {}
                for index in users:
                    users_pk_list[index.id] = index.username
                print(users_pk_list)
                return JsonResponse(users_pk_list)


def db_handler(request, *args, **kwargs):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        try:
            if request.POST.get("status") == "backup":
                if os.path.exists(os.path.join(settings.BASE_DIR, "db.sqlite3")):
                    os.system("python.exe manage.py dbbackup")
                    messages.success(request, "بک آپ دیتا بیس گرفته شد")
                    return redirect(reverse("admin_dashboard"))
                else:
                    messages.error(request, "دیتابیسی نداری که ازش بک اپ بگیری")
                    return redirect(reverse("database_handler"))
            elif request.POST.get("status") == "auto_backup":
                if os.path.exists(os.path.join(settings.BASE_DIR, "db.sqlite3")):
                    os.system("python.exe manage.py auto_db_backup")
                    # messages.success(request, "بک آپ دیتا بیس گرفته شد")
                    # return redirect(reverse("admin_dashboard"))\
                    return HttpResponse(True)
                else:
                    messages.error(request, "دیتابیسی نداری که ازش بک اپ بگیری")
                    return redirect(reverse("database_handler"))
            elif request.POST.get("status") == "restore":
                path_db_restore = str(settings.DBBACKUP_STORAGE_OPTIONS['location'])
                count_db_restores = len(os.listdir(path_db_restore))
                if count_db_restores == 0:
                    messages.error(request, "فایل بک آپ دیتا بیس وجود نداره")
                    return redirect(reverse("database_handler"))
                os.system("python.exe manage.py dbrestore")
                os.system("Y")
                messages.success(request, "دیتا بیس برگشت :)")
                return redirect(reverse("login"))
        except:
            messages.error(request, "خطا بوجود اومده، به ادمین بگو چک کنه :)")
            return redirect(reverse("admin_dashboard"))
    return render(request, "db_restore.html")


# def download(request):
#     if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
#         # file_path = os.path.join(settings.MEDIA_ROOT, path)
#         file_path = os.path.join(settings.BASE_DIR, "db_backups/default-DESKTOP-IBOP86Q-2023-11-13-104221.dump")
#         if os.path.exists(file_path):
#             with open(file_path, 'rb') as fh:
#                 response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
#                 response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
#                 return response
