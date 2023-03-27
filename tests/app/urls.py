import wagtail.admin.urls
import wagtail.urls
from django.urls import path, include

urlpatterns = [
    path('admin/', include(wagtail.admin.urls)),
    path('', include(wagtail.urls)),
]
