from django.shortcuts import render
from .models import *

# Create your views here.

def home(request):
    banner = Banner.objects.filter(
        is_active=True
    ).first()
    quick_links=QuickLink.objects.filter(is_active=True)

    context = {
        'banner': banner,
        'quick_links':quick_links
    }

    return render(
        request,
        template_name='home/home.html',
        context=context
    )