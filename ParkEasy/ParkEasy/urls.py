from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('files/', include("files.urls")),
    path("", include("users.urls")),
    path('admin_panel/', include('admin_panel.urls')),
    path('parkings/', include('parkings.urls')),
    path('nns/', include('nns.urls'))
    ]
