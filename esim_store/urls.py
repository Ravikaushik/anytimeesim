from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('countries/', views.countries_view, name='countries'),
    path('country/<str:country_code>/', views.country_plans, name='country_plans'),
    path('about/', views.about_view, name='about'),
    path('faq/', views.faq_view, name='faq'),
    path('api/search/', views.search_plans, name='search_plans'),
]