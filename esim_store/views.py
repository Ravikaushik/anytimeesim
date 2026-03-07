from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Q, Count
from .models import ESIMPlan, Country, PageContent

def home(request):
    """Home page with eSIM plans and filtering"""
    plans = ESIMPlan.objects.filter(is_active=True).select_related()
    
    # Get filter parameters
    country_filter = request.GET.get('country', '')
    price_filter = request.GET.get('price', '')
    search_query = request.GET.get('search', '')
    
    # Apply filters
    if country_filter:
        plans = plans.filter(countries__code=country_filter)
    
    if price_filter:
        if price_filter == 'under_10':
            plans = plans.filter(price__lt=10)
        elif price_filter == '10_20':
            plans = plans.filter(price__gte=10, price__lte=20)
        elif price_filter == '20_50':
            plans = plans.filter(price__gte=20, price__lte=50)
        elif price_filter == 'over_50':
            plans = plans.filter(price__gt=50)
    
    if search_query:
        plans = plans.filter(
            Q(name__icontains=search_query) |
            Q(data_amount__icontains=search_query) |
            Q(countries__name__icontains=search_query)
        ).distinct()
    
    # Get unique countries for filter dropdown
    countries = Country.objects.all().order_by('name')
    
    context = {
        'plans': plans,
        'countries': countries,
        'selected_country': country_filter,
        'selected_price': price_filter,
        'search_query': search_query,
    }
    
    return render(request, 'esim_store/home.html', context)

def countries_view(request):
    """Countries page showing plans by country"""
    countries = Country.objects.all().order_by('name')
    
    # Get world pack plans (plans available in 5 or more countries)
    world_pack_plans = ESIMPlan.objects.filter(
        is_active=True
    ).annotate(
        country_count=Count('countries')
    ).filter(
        country_count__gte=5
    ).order_by('price')[:12]  # Limit to 12 world pack plans
    
    context = {
        'countries': countries,
        'world_pack_plans': world_pack_plans,
    }
    return render(request, 'esim_store/countries.html', context)

def country_plans(request, country_code):
    """Show plans for a specific country"""
    country = get_object_or_404(Country, code=country_code)
    plans = ESIMPlan.objects.filter(
        is_active=True, 
        countries=country
    ).select_related()
    
    context = {
        'country': country,
        'plans': plans,
    }
    return render(request, 'esim_store/country_plans.html', context)

def about_view(request):
    """About Us page"""
    try:
        content = PageContent.objects.get(slug='about-us')
    except PageContent.DoesNotExist:
        content = PageContent.objects.create(
            title='About AnytimeEsim',
            slug='about-us',
            content='''<h2>Welcome to AnytimeEsim</h2>
            <p>We are your trusted partner for global eSIM solutions. Our mission is to provide fast, reliable, and affordable connectivity worldwide.</p>
            <p>With AnytimeEsim, you can stay connected wherever you go without the hassle of physical SIM cards.</p>''',
            is_active=True
        )
    
    context = {
        'content': content,
    }
    return render(request, 'esim_store/page.html', context)

def faq_view(request):
    """FAQ page"""
    try:
        content = PageContent.objects.get(slug='faq')
    except PageContent.DoesNotExist:
        content = PageContent.objects.create(
            title='Frequently Asked Questions',
            slug='faq',
            content='''<h2>How does eSIM work?</h2>
            <p>eSIM is a digital SIM that allows you to activate a cellular plan without having to use a physical SIM card.</p>
            
            <h2>Is eSIM secure?</h2>
            <p>Yes, eSIM technology is secure and provides the same level of security as traditional SIM cards.</p>
            
            <h2>Which devices support eSIM?</h2>
            <p>Most modern smartphones, tablets, and smartwatches support eSIM technology. Check your device specifications.</p>''',
            is_active=True
        )
    
    context = {
        'content': content,
    }
    return render(request, 'esim_store/page.html', context)

def search_plans(request):
    """AJAX endpoint for searching plans"""
    query = request.GET.get('q', '')
    
    if query:
        plans = ESIMPlan.objects.filter(
            Q(is_active=True) &
            (Q(name__icontains=query) |
             Q(data_amount__icontains=query) |
             Q(countries__name__icontains=query))
        ).distinct().select_related()[:12]  # Limit results
    else:
        plans = ESIMPlan.objects.filter(is_active=True)[:12]
    
    results = []
    for plan in plans:
        countries = list(plan.countries.values_list('name', flat=True))
        results.append({
            'id': plan.id,
            'name': plan.name,
            'price': str(plan.price),
            'data_amount': plan.data_amount,
            'validity_days': plan.validity_days,
            'countries': countries,
            'image': plan.image.url if plan.image else None,
            'description': plan.description,
        })
    
    return JsonResponse({'results': results})