from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from points.views import AwardView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", include("health_check.urls")),
    path("api/award/<uuid:customer_id>/", AwardView.as_view()),
]

urlpatterns += staticfiles_urlpatterns()
