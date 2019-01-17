from django.urls import path,re_path
from .views import ApliyView,Homepage,CaseInfo,AuditView


app_name = 'gongdan'

urlpatterns =[
    path("",Homepage.as_view(),name='gongdanhong'),
    path('apliy/<int:id>',ApliyView.as_view(),name='apliy'),
    path('caseinfo/<int:id>/',CaseInfo.as_view(),name='caseinfo'),
    path('audit/<int:id>/',AuditView.as_view(),name='audit'),
]