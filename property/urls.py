from django.urls import path
from . import views
from .views import *

app_name = 'property'

urlpatterns = [
    path('create/', views.create_property_draft, name='create_property_draft'),
    path('step1/<int:pk>/', views.property_step1, name='property_step1'),
    path('step2/<int:pk>/', views.property_step2, name='property_step2'),
    path('step3/<int:pk>/', views.property_step3, name='property_step3'),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
    path('ajax/load-districts/', views.load_districts, name='ajax_load_districts'),
    path('list/',views.property_list,name='property_list'),
    path('detail/<int:pk>/', views.property_detail, name='property_detail'),
    path('agent_property/',views.agent_property,name='agent_property'),
    path('edit_property/<int:pk>/',views.edit_property,name='edit_property'),
    path('search/',views.property_search,name='property_search')


]
