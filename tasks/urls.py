from django.urls import path
from . import views
# Auth
urlpatterns = [
    path('signup/', views.signup_user, name='signupuser'),
    path('logout/', views.logout_user, name='logoutuser'),
    path('login/', views.login_user, name='loginuser'),
    # Tasks
    path('', views.home, name='home'),
    path('current/', views.current_tasks, name='currenttasks'),
    path('create/', views.create_task, name='createtask'),
    path('tasks/<int:tasks_pk>/', views.view_task, name='viewtask'),
    path('tasks/<int:tasks_pk>/complete', views.complete_task, name='completetask'),
    path('completed/', views.completed_tasks, name='completedtasks'),
    path('tasks/<int:tasks_pk>/delete', views.delete_task, name='deletetask'),
    path('tasks/inbox.html', views.inbox, name='inbox'),
    path('message/<str:pk>', views.veiw_message, name='message'),
    path('create-message/<str:pk>', views.create_message, name='create-message'),
    ]
