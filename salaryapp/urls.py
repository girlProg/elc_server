from rest_framework import routers
from . import api_views, views
from django.conf.urls import  url, include
from esteemServer import settings
from django.conf.urls.static import static



router = routers.DefaultRouter()
router.register('staff', api_views.StaffViewSet, 'staff',)
router.register('payslip', api_views.PaySlipViewSet, 'basic')
router.register('pfas', api_views.PensionCollectorViewSet, 'pfas')
router.register('bank', api_views.BankViewSet, 'bank')
router.register('bankaccount', api_views.BankAccountViewSet, 'bankaccount')
router.register('schoolbranch', api_views.SchoolBranchViewSet, 'schoolbranch')
router.register('varadjtype', api_views.VariableAdjustmentTypeViewSet, 'varadjtype')
router.register('varadj', api_views.VariableAdjustmentViewSet, 'varadj')
router.register('generatethismonth', api_views.GenerateCurrentMonthPayslipsViewSet, 'thismonth')
router.register('generatenextmonth', api_views.GenerateNextMonthPayslipsViewSet, 'nextmonth')
router.register('adjustallstaff', api_views.AdjustAllStaffViewSet, 'adjustallstaff')


# urlpatterns = router.urls

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^getstaff', views.convert_staff, name='convert_staff'),
    url(r'^lokogomastaff', views.lokogoma_staff, name='lokogoma_staff'),
    url(r'^checkalert', views.ps_email, name='checkalert'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
