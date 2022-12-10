from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from customer.views import CustomerViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"customers", CustomerViewSet, basename="customer")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", include("health_check.urls")),
    path("api/", include(router.urls)),
]

urlpatterns += staticfiles_urlpatterns()
