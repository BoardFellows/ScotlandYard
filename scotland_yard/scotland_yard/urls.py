from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from syard_api import views

router = DefaultRouter()
router.register('users', views.UserViewSet)
router.register('games', views.GameViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home_view),
    url(r'^board$', views.board_view),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
