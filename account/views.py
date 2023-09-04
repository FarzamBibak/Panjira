from django.shortcuts import render
from .forms import LoginForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from work.models import Activity, ToDo, Gift, Comment, Pause, TaskPause
from django.http import HttpResponse
from django.contrib import messages


def login_logic(request, *args, **kwargs):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_staff:
                    login(request, user)
                    print('admin logged in :)')
                    print('form is valid')
                    print('view: user: ', username, ' ,pass: ', password)
                    messages.success(request, "خوش اومدی ادمین")
                    return redirect('/admin/')
                else:
                    login(request, user)
                    date = datetime.now()
                    date = datetime(day=date.day, month=date.month, year=date.year)
                    activity_obj = request.user.activity_user.filter(date__gte=date).first()
                    if not activity_obj:
                        start_time = datetime.now()
                        activity_obj = Activity(user=request.user, start_time=start_time)
                        activity_obj.save()
                        print('user logged in!')
                    messages.success(request, "خوش اومدی")
                    return redirect('/user_dashboard/')
            else:
                print('user is not true')
                messages.error(request, "نام کاربری یا رمزتو اشتباه وارد کردی")
        else:
            print('form is not valid')
            messages.error(request, "فرم رو درست پر نکردی")
    return render(request, 'login.html')


def admin_dashboard(request, *args, **kwargs):
    return render(request, 'admin_dashboard.html')


def user_dashboard(request, *args, **kwargs):
    user = request.user
    todo = ToDo.objects.all()
    gift = Gift.objects.all()
    comment = Comment.objects.all()
    pause = Pause.objects.filter(user=user).last()
    context = {
        'todo': todo,
        'gift': gift,
        'comment': comment,
        'pause': pause
    }
    return render(
        request,
        'user_dashboard.html',
        context
    )


def user_logout(request, *args, **kwargs):
    time_now = datetime.now()
    user = request.user
    last_activity = Activity.objects.filter(user=user).last()
    last_activity.end_time = time_now
    last_activity.save()
    last_pause = Pause.objects.filter(user=user).last()
    if last_pause:
        if not last_pause.end_time:
            last_pause.end_time = time_now
            last_pause.save()
    logout(request)
    messages.success(request, "خسته نباشی")
    return redirect('/login/')


def pause_activity(request, *args, **kwargs):
    user = request.user
    time_now = datetime.now()
    pause_db = Pause.objects.create(user=user, start_time=time_now)
    pause_db.save()
    return HttpResponse('Pause')


def continue_activity(request, *args, **kwargs):
    user = request.user
    pause_db = Pause.objects.filter(user=user).last()
    if pause_db:
        pause_db.end_time = datetime.now()
        pause_db.save()
    return HttpResponse('Play')
