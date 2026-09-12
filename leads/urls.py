from django.urls import path
from. import views
from leads.views import *

app_name ='leads'

urlpatterns = [
    path("requests/", Costomer_request.as_view(), name='request-list'),
    path('requests/<int:pk>/', CuostomerDetailView.as_view(), name='customer-detail'),
    path("agent-panel/",AgentDashboardView.as_view(),name='agent-panel'),
    path('customers/',CustomerManageView.as_view(),name='customer_manage'),
    path('create-request',CreateCustomerRequestView.as_view(),name="create-request"),
    path('requests/<int:pk>/change-status/<str:status_action>/', views.change_request_status,
         name='change-request-status'),
    path('agent_task_form/',Todo_list_form.as_view(),name="todo_list_form"),
    path('agent_task_list/',Todo_List.as_view(),name='agent_task_list'),
    path('agent_tasks_edit/<int:pk>/',UpdateAgentTaskView.as_view(),name='update_agent_task'),
    path('agent_tasks_complete/<int:pk>/',AgentTaskComplete.as_view(),name='agent_task_complete'),

]