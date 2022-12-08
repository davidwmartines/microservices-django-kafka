from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from planning.views import FinancialRatiosView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", include("health_check.urls")),
    path("api/ratios/<uuid:person_id>/", FinancialRatiosView.as_view()),
]

urlpatterns += staticfiles_urlpatterns()
