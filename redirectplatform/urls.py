from django.contrib import admin
from django.urls import path, re_path, include


urlpatterns = [
    re_path('', include(('platform_main.urls', 'platform_main'), namespace='platform_main')),
    path('admin/su35', admin.site.urls),
]
