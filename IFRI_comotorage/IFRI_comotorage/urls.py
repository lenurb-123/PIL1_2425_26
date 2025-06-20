"""
URL configuration for IFRI_comotorage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from comptes import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    path('logout/', views.logout_view, name='logout'),
    path('accounts/', include('allauth.urls')), #  pour les connexions sociales
    
    path('', include('discussions.urls')),
    path('', include('comptes.urls')),
    path('', include('trajets.urls'))# <== ligne corrigée
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Home view for the application