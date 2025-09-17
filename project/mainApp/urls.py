from django.urls import path, include
from .views import home, UserViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    path('', home),
    path('api/', include(router.urls)),
]
