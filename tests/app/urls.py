import wagtail.admin.urls
import wagtail.core.urls
from django.urls import path, include

urlpatterns = [
    path('admin/', include(wagtail.admin.urls)),
    path('', include(wagtail.core.urls)),
]
