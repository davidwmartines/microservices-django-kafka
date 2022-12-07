from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from person.views import PersonViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"persons", PersonViewSet, basename="person")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", include("health_check.urls")),
    path("api/", include(router.urls)),
]

urlpatterns += staticfiles_urlpatterns()
