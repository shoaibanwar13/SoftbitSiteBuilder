 
from django.shortcuts import render, redirect, HttpResponse,get_object_or_404 
from django.contrib.auth import get_user_model
from .models import *
from django.http import JsonResponse
import stripe
import re
from django.conf import settings
import json
from django.shortcuts import render,redirect
from  .forms import ProfileUpdateForm,UserUpdateForm,Portfoliotemplate,UpdatePortfoliotemplate,Advertisingtem,UpdateAdvertisingtem,RatingForm,DeployesiteForm,HospitalForm,HospitalEditForm
from  .models import Profile,Withdrawl_Request,Deploye,Contact,Hospital,team,Offers,Co_Founder,Testimonial
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils import timezone
from ipware import get_client_ip
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from .proxydetector import proxy_checker
from .useractivity import track_user_activity
# send email to expire  plan user
def send_mail(email,user,site_name):
    email_subject2 = "Plan Expire Date Is Approaching "
    message2 = render_to_string('SendEmail6.html', {
                'user':user,
                'site_name':site_name
                 
        })
    email_message2 = EmailMessage(email_subject2, message2, settings.EMAIL_HOST_USER, [email])
    email_message2.send()
# Function to start a scheduler for sending emails
def start_scheduler(email,user,site_name):
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mail, 'interval', hours=0,minutes=0,seconds=0,args=[email,user,site_name])  # Change as needed
    scheduler.start()
#Function to Detect expire plan to  email when plan expire to start schedular
def sendemail():
     
    plans = SitePurchase.objects.filter(paid=True)
    for plan in plans:
        expiredate=plan.expiration_date
        days_until_expiration = (expiredate - timezone.now()).days
        print(days_until_expiration)
        if 0 < days_until_expiration <= 1:
            user=plan.user
            email=plan.user.email
            site_name=plan.name
            plan.delete()
            start_scheduler(email,user,site_name)
#calling sending mail function
sendemail()
def account_restriction(request):
    return render(request, 'accountrestriction.html')

# View to render the proxy warning page
def proxy_warning_view(request):
    return render(request, 'ipblock.html')

# View to check if a username already exists
def check_username(request):
    # Retrieve username from POST request
    username = request.POST.get('username')
    if get_user_model().objects.filter(username=username).exists():
        # Return response indicating username already exists
        return HttpResponse("<div style='color:red;'>Username Already Exist </div>")
    else:
        # Return response indicating username is available
        return HttpResponse("<div style='color:green;'>Username is Available </div>")

# View to check if an email is already in use
def check_email(request):
    # Retrieve email from POST request
    email = request.POST.get('email')
    if get_user_model().objects.filter(email=email).exists():
        # Return response indicating email is already used
        return HttpResponse("<div style='color:red;'>Email Already Used</div>")
    else:
        # Return response indicating email is available
        return HttpResponse("<div style='color:green;'>Available </div>")

# Import necessary module for JSON response
from django.http import JsonResponse

# View to check password strength and match with confirmation
def check_password(request):
    # Retrieve password and confirm password from POST request
    password = request.POST.get('password1')
    confirm_password = request.POST.get('password2')
    # Regular expressions to check password strength
    if (
            len(password) < 8 or  # Check if password is at least 8 characters long
            not re.search(r'[a-z]', password) or  # Check if password contains at least one lowercase letter
            not re.search(r'[0-9]', password) or  # Check if password contains at least one digit
            not re.search(r'[!@#$%^&*()_+{}[\]:;<>,.?/~\\-]', password)  # Check if password contains at least one symbol
        ):
        # Return response indicating password requirements
        return HttpResponse("<div style='color:white;'>Password must contain at least one lowercase letter, one number, and be at least 8 characters long. (For Security Please Add at least one Symbol)</div>")
    elif password != confirm_password:
        # Return response indicating password and confirm password do not match
        return HttpResponse("<div style='color:red;'>Password Not Matche</div>")
    else:
        # Return response indicating password and confirm password match
        return HttpResponse("<div style='color:white;' >Password Matche</div>")@login_required
# View function to display user profile
def profile(request):
    # Check if user activity needs to be traced, redirect if necessary
    trace = track_user_activity(request)
    if trace == True:
        return redirect('account_restriction')
    trace2=UserMonitering.objects.filter(user=request.user)
    
    # Check if request is from a proxy, redirect if necessary
    check = proxy_checker(request)
    if check == True:
        return redirect('proxy_warning_view')
    
    # Retrieve user profile data
    data = Profile.objects.get(user=request.user)
    
    # Check if user commission is zero
    usercommession = data.commession == 0
    
    # Retrieve total balance of the user
    totalbalance = data.balance
    
    # Retrieve current user profile
    currentuser = Profile.objects.filter(user=request.user)
    
    # Render profile template with relevant data
    return render(request, 'profile.html', {'currentuser': currentuser, 'usercommession': usercommession, 'totalbalance': totalbalance, 'trace': trace2})

# View function to edit user profile
@login_required
def edit_profile(request):
    # Check if user activity needs to be traced, redirect if necessary
    trace = track_user_activity(request)
    if trace == True:
        return redirect('account_restriction')
    
    # Check if request is from a proxy, redirect if necessary
    check = proxy_checker(request)
    if check == True:
        return redirect('proxy_warning_view')
    
    # Retrieve user profile data
    data = Profile.objects.get(user=request.user)
    
    # Retrieve total balance of the user
    totalbalance = data.balance
    
    # Check if user commission is zero
    usercommession = data.commession == 0
    
    if request.method == 'POST':
        # If request method is POST, process form data
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        # If request method is GET, render form with existing data
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    # Prepare context to pass to the template
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'usercommession': usercommession,
        'totalbalance': totalbalance
    }

    # Render edit profile template with form data
    return render(request, 'editprofile.html', context)


# View function to display all sites
def oursites(request):
    # Check if request is from a proxy, redirect if necessary
    check = proxy_checker(request)
    if check == True:
        return redirect('proxy_warning_view')
    
    # Retrieve all sites, categories, top-rated sites, and offers
    allsite = Oursites.objects.all()
    category = Category.objects.all()
    toprated = Oursites.objects.all()[:3]
    offer = Offers.objects.all()
    
    # Check if the request is via HTMX
    if request.htmx:
        # Return the response with HTMX template
        return render(request, 'webgenrator/webtemplates.html', {'allsite': allsite, 'category': category, 'toprated': toprated, 'offer': offer})
    else:
        # Return the response with regular template
        return render(request, 'webtemplates.html', {'allsite': allsite, 'category': category, 'toprated': toprated, 'offer': offer})

# View function to display sites by category
def sites_by_category(request, category):
    # Retrieve sites filtered by category
    sites = Oursites.objects.filter(category=category)
    
    # Check if the request is via HTMX
    if request.htmx:
        # Return the response with HTMX template
        return render(request, 'webgenrator/categorypage.html', {'sites': sites})
    else:
        # Return the response with regular template
        return render(request, 'category.html', {'sites': sites})

# View function to display site details
@login_required
def sitedetail(request, id):
    # Check if user activity needs to be traced, redirect if necessary
    trace = track_user_activity(request)
    if trace == True:
        return redirect('account_restriction')
    
    # Check if request is from a proxy, redirect if necessary
    check = proxy_checker(request)
    if check == True:
        return redirect('proxy_warning_view')
    
    # Retrieve site details by ID
    site_detail = get_object_or_404(Oursites, id=id)
    product = Oursites.objects.get(pk=id)
    
    # Retrieve ratings for the site
    ratings = Rating.objects.filter(product=id)
    average_rating = ratings.aggregate(models.Avg('rating'))['rating__avg'] or 0
    rated = Rating.objects.filter(user=request.user, product=id)

    # Check if form is submitted via POST method
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.product = product
            rating.user = request.user
            rating.save()
            return redirect('sitedetail', id=id)
    else:
        form = RatingForm()
    
    # Retrieve Stripe public key
    pub_key = settings.STRIPE_PUBLIC_KEY
    
    # Retrieve related site based on the site's category
    related_site = Oursites.objects.filter(category=site_detail.category).exclude(id=id)[:1]
    
    # Check if the request is via HTMX
    if request.htmx:
        # Return the response with HTMX template
        return render(request, "webgenrator/sitedetailpage.html", {'detail': site_detail, 'related_site': related_site, 'pub_key': pub_key, 'form': form, 'rated': rated, 'average_rating': average_rating})
    else:
        # Return the response with regular template
        return render(request, 'webdetail.html', {'detail': site_detail, 'related_site': related_site, 'pub_key': pub_key, 'form': form, 'rated': rated, 'average_rating': average_rating})
# View function to handle search functionality
def search(request):
    # Retrieve search text from the POST request
    search_text = request.POST.get('search')
    # Filter categories based on name containing search text
    results2 = Category.objects.filter(name__icontains=search_text)
    # Filter sites based on name containing search text
    results = Oursites.objects.filter(name__icontains=search_text)
    # Prepare context to pass to the template
    context = {"results": results, 'results2': results2}
    # Render search result template with context
    return render(request, 'searchresult.html', context)

# View function to render the search page
def searchpage(request):
    # Check if the request is via HTMX
    if request.htmx:
        return render(request, 'webgenrator/search.html')
    else:
        return render(request, 'searchpage.html')

# View function to handle search functionality on the main page
def mainpagesearch(request):
    # Retrieve search text from the POST request
    search_text = request.POST.get('search')
    # Filter categories based on name containing search text
    results2 = Category.objects.filter(name__icontains=search_text)
    # Filter sites based on name containing search text
    results = Oursites.objects.filter(name__icontains=search_text)
    # Prepare context to pass to the template
    context = {"results": results, 'results2': results2}
    # Render search results template with context
    return render(request, 'searchresults.html', context)

# View function to handle rating submission
@login_required
def rating(request):
    # Check if user activity needs to be traced, redirect if necessary
    trace = track_user_activity(request)
    if trace == True:
        return redirect('account_restriction')
    # Check if request is from a proxy, redirect if necessary
    check = proxy_checker(request)
    if check == True:
        return redirect('proxy_warning_view')
    
    if request.method == 'POST':
        # Retrieve rating value and site name from POST request
        rating_value = request.POST.get('rating')
        rating_int = int(rating_value)
        sitename = request.POST.get('sitename')  # Assuming 'sitename' is the name of your dropdown field
        # Create and save the rating object
        rating = Rating.objects.create(
                site=sitename,
                user=request.user,
                rating=rating_int
        )
        rating.save()
        return redirect('oursite')  # Redirect after successful submission

# View function to render the team page
def ourteam(request):
    # Retrieve data for team members and co-founders
    data = team.objects.all()
    data2 = Co_Founder.objects.all()
    # Check if the request is via HTMX
    if request.htmx:
        return render(request, "webgenrator/teampage.html", {'data': data, 'data2': data2})
    else:
        return render(request, 'ourteam.html', {'data': data, 'data2': data2})

# View function to handle contact form submission
@login_required
def contact(request):
    if request.method == "POST":
        # Retrieve data from the POST request
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        phone = request.POST.get("phone")
        # Save contact details to database
        myquery = Contact(name=name, email=email, message=message, phone=phone)
        myquery.save()
        # Send email notification
        email_subject2 = "Customer Contact Detail Recieved "
        message = render_to_string('SendEmail7.html', {
                'user': request.user,
                'name': name,
                'phone': phone,
                'email': email,
                'message': message
        })
        email_message = EmailMessage(email_subject2, message, settings.EMAIL_HOST_USER, ['shoaib4311859@gmail.com'])
        email_message.send()
        # Display success message and redirect
        messages.success(request, 'Thank You For Contacting With Us! We will Back Soon!!! ')
        redirect('contact.html')
    # Check if the request is via HTMX
    if request.htmx:
        return render(request, "webgenrator/contactpage.html")
    else:
        return render(request, 'contact.html')
# View function to render the about page
def about(request):
    # Retrieve data for team members and co-founders
    data = team.objects.all()
    data2 = Co_Founder.objects.all()
    # Check if the request is via HTMX
    if request.htmx:
        return render(request, "webgenrator/aboutpage.html", {'data': data, 'data2': data2})
    else:
        return render(request, 'about.html', {'data': data, 'data2': data2})

# View function to render the AdvertisementPreview1 page
@login_required
def preview1(request):
    # Check if user activity needs to be traced, redirect if necessary
    trace = track_user_activity(request)
    if trace == True:
        return redirect('account_restriction')
    # Check if request is from a proxy, redirect if necessary
    check = proxy_checker(request)
    if check == True:
        return redirect('proxy_warning_view')
    return render(request, 'AdvertisementPreview1.html')

# View function to render the AspersitePreview page
def AspersitePreview(request):  
    # Check if user activity needs to be traced, redirect if necessary
    trace = track_user_activity(request)
    if trace == True:
        return redirect('account_restriction')
    # Check if request is from a proxy, redirect if necessary
    check = proxy_checker(request)
    if check == True:
        return redirect('proxy_warning_view') 
    try:
        SitePurchase.objects.get(user=request.user, paid=True, name='Asper')
    except SitePurchase.DoesNotExist:
        return redirect('/')
    try:
        user_purchases = SitePurchase.objects.get(user=request.user, paid=True, name='Asper')
        expiration_date = user_purchases.expiration_date
        days_until_expiration = (expiration_date - timezone.now()).days
        print(days_until_expiration)
        if days_until_expiration == 0:
            SitePurchase.objects.filter(user=request.user, paid=True, name='Asper').delete()
            Advertising.objects.filter(user=request.user).delete()
            return redirect('Planexpiredalert')
    except:
        pass
    try:
        Advertising.objects.get(user=request.user)
    except Advertising.DoesNotExist:
        return redirect('/')
    data = Advertising.objects.filter(user=request.user)
    return render(request, 'advertising/advertising.html', {'data': data})

# View function to render the Asper page
@login_required
def Asper(request):
    # Check if user activity needs to be traced, redirect if necessary
    trace = track_user_activity(request)
    if trace == True:
        return redirect('account_restriction')
    # Check if request is from a proxy, redirect if necessary
    check = proxy_checker(request)
    if check == True:
        return redirect('proxy_warning_view')
    try:
        SitePurchase.objects.get(user=request.user, paid=True, name='Asper')
    except SitePurchase.DoesNotExist:
        return redirect('/')
    try:
        user_purchases = SitePurchase.objects.get(user=request.user, paid=True, name='Asper')
        expiration_date = user_purchases.expiration_date
        days_until_expiration = (expiration_date - timezone.now()).days
        print(days_until_expiration)
        if days_until_expiration == 0:
            SitePurchase.objects.filter(user=request.user, paid=True, name='Asper').delete()
            return redirect('Planexpiredalert')
    except:
        pass
    try:
        data = Advertising.objects.get(user=request.user)
        if data:
            return redirect('AspersitePreview')
    except Advertising.DoesNotExist:
        pass
    if request.method == 'POST':
        form = Advertisingtem(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('AspersitePreview')
    else:
        form = Advertisingtem()
    return render(request, 'Advertisingform.html', {'form': form})

# View function to render the edit Asper page
@login_required
def edit_Asper(request):
    # Check if user activity needs to be traced, redirect if necessary
    trace = track_user_activity(request)
    if trace == True:
        return redirect('account_restriction')
    # Check if request is from a proxy, redirect if necessary
    check = proxy_checker(request)
    if check == True:
        return redirect('proxy_warning_view')
    try:
        SitePurchase.objects.get(user=request.user, paid=True, name='Asper')
    except SitePurchase.DoesNotExist:
        return redirect('/')
    try:
        user_purchases = SitePurchase.objects.filter(user=request.user, paid=True, name='Asper')
        for purchase in user_purchases:
            expiration_date = purchase.expiration_date
            days_until_expiration = (expiration_date - timezone.now()).days
            print(days_until_expiration)
            if days_until_expiration == 0:
                SitePurchase.objects.filter(user=request.user, paid=True, name='Asper').delete()
                return redirect('Planexpiredalert')
    except:
        pass
    try:
        Adver = Advertising.objects.get(user=request.user)
    except Advertising.DoesNotExist:
        return redirect('/')
    if request.method == 'POST':
        form = UpdateAdvertisingtem(request.POST, request.FILES, instance=Adver)
        if form.is_valid():
            form.save()
            return redirect('AspersitePreview')
    else:
        form = UpdateAdvertisingtem(instance=Adver)
    return render(request, 'editadvertising.html', {'form': form})

# View function to delete advertising site
@login_required
def delete_Advertising_site(request, id):
    # Check if user activity needs to be traced, redirect if necessary
    trace = track_user_activity(request)
    if trace == True:
        return redirect('account_restriction')
    # Check if request is from a proxy, redirect if necessary
    check = proxy_checker(request)
    if check == True:
        return redirect('proxy_warning_view')
    Advertising.objects.filter(user=request.user, id=id).delete()
    return redirect('oursites')
@login_required
# View function to render the portfolio preview page
def preview2(request):
    # Check if user activity needs to be traced, redirect if necessary
    trace = track_user_activity(request)
    if trace == True:
        return redirect('account_restriction')
    # Check if request is from a proxy, redirect if necessary
    check = proxy_checker(request)
    if check == True:
        return redirect('proxy_warning_view')
    return render(request, 'portfoliopreview.html')

# View function to render the portfolio page
@login_required
def portfolio(request):
    # Check if user activity needs to be traced, redirect if necessary
    trace = track_user_activity(request)
    if trace == True:
        return redirect('account_restriction')
    # Check if request is from a proxy, redirect if necessary
    check = proxy_checker(request)
    if check == True:
        return redirect('proxy_warning_view')
    try:
        SitePurchase.objects.get(user=request.user, paid=True, name='yourportfolio')
    except SitePurchase.DoesNotExist:
        return redirect('/')
    try:
        user_purchases = SitePurchase.objects.get(user=request.user, paid=True, name='yourportfolio')
        expiration_date = user_purchases.expiration_date
        days_until_expiration = (expiration_date - timezone.now()).days
        print(days_until_expiration)
        if days_until_expiration == 0:
            SitePurchase.objects.filter(user=request.user, paid=True, name='yourportfolio').delete()
            return redirect('Planexpiredalert')
    except:
        pass
    try:
        Portfolio.objects.get(user=request.user)
    except Portfolio.DoesNotExist:
        return redirect('/')
    data = Portfolio.objects.filter(user=request.user)
    return render(request, 'portfolio.html', {'data': data})

# View function to render the "your portfolio" page
@login_required
def yourportfolio(request):
    # Check if user activity needs to be traced, redirect if necessary
    trace = track_user_activity(request)
    if trace == True:
        return redirect('account_restriction')
    # Check if request is from a proxy, redirect if necessary
    check = proxy_checker(request)
    if check == True:
        return redirect('proxy_warning_view')
    try:
        SitePurchase.objects.get(user=request.user, paid=True, name='yourportfolio')
    except SitePurchase.DoesNotExist:
        return redirect('/')
    try:
        user_purchases = SitePurchase.objects.get(user=request.user, paid=True, name='yourportfolio')
        expiration_date = user_purchases.expiration_date
        days_until_expiration = (expiration_date - timezone.now()).days
        print(days_until_expiration)
        if days_until_expiration == 0:
            SitePurchase.objects.filter(user=request.user, paid=True, name='yourportfolio').delete()
            return redirect('Planexpiredalert')
    except:
        pass
    try:
        data = Portfolio.objects.get(user=request.user)
        if data:
            return redirect('portfolio')
    except Portfolio.DoesNotExist:
        pass
    if request.method == 'POST':
        form = Portfoliotemplate(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('/yourportfolio/')
    else:
        form = Portfoliotemplate()
    return render(request, 'portfoliotemform.html', {'form': form})

# View function to render the edit portfolio page
@login_required
def edit_Portfolio(request):
    # Check if user activity needs to be traced, redirect if necessary
    trace = track_user_activity(request)
    if trace == True:
        return redirect('account_restriction')
    # Check if request is from a proxy, redirect if necessary
    check = proxy_checker(request)
    if check == True:
        return redirect('proxy_warning_view')
    try:
        SitePurchase.objects.get(user=request.user, paid=True, name='yourportfolio')
    except SitePurchase.DoesNotExist:
        return redirect('/')
    try:
        user_purchases = SitePurchase.objects.get(user=request.user, paid=True, name='yourportfolio')
        expiration_date = user_purchases.expiration_date
        days_until_expiration = (expiration_date - timezone.now()).days
        print(days_until_expiration)
        if days_until_expiration == 0:
            SitePurchase.objects.filter(user=request.user, paid=True, name='yourportfolio').delete()
            return redirect('Planexpiredalert')
    except:
        pass
    try:
        portfolio = Portfolio.objects.get(user=request.user)
    except Portfolio.DoesNotExist:
        return redirect('/')
    if request.method == 'POST':
        form = UpdatePortfoliotemplate(request.POST, request.FILES, instance=portfolio)
        if form.is_valid():
            form.save()
            return redirect('/portfolio/')
    else:
        form = UpdatePortfoliotemplate(instance=portfolio)
    return render(request, 'editportfolio.html', {'form': form})

# View function to delete portfolio site
@login_required
def delete_Portfolio_site(request, id):
    # Check if user activity needs to be traced, redirect if necessary
    trace = track_user_activity(request)
    if trace == True:
        return redirect('account_restriction')
    # Check if request is from a proxy, redirect if necessary
    check = proxy_checker(request)
    if check == True:
        return redirect('proxy_warning_view')
    Portfolio.objects.filter(user=request.user, id=id).delete()
    return redirect('oursites')
# View function to render the preview page for Medipark
def preview3(request):
    return render(request, 'mediparkpreview.html')

# View function to render the Medipark preview page
@login_required
def MediparkPreview(request):
    # Check if user activity needs to be traced, redirect if necessary
    trace = track_user_activity(request)
    if trace == True:
        return redirect('account_restriction')
    # Check if request is from a proxy, redirect if necessary
    check = proxy_checker(request)
    if check == True:
        return redirect('proxy_warning_view')
    try:
        SitePurchase.objects.get(user=request.user, paid=True, name='Medipark')
    except SitePurchase.DoesNotExist:
        return redirect('/')
    try:
        user_purchases = SitePurchase.objects.get(user=request.user, paid=True, name='Medipark')
        expiration_date = user_purchases.expiration_date
        days_until_expiration = (expiration_date - timezone.now()).days
        print(days_until_expiration)
        if days_until_expiration == 0:
            SitePurchase.objects.filter(user=request.user, paid=True, name='Medipark').delete()
            return redirect('Planexpiredalert')
    except:
        pass
    try:
        Hospital.objects.get(user=request.user)
    except Hospital.DoesNotExist:
        return redirect('/')
    data = Hospital.objects.filter(user=request.user)
    return render(request, 'medipark.html', {'data': data})

# View function to render the Medipark form page
@login_required
def Medipark(request):
    # Check if user activity needs to be traced, redirect if necessary
    trace = track_user_activity(request)
    if trace == True:
        return redirect('account_restriction')
    # Check if request is from a proxy, redirect if necessary
    check = proxy_checker(request)
    if check == True:
        return redirect('proxy_warning_view')
    try:
        SitePurchase.objects.get(user=request.user, paid=True, name='Medipark')
    except SitePurchase.DoesNotExist:
        return redirect('/')
    try:
        user_purchases = SitePurchase.objects.get(user=request.user, paid=True, name='Medipark')
        expiration_date = user_purchases.expiration_date
        days_until_expiration = (expiration_date - timezone.now()).days
        print(days_until_expiration)
        if days_until_expiration == 0:
            SitePurchase.objects.filter(user=request.user, paid=True, name='Medipark').delete()
            return redirect('Planexpiredalert')
    except:
        pass
    try:
        data = Hospital.objects.get(user=request.user)
        if data:
            return redirect('MediparkPreview')
    except Hospital.DoesNotExist:
        pass
    if request.method == 'POST':
        form = HospitalForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('MediparkPreview')
    else:
        form = HospitalForm()
    return render(request, 'mediparkform.html', {'form': form})

# View function to render the edit Medipark page
@login_required
def edit_Medipark(request):
    # Check if user activity needs to be traced, redirect if necessary
    trace = track_user_activity(request)
    if trace == True:
        return redirect('account_restriction')
    # Check if request is from a proxy, redirect if necessary
    check = proxy_checker(request)
    if check == True:
        return redirect('proxy_warning_view')
    try:
        SitePurchase.objects.get(user=request.user, paid=True, name='Medipark')
    except SitePurchase.DoesNotExist:
        return redirect('/')
    try:
        user_purchases = SitePurchase.objects.get(user=request.user, paid=True, name='Medipark')
        expiration_date = user_purchases.expiration_date
        days_until_expiration = (expiration_date - timezone.now()).days
        print(days_until_expiration)
        if days_until_expiration == 0:
            SitePurchase.objects.filter(user=request.user, paid=True, name='Medipark').delete()
            return redirect('Planexpiredalert')
    except:
        pass
    try:
        hospital = Hospital.objects.get(user=request.user)
    except Hospital.DoesNotExist:
        return redirect('/')
    if request.method == 'POST':
        form = HospitalEditForm(request.POST, request.FILES, instance=hospital)
        if form.is_valid():
            form.save()
            return redirect('/MediparkPreview/')
    else:
        form = HospitalEditForm(instance=hospital)
    return render(request, 'editmedipark.html', {'form': form})

# View function to delete Medical site from Medipark
@login_required
def delete_Medical_site(request, id):
    # Check if user activity needs to be traced, redirect if necessary
    trace = track_user_activity(request)
    if trace == True:
        return redirect('account_restriction')
    # Check if request is from a proxy, redirect if necessary
    check = proxy_checker(request)
    if check == True:
        return redirect('proxy_warning_view')
    Hospital.objects.filter(user=request.user, id=id).delete()
    return redirect('oursites')
# View function to start the order process
def start_order(request):
    # Check if user activity needs to be traced, redirect if necessary
    trace = track_user_activity(request)
    if trace == True:
        return redirect('account_restriction')
    # Check if request is from a proxy, redirect if necessary
    check = proxy_checker(request)
    if check == True:
        return redirect('proxy_warning_view')
    
    # Extract data from request body
    data = json.loads(request.body)
    name = data.get('name', '')
    raw_paid_amount = data.get('paid_amount', '0.00')
    
    # Convert paid_amount to Decimal
    paid_amount = Decimal(raw_paid_amount)
    
    # Multiply by 100 and format the result
    result = int(paid_amount * Decimal('100.00'))
    
    items = []
    price = result
    
    # Construct line items for Stripe checkout
    items.append({
        'price_data': {
            'currency': 'usd',
            'product_data': {
                'name': name,
            },
            'unit_amount': price,
        },
        'quantity': 1
    })

    # Create a Stripe checkout session
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=items,
        mode='payment',
        success_url=request.build_absolute_uri('/payment_success/'),
        cancel_url=request.build_absolute_uri('/payment_cancel/'),
    )
    
    payment_intent = session.payment_intent

    # Create a SitePurchase object to represent the order
    order = SitePurchase.objects.create(
        user=request.user, 
        name=data['name'], 
        paid_amount=data['paid_amount'],
        paid=False
    )

    return JsonResponse({'session': session, 'order': payment_intent})

# View function to handle successful payment
@login_required
def payment_success(request):
    # Check if user activity needs to be traced, redirect if necessary
    trace = track_user_activity(request)
    if trace == True:
        return redirect('account_restriction')
    # Check if request is from a proxy, redirect if necessary
    check = proxy_checker(request)
    if check == True:
        return redirect('proxy_warning_view')
    
    try:
        # Retrieve the order that needs to be marked as paid
        order = get_object_or_404(SitePurchase, user=request.user, paid=False)
        order.paid = True
        order.save()
        
        # Extract necessary data from the order
        sitename = order.name
        price = order.paid_amount
        purchaseid = order.id
        
        # Send a success email to the user
        email_subject2 = "Thank You for Your Purchase on Softbit Website Builder"
        message2 = render_to_string('SendEmail3.html', {
            'sitename': sitename,
            'paid': price,
            'purchaseid': purchaseid
        })
        email_message2 = EmailMessage(email_subject2, message2, settings.EMAIL_HOST_USER, [request.user.email])
        email_message2.send()
        
        messages.success(request, 'Now this is your site. Please enjoy your journey with us.')

        return render(request, 'success.html')
    except Exception as e:
        print(f"Error: {str(e)}")
        return HttpResponse(status=400)

# View function to handle payment cancellation
@login_required    
def payment_cancel(request):
    # Check if user activity needs to be traced, redirect if necessary
    trace = track_user_activity(request)
    if trace == True:
        return redirect('account_restriction')
    # Check if request is from a proxy, redirect if necessary
    check = proxy_checker(request)
    if check == True:
        return redirect('proxy_warning_view')
    
    return render(request, 'fail.html')

# View function to render the checkout page for deployment
@login_required
def deployecheckout(request):
    # Check if user activity needs to be traced, redirect if necessary
    trace = track_user_activity(request)
    if trace == True:
        return redirect('account_restriction')
    # Check if request is from a proxy, redirect if necessary
    check = proxy_checker(request)
    if check == True:
        return redirect('proxy_warning_view')
    
    try:
        SitePurchase.objects.filter(user=request.user)
    except SitePurchase.DoesNotExist:
        return redirect('/')
    
    # Retrieve deployment rates
    rates = DeployeRate.objects.all()[:1]
    pub_key = settings.STRIPE_PUBLIC_KEY
    
    return render(request, 'deployecheckout.html', {'pub_key': pub_key, 'rates': rates})

# View function to initiate deployment order
@login_required
def deploye_order(request):
    # Check if user activity needs to be traced, redirect if necessary
    trace = track_user_activity(request)
    if trace == True:
        return redirect('account_restriction')
    # Check if request is from a proxy, redirect if necessary
    check = proxy_checker(request)
    if check == True:
        return redirect('proxy_warning_view')
    
    # Extract data from request body
    data = json.loads(request.body)
    name = data.get('name', '')
    raw_paid_amount = data.get('paid_amount', '0.00')
    domain = data.get('domain', '')

    # Convert paid_amount to Decimal
    paid_amount = Decimal(raw_paid_amount)

    # Multiply by 100 and format the result
    result = int(paid_amount * Decimal('100.00'))

    items = []
    price = result

    # Construct line items for Stripe checkout
    items.append({
        'price_data': {
            'currency': 'usd',
            'product_data': {
                'name': name,
            },
            'unit_amount': price,
        },
        'quantity': 1
    })

    # Create a Stripe checkout session
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=items,
        mode='payment',
        success_url=request.build_absolute_uri('/payment_success2/'),
        cancel_url=request.build_absolute_uri('/payment_cancel/'),
    )
    stripe_session_id = session.id
    
    # Construct the success_url with the session_id parameter
    success_url = request.build_absolute_uri(f'/payment_success2/?session_id={stripe_session_id}')
    payment_intent = session.payment_intent

    # Create a Deploye object to represent the deployment order
    order = Deploye.objects.create(
        user=request.user, 
        name=data['name'], 
        domainname=data['domain'],
        paid_amount=data['paid_amount'],
        paid=False
    )

    return JsonResponse({'session': session, 'order': payment_intent})

# View function to handle successful deployment payment
@login_required
def payment_success2(request):
    trace = track_user_activity(request)
    if trace == True:
        return redirect('account_restriction')
    check = proxy_checker(request)
    if check == True:
        return redirect('proxy_warning_view')
    
    order = get_object_or_404(Deploye, user=request.user, paid=False)
    order.paid = True
    order.save()
    
    sitename = order.name
    domainname = order.domainname
    price = order.paid_amount
    purchaseid = order.id
    
    # Send a success email to the user
    email_subject2 = "Thank You for Your Purchase on Softbit Website Builder"
    message2 = render_to_string('SendEmail4.html', {
        'sitename': sitename,
        'paid': price,
        'purchaseid': purchaseid,
        'domainname': domainname
    })
    email_message2 = EmailMessage(email_subject2, message2, settings.EMAIL_HOST_USER, [request.user.email])
    email_message2.send()
    
    messages.success(request, 'Now this is your site. Please enjoy your journey with us.')
    
    return render(request, 'deployesuccess.html')

# View function to deploy the site
@login_required 
def Deployesite(request):
    trace = track_user_activity(request)
    if trace == True:
        return redirect('account_restriction')
    check = proxy_checker(request)
    if check == True:
        return redirect('proxy_warning_view')
    
     
    siteuser = Deploye.objects.filter(user=request.user, paid=True).last()
    
    if request.method == 'POST':
        form = DeployesiteForm(request.POST, request.FILES, instance=siteuser)
        if form.is_valid():
            form.save()
            return redirect('mysites')
    else:
        form = DeployesiteForm(instance=siteuser)

    return render(request, 'deploye.html', {'form': form})  
@login_required
def userpurchase(request):
    # Check if user activity needs to be traced, redirect if necessary
    trace = track_user_activity(request)
    if trace == True:
        return redirect('account_restriction')
    # Check if request is from a proxy, redirect if necessary
    check = proxy_checker(request)
    if check == True:
        return redirect('proxy_warning_view')
    
    # Get all purchases made by the user
    user_purchases = SitePurchase.objects.filter(user=request.user, paid=True)
    website_links = [{'name': purchase.name, 'link': purchase.name ,'price':purchase.paid_amount} for purchase in user_purchases]
    
    if request.htmx:
        return render(request, "webgenrator/purchase.html", {'website_links': website_links})
    else:
        return render(request, 'userpurchasesite.html', {'website_links': website_links})

@login_required
def userdashboard(request):
    # Check if user activity needs to be traced, redirect if necessary
    trace = track_user_activity(request)
    if trace == True:
        return redirect('account_restriction')
    # Check if request is from a proxy, redirect if necessary
    check = proxy_checker(request)
    if check == True:
        return redirect('proxy_warning_view')
     
    # Get user's profile information
    data = Profile.objects.get(user=request.user)
    comtotal = data.commession
    totalbalance = data.balance
    userbalace = data.balance == 0
    usercommession = data.commession == 0
    totalwithdraw = data.withdrawl_amount
    
    # Get user's withdrawal requests and format withdrawal dates
    user_withdrawal_requests = Withdrawl_Request.objects.filter(user=request.user)
    withdrawal_dates = list(user_withdrawal_requests.values_list('created_at', flat=True))
    withdrawal_dates_json = json.dumps([[date.year, date.month - 1, date.day] for date in withdrawal_dates])
    
    # Get user's total purchase amount
    purchase_plans = SitePurchase.objects.filter(user=request.user)
    total_purchase_amount = sum(plan.paid_amount for plan in purchase_plans)
    
    # Get user's total deployment amount
    deploye_plan = Deploye.objects.filter(user=request.user)
    total_deploye = sum(plan.paid_amount for plan in deploye_plan)
   
    # Get user's withdrawal requests and approved requests
    withdraw = Withdrawl_Request.objects.filter(user=request.user)
    Approved = Withdrawl_Request.objects.filter(user=request.user, status='Approved') 
    
    if request.htmx:
        return render(request, 'webgenrator/userdashboard.html', {'comtotal': comtotal, 'totalbalance': totalbalance, 'userbalace': userbalace, 'totalwithdraw': totalwithdraw, 'withdrawal_dates_json': withdrawal_dates_json, 'withdraw': withdraw, 'Approved': Approved, 'total_purchase_amount': total_purchase_amount, 'total_deploye': total_deploye, 'usercommession': usercommession})
    else:
        return render(request, 'userdashboard.html', {'comtotal': comtotal, 'totalbalance': totalbalance, 'userbalace': userbalace, 'totalwithdraw': totalwithdraw, 'withdrawal_dates_json': withdrawal_dates_json, 'withdraw': withdraw, 'Approved': Approved, 'total_purchase_amount': total_purchase_amount, 'total_deploye': total_deploye, 'usercommession': usercommession})
   
@login_required
def withdraw(request):
    # Check if user activity needs to be traced, redirect if necessary
    trace = track_user_activity(request)
    if trace == True:
        return redirect('account_restriction')
    # Check if request is from a proxy, redirect if necessary
    check = proxy_checker(request)
    if check == True:
        return redirect('proxy_warning_view')
     
    # Get user's profile information
    profile = Profile.objects.get(user=request.user)
    payout = int(profile.balance)
    
    if request.method == "POST":
        pmethod = request.POST.get("pmethod")
        account_no = request.POST.get("account_no")
        withrwal_amount = int(request.POST.get("amount"))
        bank = request.POST.get("bank")
        route = request.POST.get("route")
        
        # Create withdrawal request and update user's balance
        if withrwal_amount <= int(profile.balance):
            if withrwal_amount >= 10:
                query = Withdrawl_Request(user=request.user, profile=profile, account_no=account_no, amount=withrwal_amount, pay_method=pmethod, created_at=timezone.now(), bank=bank, routing_no=route)
                query.save() 
                profile.balance -= withrwal_amount
                profile.withdrawl_amount += withrwal_amount
                profile.save()
                
                # Send email notifications
                email_subject2 = "New Withdrawal Request Received"
                message2 = render_to_string('SendEmail2.html', {
                    'profile': profile,
                    'pmethod':  pmethod,
                    'bank': bank,
                    'route': route,
                    'account_no': account_no,
                    'withrwal_amount': withrwal_amount,
                })
                email_message2 = EmailMessage(email_subject2, message2, settings.EMAIL_HOST_USER, ['shoaib4311859@gmail.com'])
                email_message2.send()
                
                email_subject2 = "Withdrawl Request Received"
                message2 = render_to_string('SendEmail2.html', {
                    'profile': profile,
                    'pmethod':  pmethod,
                    'account_no': account_no,
                    'withrwal_amount': withrwal_amount,
                })
                email_message2 = EmailMessage(email_subject2, message2, settings.EMAIL_HOST_USER, [request.user.email])
                email_message2.send()
                
                messages.success(request, 'Withdrawal Success!! It takes 10 to 30 minutes to arrive in your account.')
                return redirect('userdashboard')
            else:
                messages.success(request, 'Minimum Withdrawal is $10')
                return redirect('userdashboard')
        else:
            messages.warning(request, 'Your Withdrawal Request Is Greater Than Available Balance.')
            return redirect('userdashboard')
    return  render(request, 'userdashboard.html')

@login_required
def history(request):
    # Check if user activity needs to be traced, redirect if necessary
    trace = track_user_activity(request)
    if trace == True:
        return redirect('account_restriction')
    # Check if request is from a proxy, redirect if necessary
    check = proxy_checker(request)
    if check == True:
        return redirect('proxy_warning_view')
    
    # Get user's profile information
    data = Profile.objects.get(user=request.user)
    usercommession = data.commession == 0
    
    # Get user's deployment history, withdrawal requests, and purchases
    usersite = Deploye.objects.filter(user=request.user)
    user_withdrawal_requests = Withdrawl_Request.objects.filter(user=request.user)
    user_purchase = SitePurchase.objects.filter(user=request.user)
    
    # Calculate total purchase and deployment amounts
    purchase_plans = SitePurchase.objects.filter(user=request.user)
    total_purchase_amount = sum(plan.paid_amount for plan in purchase_plans)
    deploye_plan = Deploye.objects.filter(user=request.user)
    total_deploye = sum(plan.paid_amount for plan in deploye_plan)
    
    return render(request, 'history.html', {'user_withdrawal_requests': user_withdrawal_requests, 'user_purchase': user_purchase, 'usersite': usersite, 'total_purchase_amount': total_purchase_amount, 'total_deploye': total_deploye, 'usercommession': usercommession})

@login_required
def mysites(request):
    # Get user's profile information
    data = Profile.objects.get(user=request.user)
    usercommession = data.commession == 0
    
    # Get user's deployed sites
    usersite = Deploye.objects.filter(user=request.user)
    
    return render(request, 'sitestatus.html', {'usersite': usersite, 'usercommession': usercommession})

@login_required
def referal(request):
    # Check if user activity needs to be traced, redirect if necessary
    trace = track_user_activity(request)
    if trace == True:
        return redirect('account_restriction')
    # Check if request is from a proxy, redirect if necessary
    check = proxy_checker(request)
    if check == True:
        return redirect('proxy_warning_view')
     
    # Get user's profile information
    data = Profile.objects.get(user=request.user)
    usercommession = data.commession == 0
    
    # Get user's referral code, recommended profiles, and earnings
    profile = get_object_or_404(Profile, user=request.user)
    refer_code = profile.code
    my_recs = profile.get_recommended_profile()
    my_earning = profile.commession
     
    return render(request, 'Reffral.html', {'refer_code': refer_code, 'my_recs': my_recs, 'my_earning': my_earning, 'usercommession': usercommession})

def Planexpiredalert(request):
    # Check if request is from a proxy, redirect if necessary
    check = proxy_checker(request)
    if check == True:
        return redirect('proxy_warning_view')
    return render(request, 'planexperimeaage.html')

def Termsandpolicies(request):
    # Check if request is from a proxy, redirect if necessary
    check = proxy_checker(request)
    if check == True:
        return redirect('proxy_warning_view')
    return render(request, 'terms.html') 

def PrivacyandPolicy(request):
    # Check if request is from a proxy, redirect if necessary
    check = proxy_checker(request)
    if check == True:
        return redirect('proxy_warning_view')
    return render(request, 'privacy.html')

def Affliatemarketing(request):
    # Check if request is from a proxy, redirect if necessary
    check = proxy_checker(request)
    if check == True:
        return redirect('proxy_warning_view')
    return render(request, 'affliate.html')

def Userguide(request):
    # Check if request is from a proxy, redirect if necessary
    check = proxy_checker(request)
    if check == True:
        return redirect('proxy_warning_view')
    return render(request, 'userguide.html') 

@login_required
def testimonial(request):
    # Check if user activity needs to be traced, redirect if necessary
    trace = track_user_activity(request)
    if trace == True:
        return redirect('account_restriction')
    # Check if request is from a proxy, redirect if necessary
    check = proxy_checker(request)
    if check == True:
        return redirect('proxy_warning_view')
    
    # Process testimonial form submission
    if request.method == "POST":
        star = request.POST.get('star')
        message = request.POST.get('message')
        image = Profile.objects.get(user=request.user)
        profile_image = image.profilepic
        
        # Save testimonial to database
        query = Testimonial(user=request.user, name=request.user.username, profile_image=profile_image, star=star, message=message)
        query.save()
        return redirect('/')
        
def emailconfirm(request):
    return render(request, 'emailverify.html')  

def accountactiveemail(request):
    return render(request, 'emailverificationsend.html')
