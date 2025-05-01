from rest_framework.routers import DefaultRouter
from .views import StaffViewSet, PatientViewSet, AppointmentViewSet, PhoneNumberViewSet, RoleViewSet

router = DefaultRouter()
router.register(r'staff', StaffViewSet)
router.register(r'patients', PatientViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'phone-numbers', PhoneNumberViewSet)
router.register(r'roles', RoleViewSet)

urlpatterns = router.urls
