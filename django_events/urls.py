from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^api/v1/', include('events.urls')),
    url(r'^admin/', admin.site.urls),
]
