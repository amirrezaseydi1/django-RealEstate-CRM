import django_filters
from .models import *
from django import forms

class PropertyFilter(django_filters.FilterSet):
    district = django_filters.ModelChoiceFilter(
        queryset=District.objects.all(),
        empty_label="همه محله‌ها",
        widget=forms.Select(attrs={
            "class": "form-select"
        })
    )

    property_category = django_filters.ModelChoiceFilter(
        field_name="PROPERTY_TYPE",
        queryset=PropertyCategory.objects.all(),
        empty_label="همه دسته‌ها",
        widget=forms.Select(attrs={
            "class": "form-select"
        })
    )

    deal_type = django_filters.ChoiceFilter(
        field_name="deal_type",
        choices=PropertyListing.DealType.choices,
        widget=forms.Select(attrs={
            "class": "form-select"
        })
    )

    class Meta:
        model = PropertyListing
        fields = ["district", "property_category", "deal_type"]