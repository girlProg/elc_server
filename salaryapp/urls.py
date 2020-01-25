from rest_framework import routers
from . import api_views
from django.conf.urls import  url
from esteemServer import settings
from django.conf.urls.static import static


router = routers.DefaultRouter()
router.register('staff', api_views.StaffViewSet, 'staff')
router.register('payslip', api_views.PaySlipViewSet, 'basic')
router.register('pfas', api_views.PensionCollectorViewSet, 'pfas')
router.register('bank', api_views.BankViewSet, 'bank')
router.register('bankaccount', api_views.BankAccountViewSet, 'bankaccount')


urlpatterns = router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
