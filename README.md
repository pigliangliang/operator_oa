# operator_oa

运维工单系统（简单流程）

1、基于Django2.1+python3.6实现，前端只是简单的展示效果，暂无样式。

2、目前实现功能：

  1）正常的审批流转

  2）审批退回操作：直接退回到发起人，退回去到当前审批流程的上一级

  3）页面审批记录，用户流程，待审批，已审批流程等的展示

  4）使用Admin后台实现自定义流程，审批过程，审批人等

3、实现思路：

   定义数据库表

          工作流表单 <- 工作流审批流 <- 审批步骤1-审批人
          
                                       审批步骤2-审批人
                                       
                                        ......
           审批记录表 每次审批步骤都会记录到表中 ，那么对于一个流程来说，在没有退回的过程中，有多少个步骤那么就有多少条记录。
                    
                    记录审批的每一步骤，表中有两个核心字段，status 和 current ，表中主要字段如下
                    
                    currentuser 当前审批人
                    
                    historyuser 历史审批人
                    
                    status 代表当前的审批人
                    
                    current 代表当前的审批步骤
                    
                    rejectflag 表征流程是否被退回，0/1
                    
                    流程正常流转的过程中，status 和 current 每次执行+1 操作，对于上一个审批人的审批记录更新他的current字段值+1
                    
                    这样就保证在获取当前审批人的时候通过 status==current 判单流程走到了哪一个人。
                    
                    这里重点是 每次流程流转必须更新current字段值，表示流程走到了那一步。否则通过上述等式判断当前审批人时候之前审批过的
                    
                    审批人在查看待审批订单的时候仍然能看到审批过的流程。
                                        
每个审批流程绑定多个审批步骤，在审批的过程中，首先每次获取到该流程的所有的审批人，通过status值判断当前审批人。
                    
                    对于流程后推到发起人：
                    
                    新增记录直接将status重置为0，当再次修改重新提交后，则status +1 流程从第一个审批人开始。current==status ，同时rejectflay=1，表示流程驳回，之前审批记录中必须更新current字段值。道理上述。
                    
                    推到上一个审批人的流程：新增记录status= status-1，current=status-1，rejectflag=1。之前审批记录中必须更新current字段值。道理上述。
                    
                    
                                   
