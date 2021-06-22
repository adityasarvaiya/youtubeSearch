from rest_framework import routers

from apps.youtube.views import YoutubeViewSet

router = routers.SimpleRouter()
router.register(r'', YoutubeViewSet)


urlpatterns = []

urlpatterns += router.urls
