from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DataModelViewSet, FormDataViewSet, FormLayoutViewSet

router = DefaultRouter()
router.register(r"models", DataModelViewSet, basename="datamodel")
router.register(r"form-data", FormDataViewSet, basename="formdata")
router.register(r"layouts", FormLayoutViewSet, basename="formlayout")

urlpatterns = [
    path("", include(router.urls)),
]