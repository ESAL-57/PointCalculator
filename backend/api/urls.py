from django.urls import path

from . import views


urlpatterns = [
    path("status/", views.status),
    path("options/", views.options),
    path("calculate/", views.calculate),
    path("calculate-player/", views.calculate_player),
    path("riot/player/", views.riot_player),
    path("crawl/player/", views.crawl_player),
    path("riot-example/", views.riot_example),
]
