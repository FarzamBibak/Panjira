from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from work.models import ToDo, Comment, TaskPause
from datetime import datetime
from django.contrib import messages


def drop(request, *args, **kwargs):
    id_api = request.GET['id']
    print(id_api)
    db = ToDo.objects.get(id=id_api)
    position_db = db.stage
    position_api = request.GET['position']
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
            return HttpResponse('None')
        return HttpResponse(position_db)
    else:
        return HttpResponse('None')


def open_comments(request, *args, **kwargs):
    todo_response = []
    todo_request_id = request.GET['id']
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


def comment(request, *args, **kwargs):
    author = request.user.username
    comment_text = request.GET['text']
    todo_request_id = request.GET['id']
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


def pause_task_activity(request, *args, **kwargs):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        id_api = request.GET['id']
        time_now = datetime.now()
        db_Todo = ToDo.objects.get(id=int(id_api))
        task_pause_db = TaskPause.objects.create(task=db_Todo, start_time=time_now)
        task_pause_db.save()
        return HttpResponse('Pause')


def continue_task_activity(request, *args, **kwargs):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        id_api = request.GET['id']
        db_Todo = ToDo.objects.get(id=int(id_api))
        task_pause_db = TaskPause.objects.filter(task=db_Todo).last()
        if task_pause_db:
            task_pause_db.end_time = datetime.now()
            task_pause_db.save()
        return HttpResponse('Play')


def task_pause_check(request, *args, **kwargs):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        id_api = request.GET['id']
        task_pause = TaskPause.objects.filter(task_id=id_api).last()
        if task_pause:
            if not task_pause.end_time and task_pause.start_time:
                return HttpResponse('Play')
        return HttpResponse('None')


def usefulness_calculate(request, *args, **kwargs):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        wrong_times = []
        wrong_times_pause = []
        get_condition = request.GET.get('task', None)
        if get_condition:
            task = request.GET['task']
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
