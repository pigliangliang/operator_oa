from django import forms

from .models import AuditProcess,CaseType


class ITApliyForms(forms.Form):
    # formid = forms.IntegerField(label='工单ID' )
    #     # user = forms.CharField(label='用户')
    casename  = forms.CharField(label='主题')
    cpu = forms.CharField(label='CPU')
    memory = forms.CharField(label='内存')
    info = forms.CharField(label='备注')




    class Meta:
        fields = "__all__"