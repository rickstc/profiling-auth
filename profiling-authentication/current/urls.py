from rest_framework import routers
from current import viewsets

app_name = 'current'

router = routers.SimpleRouter()


router.register(r'permissions', viewsets.PermissionViewSet)
router.register(r'roles', viewsets.RoleViewSet)
router.register(r'profiles', viewsets.ProfileViewSet)

urlpatterns = router.urls