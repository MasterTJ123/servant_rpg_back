from django.urls import path, include

urlpatterns = [
    # Apps
    path('servant_rpg_back/', include("apps.servant_rpg_back.urls")),
]
