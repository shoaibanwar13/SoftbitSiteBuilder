# Import necessary modules and views
 
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from DynamicGenerator.views import   oursites,deploye_order,Deployesite,profile,edit_profile, history, payment_success2, userdashboard,referal,proxy_warning_view,rating,deployecheckout, delete_user_site,payment_success,check_username,check_email,search,check_password,preview1,Asper,payment_cancel, ourteam, contact,start_order, about,  Advertising_web,sitedetail,userpurchase,sites_by_category,yourportfolio,portfolio,edit_Portfolio,edit_Advertising,withdraw,mysites,preview3
from django.contrib.auth import views
# Define URL patterns
urlpatterns = [
    

    # Other views
    path('sites/<str:category>/', sites_by_category, name='sites_by_category'),
    path('payment_success2/',payment_success2, name='payment_success2'),
    path('profile/', profile, name='profile'),
    path('mysites/', mysites, name='mysites'),
    path('referal/', referal, name='referal'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('oursites/', oursites, name='oursites'),
    path('Deployesite/', Deployesite, name='Deployesite'),
    path('deployecheckout/', deployecheckout, name='deployecheckout'),
    path('delete_user_site/', delete_user_site, name='delete_user_site'),
    path('userdashboard/', userdashboard, name='userdashboard'),
    path('deploye_order/', deploye_order, name='deploye_order'),
     
    path('history/',history, name=' history'),
   
    path('ourteam/', ourteam, name='ourteam'),
    path('proxy_warning_view/', proxy_warning_view, name='proxy_warning_view'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('Advertising_web/', Advertising_web, name='Advertising_web'),
    path('Asper/', Asper, name='Asper'),
    path('edit_Advertising/', edit_Advertising, name='edit_Advertising'),
    path('yourportfolio/', yourportfolio, name='yourportfolio'),
    path('portfolio/', portfolio, name='portfolio'),
    path('rating/', rating, name='rating'),
    path('edit_Portfolio/', edit_Portfolio, name='edit_Portfolio'),
    path('sitedetail/<str:id>',sitedetail,name='sitedetail'),
    path('payment_success/',payment_success,name='payment_success'),
    path('payment_cancel/',payment_cancel,name='payment_cancel'),
    path('preview1/',preview1,name='preview1'),
    path('preview3/',preview3,name='preview3'),
    path('userpurchase/',userpurchase,name='payment_cancel'),
    path('withdraw/',withdraw,name='withdraw'),
    path('start_order/', start_order, name='start_order'),
    path('check_username/',check_username,name='check_username'),
    path('check_email/',check_email,name='check_email'),
    path('search/',search,name='search'),
    path('check_password/',check_password,name='check_password'),
    path('logout', views.LogoutView.as_view(), name='logout'),
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
 
]

# Serve media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files during development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
