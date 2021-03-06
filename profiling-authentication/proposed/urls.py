from rest_framework import routers
from proposed import viewsets

app_name = 'proposed'

router = routers.SimpleRouter()


router.register(r'roles', viewsets.RoleViewSet)
router.register(r'profiles', viewsets.ProfileViewSet)

urlpatterns = router.urls