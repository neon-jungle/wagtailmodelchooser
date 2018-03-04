import wagtail.admin.urls
import wagtail.core.urls
from django.conf.urls import include, url

urlpatterns = [
    url(r'^admin/', include(wagtail.admin.urls)),
    url(r'', include(wagtail.core.urls)),
]
