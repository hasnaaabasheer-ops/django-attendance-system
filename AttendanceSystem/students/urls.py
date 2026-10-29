from django.urls import path
from . import views


urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('add/', views.student_add, name='student_add'),
    path('<int:id>/edit/', views.student_edit, name='student_edit'),
    path('<int:id>/delete/', views.student_delete, name='student_delete'),
]