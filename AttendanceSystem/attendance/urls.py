from django.urls import path
from . import views


urlpatterns = [
    path('mark/', views.mark_attendance, name='mark_attendance'),
    path('records/', views.attendance_records, name='attendance_records'),
    path(
        'student/<int:id>/history/',
        views.student_history,
        name='student_history'
    ),
    path('', views.dashboard, name='dashboard'),
]