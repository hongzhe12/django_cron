# cron_management_app/urls.py
from django.urls import path
from .views import index, add, delete, edit, get_description_route,logs,view_log

urlpatterns = [
    path('', index, name='index'),
    path('add/', add, name='add'),
    path('delete/<int:task_id>/', delete, name='delete'),
    path('edit/<int:task_id>/', edit, name='edit'),
    path('logs/', logs, name='logs'),  # 新增日志列表视图
    path('view_log/<str:log_name>/', view_log, name='view_log'),  # 新增查看日志视图
    path('get_description/', get_description_route, name='get_description'),
    
]
