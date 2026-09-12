import re

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib import messages
from django.utils import timezone
from .forms import FollowUpForm
from . models import *
#دسترسی مشاور ها و مدیر به این اپ
from leads.mixins import LeadsAccessMixin




# Create your views here.

# @login_required()
class AgentDashboardView(LoginRequiredMixin,TemplateView,LeadsAccessMixin):
    template_name = 'leads/agent-dashboard.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
class CustomerManageView(View,LeadsAccessMixin):
    template_name = 'leads/customer-manage.html'

    def get(self,request):
        customers = Costomer.objects.all()
        context = {
            'customers':customers
        }
        return render(request,self.template_name,context)
    def post(self,request):
        name = request.POST.get('name')
        phone= request.POST.get('phone')
        description =request.POST.get('description')

        if not phone:
            messages.error(request,"شماره تلفن الزامی است")
        elif not re.fullmatch(r'09\d{9}'):
            messages.error(request, "شماره تلفن باید 11 رقم باشد و با 09 شروع شود")
        if Costomer.objects.filter(phone=phone).exists():
            messages.error(request,"این مشتری با این شماره تلفن قبلا ثبت شده است")
        else:
            try:
                Costomer.objects.create(
                    name=name,
                    phone=phone,
                    description=description
                )
                messages.success(request,"اطلاعات مشتری با موقثیت ثبت شد")
                return redirect('leads:customer_manage')
            except Exception as e:
                messages.error(request,f"خطایی در ذخیره سازی رخ داد {e}")
        customers =Costomer.objects.all()
        return render(request,self.template_name, {'customers': customers})

class CreateCustomerRequestView(View,LeadsAccessMixin):
    template_name = 'leads/create-request.html'

    def get_context(self):
        return {
            "customers": Costomer.objects.all(),
            "categories": PropertyCategory.objects.all(),
            "districts": District.objects.all(),
            "deal_types": CuostomerRequest.DealType.choices,
            "statuses": CuostomerRequest.RequestStatus.choices,
        }

    def get(self, request):
        return render(request, self.template_name, self.get_context())
    def post(self, request):
        try:
            customer=Costomer.objects.get(id=request.POST.get("customer"))
            property_type=PropertyCategory.objects.get(id=request.POST.get("property_type"))

            customer_request = CuostomerRequest.objects.create(
                title=request.POST.get("title"),
                customer=customer,
                dealtype=request.POST.get("dealtype"),
                property_type=property_type,
                # status=request.POST.get("status"),
                min_area= request.POST.get("min_area") or None,
                max_area=request.POST.get("max_area")or None,
                mortgage_price=request.POST.get("mortgage_price")or None,
                rent_price=request.POST.get("rent_price") or None,
                min_price=request.POST.get("min_price") or None,
                max_price=request.POST.get("max_price") or None,
                rooms=request.POST.get("rooms") or None,
                description=request.POST.get("description"),
            )
            district_ids=request.POST.getlist("district")
            customer_request.district.set(district_ids)
            messages.success(request,'درخواست با موفقیت ثبت شد')
            return redirect("leads:request-list")

        except Costomer.DoesNotExist:
            messages.error(request,'کاربری با این مشخصات  معتبر نیست')
        except PropertyCategory.DoesNotExist:
            messages.error(request,'فیلد نوع درخواست  صجیج نمیباشد')
        except Exception as e:
            messages.error(request, f"خطا: {e}")
        context = {
            "customers": Costomer.objects.all(),
            "categories": PropertyCategory.objects.all(),
            "districts": District.objects.all(),
            "deal_types": CuostomerRequest.DealType.choices,
            # "statuses": CuostomerRequest.RequestStatus.choices,
            "requests": CuostomerRequest.objects.all(),
        }

        return render(request, self.template_name, context)

class Costomer_request(ListView,LeadsAccessMixin):
    model = CuostomerRequest
    template_name = "leads/request_list.html"
    context_object_name = "requests"
    paginate_by = 10
    def get_queryset(self):
        return(
            CuostomerRequest.objects.select_related("customer").filter(
                status__in=[
                    CuostomerRequest.RequestStatus.ACTIVE,
                    CuostomerRequest.RequestStatus.IN_PROGRESS
                ]
            ).order_by("-created_at")
        )

class CuostomerDetailView(DetailView,LeadsAccessMixin):
    model = CuostomerRequest
    template_name = "leads/Costomer_detail.html"
    context_object_name = 'customer_request'
    def  dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.profile.is_agent:
            return redirect('home:home')
        return  super().dispatch(request,*args,**kwargs)
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        customer =self.object.customer
        context['customer'] =customer

        context['form'] =FollowUpForm()
        context['followups'] =customer.followups.all()
        context['requests'] = customer.requests.all().order_by('-id')
        context['other_requests'] =customer.requests.exclude(id=self.object.id)
        # if 'form' in kwargs:
        #     context['form'] = kwargs['form']
        return context
    def post(self,request,*args,**kwargs):
        self.object =self.get_object()
        customer =self.object.customer
        form = FollowUpForm(request.POST)
        if form.is_valid():
            followup = form.save(commit=False)
            followup.customer =customer
            if request.user.is_authenticated:
                followup.agent =request.user

                followup.save()
                return redirect(reverse("leads:customer-detail",kwargs={"pk":self.object.pk}))
            return self.render_to_response(self.get_context_data(form=form))

@login_required
def change_request_status(request, pk, status_action,):
    # بررسی دسترسی کاربر (عاملین/آژانس‌ها)
    if not (request.user.profile.is_agent or request.user.profile.is_manager):
        messages.error(request, "شما دسترسی لازم برای تغییر وضعیت این درخواست را ندارید.")
        return redirect('home:home')

    # پیدا کردن درخواست یا بازگرداندن خطای 404
    customer_request = get_object_or_404(CuostomerRequest, pk=pk)

    # بررسی معتبر بودن وضعیت درخواستی
    valid_statuses = dict(CuostomerRequest.RequestStatus.choices).keys()

    if status_action in valid_statuses:
        customer_request.status = status_action
        customer_request.save()
        messages.success(request, f"وضعیت درخواست با موفقیت به '{customer_request.get_status_display()}' تغییر یافت.")
    else:
        messages.error(request, "وضعیت ارسالی نامعتبر است.")

    # بازگرداندن کاربر به صفحه جزئیات همین درخواست
    return redirect('leads:customer-detail', pk=pk)

class Todo_list_form(View,LeadsAccessMixin):
    template_name= 'leads/agenttask_form.html'
    def get_context(self):
        return {
            "customers":Costomer.objects.all(),
            "requests":CuostomerRequest.objects.all(),
            "task_types":AgentTask.TASK_TYPE_CHOICES,
            "priorities":AgentTask.PRIORITY_CHOICES,
            "statuses":AgentTask.STATUS_CHOICES,
            "properties":PropertyListing.objects.filter(status='AVAILABLE')
        }
    def get(self,request):
        return render(request,self.template_name,self.get_context())

    def post(self,request):
        try:
            related_customer =None
            related_request=None
            related_property= None
            if request.POST.get("related_customer"):
                related_customer =Costomer.objects.get(id=request.POST.get('related_customer'))
            if request.POST.get("related_request"):
                related_request =CuostomerRequest.objects.get(id=request.POST.get('related_request'))
            if request.POST.get("related_property"):
                related_property =PropertyListing.objects.get(id=request.POST.get('related_property'))
            sms_reminder_enabled =True if request.POST.get("sms_reminder_enabled")== "on" else False
            completed_at = None
            if request.POST.get('status') =="done":
                completed_at = timezone.now()
            AgentTask.objects.create(
                agent=request.user,
                title=request.POST.get("title"),
                description=request.POST.get("description"),
                task_type=request.POST.get("task_type"),
                priority=request.POST.get("priority"),
                status=request.POST.get("status"),
                due_date=request.POST.get("due_date")or None,
                due_time=request.POST.get("due_time") or None,
                related_customer=related_customer,
                related_request=related_request,
                related_property=related_property,
                is_auto_created=False,
                sms_reminder_enabled=sms_reminder_enabled,
                sms_sent=False,
                sms_sent_as=None,
                completed_at=completed_at,

            )
            messages.success(request,"فعالیت با موفقیت ثبت شد")
            return redirect("leads:agent-panel")


        except Costomer.DoesNotExist:
            messages.error(request,"مشتری انتخاب شده معتبر نیست")
        except CuostomerRequest.DoesNotExist:
            messages.error(request,"درخواست انتخاب شده معتبر نیست")
        except PropertyListing.DoesNotExist:
            messages.error(request,"ملک انتخابی معتبر نیست")
        except Exception as e:
            messages.error(request,f'خطا:{e}')
        return render(request,self.template_name,self.get_context())


class Todo_List(LeadsAccessMixin ,View):
    template_name = 'leads/agentTaskList.html'

    def get_queryset(self, request):
        profile = getattr(request.user, 'profile', None)

        if profile and profile.role in ['admin', 'manager']:
            return AgentTask.objects.all()

        return AgentTask.objects.filter(agent=request.user)

    def get(self, request):
        tasks = self.get_queryset(request).select_related(
            'agent',
            'related_customer',
            'related_request',
            'related_property',
        ).order_by('status', 'due_date', 'due_time', '-created_at')

        context = {
            'tasks': tasks,
            'today': timezone.localdate(),
        }
        return render(request, self.template_name, context)

class AgentTaskComplete(LeadsAccessMixin,View):
    def post(self,request,pk):
        task = get_object_or_404(AgentTask,pk=pk,agent=request.user)
        task.status = 'done'
        task.completed_at =timezone.now()
        task.save(update_fields=['status','completed_at','updated_at'])

        messages.success(request,'فعالیت با موفقست بروزرسانی شد')
        return redirect('leads:agent_task_list')
class UpdateAgentTaskView(LeadsAccessMixin, View):
    template_name = 'leads/agenttask_update.html'

    def get_context(self, task):
        return {
            "task": task,
            "customers": Costomer.objects.all(),
            "requests": CuostomerRequest.objects.all(),
            "task_types": AgentTask.TASK_TYPE_CHOICES,
            "priorities": AgentTask.PRIORITY_CHOICES,
            "statuses": AgentTask.STATUS_CHOICES,
            "properties": PropertyListing.objects.filter(status='AVAILABLE'),
        }

    def get(self, request, pk):
        task = get_object_or_404(AgentTask, pk=pk, agent=request.user)
        return render(request, self.template_name, self.get_context(task))

    def post(self, request, pk):
        task = get_object_or_404(AgentTask, pk=pk, agent=request.user)

        task.title = request.POST.get("title")
        task.description = request.POST.get("description")
        task.task_type = request.POST.get("task_type")
        task.priority = request.POST.get("priority")
        task.status = request.POST.get("status")
        task.due_date = request.POST.get("due_date") or None
        task.due_time = request.POST.get("due_time") or None

        task.related_customer = Costomer.objects.filter(
            id=request.POST.get("related_customer")
        ).first() if request.POST.get("related_customer") else None

        task.related_request = CuostomerRequest.objects.filter(
            id=request.POST.get("related_request")
        ).first() if request.POST.get("related_request") else None

        task.related_property = PropertyListing.objects.filter(
            id=request.POST.get("related_property")
        ).first() if request.POST.get("related_property") else None

        if task.status == "done" and not task.completed_at:
            task.completed_at = timezone.now()

        task.save()
        messages.success(request, "تسک با موفقیت ویرایش شد")
        return redirect("leads:agent_task_list")



