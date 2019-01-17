from django.db import models
from users.models import MyUser
# Create your models here.

class AuditProcess(models.Model):
    """
    审批过程
    """
    name = models.CharField('流程名称',max_length=100)
    audituser = models.ForeignKey(MyUser,verbose_name='审批用户',on_delete=models.CASCADE)
    auditorder = models.IntegerField('审核顺序',default=1)
    workflow = models.ForeignKey('WorkFlow',verbose_name='所属工作流',on_delete=models.CASCADE)

    class Meta:
        unique_together=('auditorder','workflow')
        verbose_name = "审核流程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name



class WorkFlow(models.Model):
    """
    工作流由许多审批过程构成
    """
    id = models.IntegerField('工作流ID',default=1,primary_key=True)
    title = models.CharField('工作流名称',max_length=32)


    class Meta:
        verbose_name = '工作流'
        verbose_name_plural = verbose_name


    def __str__(self):
        return self.title


class CaseType(models.Model):
    """
    工单对应一个工作流
    """
    title = models.CharField("工单名称",max_length=32)

    auditmodle = models.ForeignKey('WorkFlow',verbose_name='审核流程',on_delete=models.CASCADE)


    class Meta:
        verbose_name = '工单类型'
        verbose_name_plural =verbose_name


    def __str__(self):
        return self.title

class User(models.Model):

    username = models.CharField("姓名",max_length=32)


    class Meta:
       verbose_name='用户'
       verbose_name_plural = verbose_name

    def __str__(self):
        return self.username



class AuditRecodr(models.Model):
    """
    操作记录，工单的审批流转过程
    """
    caseid = models.IntegerField('工单ID')
    currentaudituser = models.CharField('当前审批人',max_length=32)
    historaudituser = models.CharField('历史审批人',max_length=32)
    status = models.IntegerField("审批节点",default=0)
    current = models.IntegerField('当前审批阶段')


    class Meta:
        verbose_name ='审批记录'
        verbose_name_plural = verbose_name



class UserCase(models.Model):
    """
    该表用于存储用户提交的工单信息
    """
    caseid = models.IntegerField('工单ID',primary_key=True)
    casename = models.CharField('工单名称',max_length=100)
    username = models.CharField('创建用户',max_length=100)
    caseinfo = models.TextField('工单内容')
    workflowid = models.IntegerField('所属工作流',default=1)


    def __str__(self):
        return self.casename


