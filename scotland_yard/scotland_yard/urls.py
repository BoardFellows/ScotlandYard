from django.conf.urls import url
from django.contrib import admin
from syard_main.views import home_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home_view)
]
