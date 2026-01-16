from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index-page"),
    path("dashboard/<str:brand>", views.brand_dashboard, name="brand-dashboard-page"),
    path(
        "campaign/<str:campaign>",
        views.campaign_dashboard,
        name="campaign-dashboard-page",
    ),
]
