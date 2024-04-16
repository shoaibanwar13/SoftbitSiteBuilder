# Import necessary modules and views
 
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from DynamicGenerator.views import *
from django.contrib.auth import views
# Define URL patterns
urlpatterns = [
    path('login/', views.LoginView.as_view(template_name='login.html'), name='login'),
    path("password_reset/", views.PasswordResetView.as_view(template_name='reset_password.html'), name="password_reset"),
    path(
        "password_reset_done/",
        views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(template_name='password_set.html'),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'),
        name="password_reset_complete",
    ),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('proxy_warning_view/', proxy_warning_view, name='proxy_warning_view'),
    path('check_username/',check_username,name='check_username'),
    path('check_email/',check_email,name='check_email'),
    path('check_password/',check_password,name='check_password'),
    path('profile/', profile, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('oursites/', oursites, name='oursites'),
    path('sites/<str:category>/', sites_by_category, name='sites_by_category'),
    path('sitedetail/<str:id>',sitedetail,name='sitedetail'),
    path('search/',search,name='search'),
    path('searchpage/', searchpage, name='searchpage'),
    path('mainpagesearch/', mainpagesearch, name='mainpagesearch'),
    path('rating/', rating, name='rating'),
    path('ourteam/', ourteam, name='ourteam'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('preview1/',preview1,name='preview1'),
    path('Asper/', Asper, name='Asper'),
    path('AspersitePreview/', AspersitePreview, name='AspersitePreview'),
    path('edit_Asper/', edit_Asper, name='edit_Asper'),
    path('delete_Advertising_site/<str:id>/', delete_Advertising_site, name='delete_Advertising_site'),
    path('preview2/',preview2,name='preview2'),
    path('yourportfolio/', yourportfolio, name='yourportfolio'),
    path('portfolio/', portfolio, name='portfolio'),
    path('edit_Portfolio/', edit_Portfolio, name='edit_Portfolio'),
    path('delete_Portfolio_site/<str:id>/', delete_Portfolio_site, name='delete_Portfolio_site'),
    path('preview3/',preview3,name='preview3'),
    path('Medipark/', Medipark, name='Medipark'),
    path('edit_Medipark/',edit_Medipark, name='edit_Medipark'),
    path('MediparkPreview/',MediparkPreview, name='MediparkPreview'),
    path('delete_Medical_site/<str:id>/', delete_Medical_site, name='delete_Medical_site'),
    path('start_order/', start_order, name='start_order'),
    path('payment_success/',payment_success,name='payment_success'),
    path('payment_cancel/',payment_cancel,name='payment_cancel'),
    path('Deployesite/', Deployesite, name='Deployesite'),
    path('deployecheckout/', deployecheckout, name='deployecheckout'),
    path('deploye_order/', deploye_order, name='deploye_order'),
    path('payment_success2/',payment_success2, name='payment_success2'),
    path('userpurchase/',userpurchase,name='userpurchas'),
    path('userdashboard/', userdashboard, name='userdashboard'),
    path('withdraw/',withdraw,name='withdraw'),
    path('history/',history, name=' history'),
    path('mysites/', mysites, name='mysites'),
    path('referal/', referal, name='referal'),
    path('Planexpiredalert/', Planexpiredalert, name='Planexpiredalert'),
    path('Affliatemarketing/', Affliatemarketing, name='Affliatemarketing'),
    path('Termsandpolicies/', Termsandpolicies, name='Termsandpolicies'),    
    path('PrivacyandPolicy/', PrivacyandPolicy, name='PrivacyandPolicy'), 
    path('Userguide/', Userguide, name='Userguide')
    
   
   
    
    
    
   
    
    
    
    
   
    
    
   
    
    
  
    
    
   
    
    
]

# Serve media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files during development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
