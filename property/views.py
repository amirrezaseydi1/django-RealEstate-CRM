
from django.http import JsonResponse

from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .filter import PropertyFilter
from django.urls import reverse
from  django.db.models import Q




def load_cities(request):
    province_id = request.GET.get('province_id')
    cities = City.objects.filter(province_id=province_id).values('id', 'name')
    return JsonResponse(list(cities), safe=False)


def load_districts(request):
    city_id = request.GET.get('city_id')
    districts = District.objects.filter(city_id=city_id).values('id', 'name')
    return JsonResponse(list(districts), safe=False)


def add_property_location(request):
    provinces = Province.objects.all()

    if request.method == "POST":

        district_id = request.POST.get("district")

        if district_id:
            listing = PropertyListing.objects.create(
                district_id=district_id,


                title="پیش نویس آگهی",
                owner_name="نامشخص",
                owner_phone="0000000000",
                PROPERTY_TYPE_id=1,
                area=0,

                status=PropertyListing.Status.DRAFT
            )

            return redirect("property_step2", pk=listing.pk)

    context = {
        "provinces": provinces
    }

    return render(request, "property/add_property.html", context)


@login_required(login_url='accounts:login')
def create_property_draft(request):

    if not hasattr(request.user, 'profile') or not request.user.profile.is_agent:
        messages.error(request, 'فقط مشاورین املاک مجاز به ثبت آگهی جدید هستند.')
        return redirect('home')  # یا هر صفحه دیگری که مناسب می‌دانید


    listing = PropertyListing.objects.create(
        agent=request.user,
        status=PropertyListing.Status.DRAFT
    )


    return redirect("property:property_step1", pk=listing.pk)


def property_step1(request, pk):
    listing = get_object_or_404(PropertyListing, pk=pk)
    provinces = Province.objects.all()
    if request.method == "POST":
        district_id = request.POST.get("district")
        listing.district_id = district_id
        listing.save()
        return redirect('property:property_step2', pk=listing.pk)
    context = {
        "listing": listing,
        "provinces": provinces
    }
    return render(request, "property/step1_location.html", context)


def property_step2(request, pk):
    listing = get_object_or_404(PropertyListing, pk=pk)

    if request.method == "POST":
        form = PropertyStep2Form(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('property:property_step3', pk=listing.pk)

    else:

        form = PropertyStep2Form(instance=listing)
    context = {
        "listing": listing,
        'form': form,
    }
    return render(request, 'property/step2_details.html', context)



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  # <-- حتما این خط را اضافه کنید



def property_step3(request, pk):
    listing = get_object_or_404(PropertyListing, pk=pk)

    if request.method == "POST":
        form = PropertyStep3Form(request.POST, request.FILES, instance=listing)
        images = request.FILES.getlist('images')

        if form.is_valid():
            form.save()

            for index, img in enumerate(images):
                is_cover = True if index == 0 else False  # عکس اول کاور می‌شود
                PropertyImage.objects.create(property=listing, image=img, is_cover=is_cover)

            listing.status = PropertyListing.Status.DRAFT
            listing.save()


            messages.success(request, 'آگهی شما با موفقیت ثبت شد و در سایت قرار گرفت.', 'success')

            # Redirect user to home

            return redirect('home:home')

    else:
        form = PropertyStep3Form(instance=listing)

    context = {
        'form': form,
        'listing': listing,
        'deal_type': listing.deal_type
    }
    return render(request, 'property/step3.html', context)


def property_list(request):
    properties = PropertyListing.objects.filter(status=PropertyListing.Status.AVAILABLE).order_by('-created_at')
    property_filter = PropertyFilter(request.GET, queryset=properties)
    paginator = Paginator(property_filter.qs, 6)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    context = {
        'properties': page_obj,
        'filter': property_filter,
    }
    return render(request, 'property/property_list.html', context)


def property_create(request):
    if request.method == 'POST':
        form = PropertyStep3Form


def property_detail(request, pk):
    # If Property available
    listing = get_object_or_404(PropertyListing, pk=pk, status=PropertyListing.Status.AVAILABLE)

    context = {
        'listing': listing
    }
    return render(request, 'property/property_detail.html', context)


@login_required()
def agent_property(request):
    if not request.user.profile.is_agent:
        return redirect('home')
    listing = PropertyListing.objects.filter(agent=request.user).order_by('-created_at')
    return render(request, 'property/agent_properties.html', context={'listing': listing})


def edit_property(request, pk):
    prop = get_object_or_404(PropertyListing, pk=pk, agent=request.user)

    if request.method == 'POST':
        prop.title = request.POST.get('title')
        prop.description = request.POST.get('description')
        prop.district = request.POST.get('district')
        prop.deal_type = request.POST.get('deal_type')
        prop.selling_price = request.POST.get("selling_price") or None
        prop.mortgage_price = request.POST.get("mortgage_price") or None
        prop.rent_price = request.POST.get("rent_price") or None
        prop.area = request.POST.get("area")
        prop.room_count = request.POST.get("room_count")
        # prop.status = request.POST.get("status")

        prop.save()

        images =request.FILES.getlist("images")
        for img in images:
            PropertyImage.objects.create(property=prop,image=img)
        return redirect("property:agent_property")
    return render(request,'property/edit_property.html',{'prop':prop})
def property_search(request):
    query = request.GET.get("q", "").strip()

    properties = PropertyListing.objects.filter(
        status=PropertyListing.Status.AVAILABLE
    )

    if query:
        for word in query.split():
            properties = properties.filter(
                Q(title__icontains=word) |
                Q(district__name__icontains=word)
            )

    filterset = PropertyFilter(request.GET, queryset=properties)
    properties = filterset.qs

    return render(request, "property/property_list.html", {
        "properties": properties,
        "filter": filterset,
        "query": query,
    })

