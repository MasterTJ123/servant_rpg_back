from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    # Root
    path('', RedirectView.as_view(url='api/', permanent=True)),
    # Other routes
    *i18n_patterns(
        # Admin
        path('admin/', admin.site.urls),
        # API
        path('api/', include([
            # Rest
            path('rest/', include('rest_framework.urls')),
            # Apps
            path('', include("apps.account.urls")),
        ])),
    ),
]