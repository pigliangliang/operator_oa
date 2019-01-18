from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse,JsonResponse
# Create your views here.
from .forms import  ITApliyForms

from django.views.generic import View
from .models import CaseType,AuditProcess,AuditRecodr,UserCase
from django.utils.decorators import method_decorator

from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.views.generic import DetailView





class Homepage(View):
    """

    用户登陆后的流程主页面

    """


    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,*args,**kwargs)


    def get(self,request):
        #可申请流程
        casetype = CaseType.objects.all()

        #我创建的流程
        mycase = UserCase.objects.filter(username=request.user.username)

        #待审批流程
        auditcase = AuditRecodr.objects.filter(currentaudituser=request.user.username)

        case={}
        for au in auditcase:
            print(au.caseid)
            if au.status==au.current:
                case[au.caseid]=UserCase.objects.filter(caseid=au.caseid).first()
        # for k,v  in case.items():
        #     print(v.rejectflag)

        print(case)

        #历史审批流程
        historycase = AuditRecodr.objects.filter(historaudituser=request.user.username)
        historycases ={}
        for hc in historycase:
            historycases[hc.caseid]=UserCase.objects.filter(caseid=hc.caseid).first()

        print(historycases)

        #审批驳回的流程
        rejectcasts ={}
        rejectcast = AuditRecodr.objects.filter(currentaudituser=request.user.username)

        for rt in rejectcast:
            if rt.status==0:
                rejectcasts[rt.caseid]=UserCase.objects.filter(caseid=rt.caseid).first()

        return render(request,'gongdanhome.html',locals())


"""


# class ApliyView(View):
# 
#     @method_decorator(login_required)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)
# 
# 
#     def get(self,request,id):
#         itf = ITApliyForms()
#         return render(request,'apliyit.html',locals())
# 
# 
#     def post(self,request,id):
# 
#         itf = ITApliyForms(request.POST)
#         if itf.is_valid():
#             print(itf.cleaned_data)
# 
#             ap = AuditProcess.objects.filter(workflow_id=id)
#             print(ap.values('audituser'))
# 
#             auditusername =[]
#             for a in ap:
# 
#                 print(a.audituser)
#                 auditusername.append(a.audituser)
#             status=AuditRecodr.objects.filter(caseid=itf.cleaned_data['formid']).order_by('-status').first()
# 
# 
#             if not status:
#                 status = 0
#                 AuditRecodr.objects.create(caseid=itf.cleaned_data["formid"],currentaudituser=auditusername[status],status=status+1,historaudituser="")
#             else:
#                 if status.status == len(auditusername):
#                     return HttpResponse('流程结束')
#                 print(status.status)
#                 status = status.status
#                 AuditRecodr.objects.create(caseid=itf.cleaned_data["formid"], currentaudituser=auditusername[status],
#                                        status=status + 1, historaudituser=auditusername[status-1])
#             result = {'code':200, "msg":"提交成功，下一审批人是{}".format(auditusername[status])}
#             import json
#             return JsonResponse(result)
"""


class ApliyView(View):
    """

    视图是工单创建人创建流程申请进行提交后的处理结果

    """
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
         return super().dispatch(request, *args, **kwargs)


    def get(self,request,id):
         itf = ITApliyForms()
         return render(request,'apliyit.html',locals())


    def post(self,request,id):
        caseid = datetime.now().strftime("%Y%m%d%H%M%S")

        itf = ITApliyForms(request.POST)
        if itf.is_valid():
            print(itf.cleaned_data)
            UserCase.objects.create(caseid=caseid,username=request.user.username,caseinfo=itf.cleaned_data,casename=itf.cleaned_data['casename'])

            ap = AuditProcess.objects.filter(workflow_id=id)
            print(ap.values('audituser'))

            auditusername =[]
            for a in ap:

                print(a.audituser)
                auditusername.append(a.audituser)

            AuditRecodr.objects.create(caseid=caseid,currentaudituser=auditusername[0],historaudituser='',status=1,current=1)


            return redirect(reverse('gongdan:gongdanhong'))


class CaseInfo(DetailView):
    """
    工单详情

    """
    context_object_name = 'caseinfo'
    template_name = 'caseinfo.html'
    model = UserCase

    pk_url_kwarg = 'id'



class AuditView(View):

    """
    进入流程审核页面

    """
    def get(self,request,id):
        usercase = UserCase.objects.get(caseid=id)
        return render(request,'auditpage.html',locals())



    def post(self,request,id):
        #通过审核
        if request.POST.get('pass')=='提交':
            #通过用户caseid 获取到对应的工作流的ID，目的是获取该工作流对应的审批人
            workflow = UserCase.objects.get(caseid=id)
            workflow_id = workflow.workflowid

            #审核人意见
            auditcontents = request.POST.get('audit','同意申请')
            print(auditcontents)

            #获取审批人
            audituser = AuditProcess.objects.filter(workflow_id=workflow_id)
            auditusername = []
            for au in audituser:
               auditusername.append(au.audituser)
            try:
                status = AuditRecodr.objects.filter(caseid=id).order_by('-status').first()
                print(status.status)
                #current代表审批的阶段，和status进行比较判断审批人的审批阶段
                current = status.current
                status = status.status
                if status<len(auditusername):
                    AuditRecodr.objects.filter(caseid=id).update(current=current+1)
                    AuditRecodr.objects.create(caseid=id, currentaudituser=auditusername[status], historaudituser=auditusername[status-1], status=status+1,current=status+1,auditcontents=auditcontents)
                    return redirect(reverse('gongdan:gongdanhong'))
                else:
                    AuditRecodr.objects.filter(caseid=id).update(current=current + 1)
                    AuditRecodr.objects.create(caseid=id, currentaudituser="流程结束",
                                               historaudituser=auditusername[status - 1], status=status + 1,
                                               current=status + 1,auditcontents=auditcontents)
                    return redirect(reverse('gongdan:gongdanhong'))
            except Exception as e:
                return  HttpResponse(e)

        #未通过审核，退回处理
        else:
            #退回到发起人
            #思路是：通过status 和current字段的值进行判定
            #具体的，用户正常提交流程后，status=1，current=1，那么如果流程被退回到发起人，直接设定
            #status=0，current根据正常流程的流程进行增加，current主要目的是记录流程经过了多少次的审批
            #status主要表征流程的当前审批人。

            auditcontents = request.POST.get('audit')
            status = AuditRecodr.objects.filter(caseid=id).order_by('-status').first()
            print(status.status)
            # current代表审批的阶段，和status进行比较判断审批人的审批阶段
            current = status.current
            status = status.status
            if request.POST.get('backtostart')=="驳回到发起人":#审批是退回到流程发起人
                AuditRecodr.objects.filter(caseid=id).update(current=current + 1)
                #获取流程发起人
                createuser = UserCase.objects.get(caseid=id).username

                AuditRecodr.objects.create(caseid=id, currentaudituser=createuser,
                                           historaudituser=request.user.username, status=0,
                                           current=status + 1, auditcontents=auditcontents,rejectflag=1)
                #更新Usercase表的驳回字段为1，表示拒绝
                UserCase.objects.filter(caseid=id).update(rejectflag=1)
                return redirect(reverse('gongdan:gongdanhong'))
            elif request.POST.get('backonestep')=='退回到上一级':
                #流程被退回到当前审批阶段的上一个阶段
                workflow = UserCase.objects.get(caseid=id)
                workflow_id = workflow.workflowid
                # 获取审批人
                audituser = AuditProcess.objects.filter(workflow_id=workflow_id)
                auditusername = []
                for au in audituser:
                    auditusername.append(au.audituser)

                AuditRecodr.objects.filter(caseid=id).update(current=current + 1)
                AuditRecodr.objects.create(caseid=id, currentaudituser=auditusername[status-2],
                                           historaudituser=request.user.username, status=status - 1,
                                           current=status - 1, auditcontents=auditcontents,rejectflag=1)
                # 更新Usercase表的驳回字段为1，表示拒绝
                UserCase.objects.filter(caseid=id).update(rejectflag=1)
                return redirect(reverse('gongdan:gongdanhong'))






