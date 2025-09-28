from django.urls import path, include
from .views import (
    home,
    UserViewSet,
    MetaBooksViewSet,
    PhysicalBooksViewSet,
    TransactionsViewSet,
    Transaction_PhysicalBookViewSet
)
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'metabooks', MetaBooksViewSet)
router.register(r'physicalbooks', PhysicalBooksViewSet)
router.register(r'transactions', TransactionsViewSet)
router.register(r'transaction_physicalbook', Transaction_PhysicalBookViewSet)

urlpatterns = [
    path('', home),
    path('api/', include(router.urls)),
]
