from django.shortcuts import render

import toons.models as toons

# Create your views here.


def about_it(request):
    context = {
        'categories': toons.Category.objects.all(),
        'no_category_toon_count': toons.Work.objects.filter(category=None).count(),
    }
    return render(
        request,
        'single_pages/about_it.html',
        context
    )

def time_table(request):
    context = {
        'categories': toons.Category.objects.all(),
        'no_category_toon_count': toons.Work.objects.filter(category=None).count(),
    }
    return render(
        request,
        'single_pages/time_table.html',
        context
    )

def landing(request):
    context = {
        'categories': toons.Category.objects.all(),
        'no_category_toon_count': toons.Work.objects.filter(category=None).count(),
    }
    return render(
        request,
        'single_pages/landing.html',
        context
    )