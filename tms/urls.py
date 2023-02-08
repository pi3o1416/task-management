"""tms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('department/', include('department.urls')),
    path('goals/', include('goal.urls')),
    path('authorization/', include('permission_handler.urls')),
    path('tasks/', include('task.urls')),
    path('team/', include('team.urls')),
    path('project/', include('project.urls')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path("schema/redoc/", SpectacularRedocView.as_view( url_name="schema"), name="redoc",),
    path("schema/swagger/", SpectacularSwaggerView.as_view( url_name="schema"), name="swagger",),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




