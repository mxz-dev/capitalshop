from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('mag/', include('mag.urls')),
    path('accounts/', include('accounts.urls')),
    path('summernote/', include('django_summernote.urls'))
]

# static and media url 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)