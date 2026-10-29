from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import register
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    path(
        'accounts/login/',
        auth_views.LoginView.as_view(
            template_name='accounts/login.html'
        ),
        name='login'
    ),

    path(
        'accounts/register/',
        register,
        name='register'
    ),

    path('', include('attendance.urls')),
    path('students/', include('students.urls')),
    path('attendance/', include('attendance.urls')),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )