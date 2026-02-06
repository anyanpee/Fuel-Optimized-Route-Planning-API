print("[+] config.urls.py loaded")

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('routes/', include('routes.urls')),
   # path('fuel/', include('datalake.urls')),
]