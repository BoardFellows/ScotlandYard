from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from django.contrib import admin
from rest_framework.authtoken import views
from syard_main.views import home_view
from syard_api import views

router = DefaultRouter()
router.register('users', views.UserViewSet)
router.register('profiles', views.ProfileViewSet)
router.register('games', views.GameViewSet)
router.register('rounds', views.RoundViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home_view),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', views.obtain_auth_token),
]
