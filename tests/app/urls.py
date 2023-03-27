import wagtail.admin.urls
import wagtail.urls
from django.urls import include, path

urlpatterns = [
    path('admin/', include(wagtail.admin.urls)),
    path('', include(wagtail.urls)),
]
