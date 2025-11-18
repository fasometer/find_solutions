from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm, MessageForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .utils import search_task, paginate_projects, search_messages, paginate_messages
from django.contrib import messages


# Create your views here.

def home(request):
    return render(request, 'tasks/home.html', {'title': "Главная страница"})


def signup_user(request):
    if request.method == "GET":
        return render(request, "tasks/signupuser.html", {'form': UserCreationForm(), 'title': "Регистрация"})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()  # сохраням пользователя
                login(request, user)
                return redirect('currenttasks')
            except IntegrityError:
                messages.error(request,'Такое имя уже есть. Задайте другое!')
                return render(request, 'tasks/signupuser.html',
                              {'form': UserCreationForm()})
        else:
            messages.error(request, 'Пароли не совпадают')
            return render(request, 'tasks/signupuser.html',
                          {'form': UserCreationForm()})


def login_user(request):
    if request.method == "GET":
        return render(request, 'tasks/loginuser.html', {'form': AuthenticationForm(), 'title': "Вход"})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            messages.error(request, 'Неверные данные для входа')
            return render(request, 'tasks/loginuser.html',
                          {'form': AuthenticationForm()})
        else:
            login(request, user)
            return redirect('currenttasks')


@login_required
def logout_user(request):
    if request.method == "POST":
        logout(request)
        messages.info(request,'Пользователь вышел')
        return redirect('home')


@login_required
def current_tasks(request):
    tasks = Task.objects.filter(user=request.user, data_complete__isnull=True)
    title = "Актуальные задачи"
    context = {
        'tasks': tasks,
        'title': title,
    }
    return render(request, 'tasks/currenttasks.html', context)


def create_task(request):
    title = "Создать задачу"
    if request.method == "GET":
        return render(request, 'tasks/createtask.html', {'form': TaskForm(), 'title': title})
    else:
        try:
            form = TaskForm(request.POST, request.FILES)
            new_task = form.save(commit=False)
            # new_task.user = request.user
            new_task.decision = ''
            new_task.save()
            return redirect('currenttasks')
        except ValueError:
            return render(request, 'tasks/createtask.html',
                          {'form': TaskForm(), 'error': 'Переданы неверные данные', 'title': title})


@login_required
def view_task(request, tasks_pk):
    task = get_object_or_404(Task, pk=tasks_pk)
    title = "Задача"
    if request.method == "GET":
        form = TaskForm(instance=task)
        contex = {
            'task': task,
            'form': form,
            'title': title,
        }
        return render(request, 'tasks/viewtask.html', contex)
    else:
        try:
            form = TaskForm(request.POST, request.FILES, instance=task)
            form.save()
            return redirect('currenttasks')
        except ValueError:
            return render(request, 'tasks/viewtask.html',
                          {'task': task, 'form': form, 'error': "Неверные данные"})


@login_required
def complete_task(request, tasks_pk):
    task = get_object_or_404(Task, pk=tasks_pk, user=request.user)
    if request.method == "POST":
        task.data_complete = timezone.now()
        task.save()
        return redirect('completedtasks')


def completed_tasks(request):
    search_query, ts = search_task(request)
    custom_range, ts = paginate_projects(request, ts, 3)
    title = "Завершенные задачи"

    contex = {
        'tasks': ts,
        'search_query': search_query,
        'custom_range': custom_range,
        'title': title,
    }
    return render(request, 'tasks/completedtasks.html', contex)


@login_required
def delete_task(request, tasks_pk):
    task = get_object_or_404(Task, pk=tasks_pk, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect('currenttasks')


@login_required(login_url='login')
def inbox(request):
    search_query, ms = search_messages(request)
    unread_count = ms.filter(is_read=False).count()
    custom_range, ms = paginate_messages(request, ms, 3)
    message_request = ms
    users = User.objects.all()
    title = "Все сообщения"
    context = {
        # 'message_request': message_request,
        'message_request': ms,
        'unread_count': unread_count,
        'search_query': search_query,
        'custom_range': custom_range,
        'users': users,
        'title': title,
    }
    return render(request, 'tasks/inbox.html', context)


@login_required(login_url='login')
def veiw_message(request, pk):
    profile = request.user
    message = profile.messages.get(id=pk)
    title = "Сообщение"
    if message.is_read is False:
        message.is_read = True
        message.save()
    context = {
        'message': message,
        'title': title,
    }
    return render(request, 'tasks/message.html', context)


def create_message(request, pk):
    recipient = User.objects.get(username=pk)
    form = MessageForm()
    sender = request.user
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            message.name = sender
            # message.email = sender.email
            message.save()
            messages.success(request, "Сообщение отправлено")
            return redirect('inbox')
    context = {
        'recipient': recipient,
        'form': form,
    }
    return render(request, 'tasks/message_form.html', context)
