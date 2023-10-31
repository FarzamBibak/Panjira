from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse
from .forms import LoginForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from work.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages


def login_logic(request, *args, **kwargs):
    context = {"form": LoginForm}
    if request.user:
        if request.user.is_authenticated:
            if request.user.is_staff:
                return redirect('admin_dashboard')
            else:
                return redirect('user_dashboard')

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            print('form is valid')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_staff:
                    login(request, user)
                    print('admin logged in :)')
                    messages.success(request, "خوش اومدی " + username)
                    return redirect('admin_dashboard')
                else:
                    login(request, user)
                    print('user logged in!')
                    date = datetime.now()
                    date = datetime(day=date.day, month=date.month, year=date.year)
                    activity_obj = request.user.activity_user.filter(date__gte=date).first()
                    if not activity_obj:
                        start_time = datetime.now()
                        activity_obj = Activity(user=request.user, start_time=start_time)
                        activity_obj.save()
                    messages.success(request, "خوش اومدی " + username)
                    return redirect('user_dashboard')
            else:
                print('user is not true')
                messages.error(request, "نام کاربری یا رمزتو اشتباه وارد کردی")
        else:
            print('form is not valid')
            messages.error(request, "فرم رو درست پر نکردی")
    return render(request, 'login.html', context)


def admin_dashboard(request, *args, **kwargs):
    if not request.user.is_staff:
        messages.warning(request, "نمیتونی داشبورد مدیر و ببینی")
        return redirect("user_dashboard")
    return render(request, 'admin_dashboard.html')


def user_dashboard(request, *args, **kwargs):
    context = {}
    if request.user.is_staff:
        messages.warning(request, "برو تو داشبورد خودت")
        return redirect("admin_dashboard")

    if request.user.is_authenticated:
        todo = ToDo.objects.filter(Q(user=None) | Q(user=request.user))
        gifts = Gift.objects.all()
        # comment = Comment.objects.all()
        pause = Pause.objects.filter(user=request.user).last()
        context.update({
            'todo': todo,
            'gifts': gifts,
            # 'comment': comment,
            'pause': pause
        })
        return render(
            request,
            'user_dashboard.html',
            context
        )
    else:
        messages.error(request, "ورود غیر مجاز لطفا دوباره وارد شوید")
        return redirect("login")


def user_logout(request, *args, **kwargs):
    if not request.user.is_staff:
        time_now = datetime.now()
        last_activity = Activity.objects.filter(user=request.user).last()
        last_activity.end_time = time_now
        last_activity.save()
        last_pause = Pause.objects.filter(user=request.user).last()
        if last_pause:
            if not last_pause.end_time:
                last_pause.end_time = time_now
                last_pause.save()
    messages.success(request, "خسته نباشی " + request.user.username)
    logout(request)
    return redirect("login")
