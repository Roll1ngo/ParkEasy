from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('files/', include("files.urls")),
    path("", include("users.urls")),
    path('admin_panel/', include('admin_panel.urls')),
    path('parkings/', include('parkings.urls')),
    path('neunet/', include('neural_networks.urls')),
    path('car_im/', include('car_image_download.urls')),
    ]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)