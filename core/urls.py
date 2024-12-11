"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.home.urls')),
    path('category/', include('app.categories.urls')),
    path('events/', include('app.events.urls')),
    path('marks/', include('app.marks.urls')),
    path('users/', include('app.users.urls')),
    path('wishes/', include('app.wishes.urls')),
    path('tickets/', include('app.tickets.urls')),
    path('search/', include('app.search.urls')),
    path('contact/', include('app.contact.urls')),
]
if settings.DEBUG:  # Only include in debug mode
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
