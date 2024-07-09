from rest_framework import routers

from detector import views

router = routers.DefaultRouter()
router.register('', views.ImageParserView, basename='parse_image')

urlpatterns = router.urls
