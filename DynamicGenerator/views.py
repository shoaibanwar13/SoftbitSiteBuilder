 
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
def account_restriction(request):
    return render(request, 'accountrestriction.html')

def proxy_warning_view(request):
    return render(request, 'ipblock.html')
def check_username(request):
    username=request.POST.get('username')
    if get_user_model().objects.filter(username=username).exists():
       return  HttpResponse("<div style='color:red;'>Username Already Exist </div>")
    else:
        return HttpResponse("<div style='color:green;'>Username is Available </div>")
def check_email(request):
    email=request.POST.get('email')
    if get_user_model().objects.filter(email=email).exists():
       return  HttpResponse("<div style='color:red;'>Email Already Used</div>")
    else:
        return HttpResponse("<div style='color:green;'>Available </div>")
from django.http import JsonResponse

def check_password(request):
    password = request.POST.get('password1')
    confirm_password = request.POST.get('password2')
    if (
            len(password) < 8 or  # Check if password is at least 8 characters long
            not re.search(r'[a-z]', password) or  # Check if password contains at least one lowercase letter
            not re.search(r'[0-9]', password) or  # Check if password contains at least one digit
            not re.search(r'[!@#$%^&*()_+{}[\]:;<>,.?/~\\-]', password)  # Check if password contains at least one symbol
        ):
        return  HttpResponse("<div style='color:white;'>Password must contain at least   one lowercase letter,  one number, and be at least 8 characters long.(For Security Please Add at least one Symbol)</div>")
    elif password != confirm_password:
        return  HttpResponse("<div style='color:red;'>Password Not Matche</div>")
    else:
        return  HttpResponse("<div style='color:white;' >Password Matche</div>")

@login_required
def profile(request):
    data=Profile.objects.get(user=request.user)
    trace=UserMonitering.objects.filter(user=request.user)
    usercommession=data.commession==0
    
    totalbalance=data.balance
    currentuser=Profile.objects.filter(user=request.user)
    return render(request,'profile.html',{'currentuser':currentuser,'usercommession':usercommession,'totalbalance':totalbalance,'trace':trace})
@login_required
def edit_profile(request):
    data=Profile.objects.get(user=request.user)
    totalbalance=data.balance
    usercommession=data.commession==0
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'usercommession':usercommession,
        'totalbalance':totalbalance
    }

    return render(request, 'editprofile.html', context,)


def oursites(request):
     
    allsite=Oursites.objects.all()
    category=Category.objects.all()
    toprated = Oursites.objects.all()[:3]
    offer=Offers.objects.all()
    if request.htmx:
        return render(request, 'webgenrator/webtemplates.html',{'allsite':allsite,'category':category,'toprated':toprated,'offer':offer})
    else:
          return render(request, 'webtemplates.html',{'allsite':allsite,'category':category,'toprated':toprated,'offer':offer})
def sites_by_category(request, category):
     
    sites = Oursites.objects.filter(category=category)
    if request.htmx:
        return render(request, 'webgenrator/categorypage.html',{'sites': sites})
    else:
         return render(request, 'category.html', {'sites': sites}) 
@login_required
def sitedetail(request, id):
     
    site_detail = get_object_or_404(Oursites, id=id)
    product = Oursites.objects.get(pk=id)
    ratings = Rating.objects.filter(product=id)
    average_rating = ratings.aggregate(models.Avg('rating'))['rating__avg'] or 0
    rated=Rating.objects.filter(user=request.user,product=id)

    print(average_rating)
    if request.method == 'POST':
        form = RatingForm(request.POST)  # If using a form
        if form.is_valid():
            rating = form.save(commit=False)  # Don't commit yet
            rating.product = product
            rating.user = request.user  # Assuming logged-in user is available
            rating.save()
            return redirect('sitedetail', id=id)  # Redirect after successful submission
    else:
        form = RatingForm()
     
             
     
    pub_key= settings.STRIPE_PUBLIC_KEY
    # Retrieve related products based on the site's category
    related_site = Oursites.objects.filter(category=site_detail.category).exclude(id=id)[:1]
    
    has_purchased= SitePurchase.objects.filter(user=request.user, name=site_detail.name).exists()


     
    print(related_site)
    if request.htmx:
        return render(request, "webgenrator/sitedetailpage.html",{'detail': site_detail, 'related_site': related_site,'pub_key':pub_key,'has_purchased':has_purchased,'form':form,'rated':rated,'average_rating':average_rating} )
    else:
        return render(request, 'webdetail.html', {'detail': site_detail, 'related_site': related_site ,'pub_key':pub_key,'has_purchased':has_purchased,'form':form,'rated':rated,'average_rating':average_rating})
def search(request):
    search_text = request.POST.get('search')
    results2 = Category.objects.filter(name__icontains=search_text)
    results = Oursites.objects.filter(name__icontains=search_text)
    print(results)
    context = {"results": results,
                'results2':results2}

    return render(request, 'searchresult.html', context)
def searchpage(request):
    if request.htmx:
       return render(request, 'webgenrator/search.html')
    else:
      return render(request, 'searchpage.html')

    
def mainpagesearch(request):
    search_text = request.POST.get('search')
    results2 = Category.objects.filter(name__icontains=search_text)
    results = Oursites.objects.filter(name__icontains=search_text)
    print(results)
    context = {"results": results,
                'results2':results2}

    return render(request, 'searchresults.html', context)

@login_required
def rating(request):
     
    if request.method == 'POST':
        rating_value = request.POST.get('rating')
        rating_int=int(rating_value)
        print
        sitename = request.POST.get('sitename')  # Assuming 'sitename' is the name of your dropdown field
           # Create and save the rating object
        rating = Rating.objects.create(
                site=sitename,
                user=request.user,
                rating=rating_int
        )
        rating.save()
        return redirect('oursite')
   
def ourteam(request):
    data=team.objects.all()
    data2=Co_Founder.objects.all()
     
    if request.htmx:
        return render(request, "webgenrator/teampage.html",{'data':data,'data2':data2})
    else:
         return render(request, 'ourteam.html',{'data':data,'data2':data2})
def contact(request):
     
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        message=request.POST.get("message")
        phone=request.POST.get("phone")
        myquery=Contact(name=name,email=email,message=message,phone=phone)
        myquery.save()
        email_subject2 = "Customer Contact Detail Recieved "
        message = render_to_string('SendEmail7.html', {
                'user':request.user,
                'name':name,
                'phone':phone,
                'email':email,
                'message':message


              
        })
        email_message = EmailMessage(email_subject2, message, settings.EMAIL_HOST_USER, ['shoaib4311859@gmail.com'])
        email_message.send()

        messages.success(request, 'Thank You For Contacting With Us! We will Back Soon!!! ')
        redirect('contact.html')
      
    if request.htmx:
        return render(request, "webgenrator/contactpage.html")
    else:
        return render(request, 'contact.html')



def about(request):
    data=team.objects.all()
    data2=Co_Founder.objects.all()
    if request.htmx:
        return render(request, "webgenrator/aboutpage.html",{'data':data,'data2':data2})
    else:
        return render(request, 'about.html',{'data':data,'data2':data2})

@login_required
def preview1(request):
    return render(request, 'AdvertisementPreview1.html')
def AspersitePreview(request):
    user_purchases = SitePurchase.objects.filter(user=request.user, paid=True,name='Asper')
    if user_purchases==False:
        return redirect('/')
    data=Advertising.objects.filter(user=request.user).exists()
    if data==False:
        return redirect('AspersitePreview')
    print(user_purchases)
    for purchase in user_purchases:
        # Check if the expiration date is approaching (e.g., within 7 days)
        expiration_date = purchase.expiration_date
        days_until_expiration = (expiration_date - timezone.now()).days
        print(days_until_expiration)
        if days_until_expiration==0:
            return redirect('Planexpiredalert')
        if 0 < days_until_expiration <= 7:
            email_subject2 = "Plan Expire Date Is Approaching "
            message2 = render_to_string('SendEmail6.html', {
                'user':request.user,
                'site_name':'Asper'

              
        })
            email_message2 = EmailMessage(email_subject2, message2, settings.EMAIL_HOST_USER, [request.user.email])
            email_message2.send()
 
    
    data=Advertising.objects.filter(user=request.user)
     
    
    return render(request,'advertising/advertising.html',{'data':data})
@login_required
def Asper(request):
    user_purchases = SitePurchase.objects.filter(user=request.user, paid=True,name='Asper')
    if user_purchases==False:
        return redirect('/')
    data=Advertising.objects.filter(user=request.user).exists()
    if data==True:
        return redirect('AspersitePreview')
     
    if request.method == 'POST':
        form = Advertisingtem(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('AspersitePreview')
    else:
        form =  Advertisingtem()
     
         
    return render(request, 'Advertisingform.html',{'form':form})
@login_required
def edit_Asper(request):
    user_purchases = SitePurchase.objects.filter(user=request.user, paid=True,name='Asper')
    if user_purchases==False:
        return redirect('/')
    try:
        Adver = Advertising.objects.get(user=request.user)
    except  Advertising.DoesNotExist:
        return redirect('/') 
 
    
   
    if request.method == 'POST':
        form = UpdateAdvertisingtem(request.POST,
                                   
                                   request.FILES,
                                   instance=Adver)
        if  form.is_valid():
            form.save()
            return redirect('AspersitePreview')

    else:
        form =UpdateAdvertisingtem(instance=Adver)

    return render(request, 'editadvertising.html',{'form':form})
@login_required
def delete_Advertising_site(request,id):
    Advertising.objects.filter(user=request.user,id=id).delete()
    return redirect('oursites')
@login_required
def preview2(request):
    return render(request, 'portfoliopreview.html')
@login_required
def portfolio(request):
    user_purchases = SitePurchase.objects.filter(user=request.user, paid=True,name='yourportfolio')
    if user_purchases==False:
        return redirect('/')
    try:
        data = Portfolio.objects.filter(user=request.user)
    except  Portfolio.DoesNotExist:
        return redirect('/')
    print(user_purchases)
    for purchase in user_purchases:
        # Check if the expiration date is approaching (e.g., within 7 days)
        expiration_date = purchase.expiration_date
        days_until_expiration = (expiration_date - timezone.now()).days
        print(days_until_expiration)
        if days_until_expiration==0:
            return redirect('Planexpiredalert')
        if 0 < days_until_expiration <= 7:
            email_subject2 = "Plan Expire Date Is Approaching "
            message2 = render_to_string('SendEmail6.html', {
                'user':request.user,
                'site_name':'yourportfolio'

              
        })
            email_message2 = EmailMessage(email_subject2, message2, settings.EMAIL_HOST_USER, [request.user.email])
            email_message2.send()
 
    
    
    return render(request, 'portfolio.html',{'data':data})
@login_required
def yourportfolio(request):
    user_purchases = SitePurchase.objects.filter(user=request.user, paid=True,name='yourportfolio')
    if user_purchases==False:
        return redirect('/')
    try:
        Portfolio.objects.filter(user=request.user)
    except  Portfolio.DoesNotExist:
        return redirect('/')
    ifuserdataexist=Portfolio.objects.filter(user=request.user).exists()
    if ifuserdataexist:
        return redirect('portfolio')
     
    
    
    if request.method == 'POST':
        form = Portfoliotemplate( request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('/yourportfolio/')
    else:
        form =  Portfoliotemplate()
     
    return render(request, 'portfoliotemform.html',{'form':form})
@login_required
def edit_Portfolio(request):
    user_purchases = SitePurchase.objects.filter(user=request.user, paid=True,name='yourportfolio')
    if user_purchases==False:
        return redirect('/')
    print(user_purchases)
    try:
        portfolio = Portfolio.objects.get(user=request.user)
    except Portfolio.DoesNotExist:
        return redirect('/')
     
 
    
   
    if request.method == 'POST':
        form = UpdatePortfoliotemplate(request.POST,
                                   
                                   request.FILES,
                                   instance=portfolio)
        if  form.is_valid():
            form.save()
            return redirect('/yourportfolio/')

    else:
        form =UpdatePortfoliotemplate(instance=portfolio)

    return render(request, 'editportfolio.html',{'form':form})

@login_required
def delete_Portfolio_site(request,id):
    Portfolio.objects.filter(user=request.user,id=id).delete()
    return redirect('oursites')
def preview3(request):
    return render(request,'mediparkpreview.html')
@login_required
def MediparkPreview(request):
    user_purchases = SitePurchase.objects.filter(user=request.user, paid=True,name='Medipark')
    if user_purchases==False:
        return redirect('/')
     
    try:
        Hospital.objects.get(user=request.user)
    except  Hospital.DoesNotExist:
        return redirect('/')
    data=Hospital.objects.filter(user=request.user)
     
    print(user_purchases)
    for purchase in user_purchases:
        # Check if the expiration date is approaching (e.g., within 7 days)
        expiration_date = purchase.expiration_date
        days_until_expiration = (expiration_date - timezone.now()).days
        print(days_until_expiration)
        if days_until_expiration==0:
            return redirect('Planexpiredalert')
        if 0 < days_until_expiration <= 7:
            email_subject2 = "Plan Expire Date Is Approaching "
            message2 = render_to_string('SendEmail6.html', {
                'user':request.user,
                'site_name':'Medipark'

              
        })
            email_message2 = EmailMessage(email_subject2, message2, settings.EMAIL_HOST_USER, [request.user.email])
            email_message2.send()
 

    return render(request,'medipark.html',{'data':data})
@login_required
def Medipark(request):
    user_purchases = SitePurchase.objects.filter(user=request.user, paid=True,name='Medipark')
    if user_purchases==False:
        return redirect('/') 
     
    if request.method == 'POST':
        form = HospitalForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('MediparkPreview')
    else:
        form =  HospitalForm()

    return render(request,'mediparkform.html',{'form':form})
@login_required
def edit_Medipark(request):
    
    user_purchases = SitePurchase.objects.filter(user=request.user, paid=True,name='Medipark')
    if user_purchases==False:
        return redirect('/')
    try:
        hospital = Hospital.objects.get(user=request.user)
    except  Hospital.DoesNotExist:
        return redirect('/')
    for purchase in user_purchases:
        # Check if the expiration date is approaching (e.g., within 7 days)
        expiration_date = purchase.expiration_date
        days_until_expiration = (expiration_date - timezone.now()).days
        print(days_until_expiration)
        if days_until_expiration==0:
            return redirect('Planexpiredalert')
    if request.method == 'POST':
        form = HospitalEditForm(request.POST,
                                   
                                   request.FILES,
                                   instance=hospital)
        if  form.is_valid():
            form.save()
            return redirect('/MediparkPreview/')

    else:
        form =HospitalEditForm(instance=hospital)

    return render(request, 'editmedipark.html',{'form':form})

@login_required
def delete_Medical_site(request,id):
    Hospital.objects.filter(user=request.user,id=id).delete()
    return redirect('oursites')
@login_required
def start_order(request):
     
    data = json.loads(request.body)
    print(data)
    name = data.get('name', '')
    raw_paid_amount = data.get('paid_amount', '0.00')

# Convert paid_amount to Decimal
    paid_amount = Decimal(raw_paid_amount)

# Multiply by 100 and format the result
    result= int(paid_amount * Decimal('100.00'))
     

    print("Name:", name)
    print("Paid Amount:", result )
    items = []
    price = result # $5.00 USD
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

    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=items,
        mode='payment',
        success_url=request.build_absolute_uri('/payment_success/'),
        cancel_url=request.build_absolute_uri('/payment_cancel/'),
    )
    
    payment_intent = session.payment_intent
    

    order=SitePurchase.objects.create(
        user=request.user, 
        name=data['name'], 
         
        paid_amount=data['paid_amount'],
        paid=False
    )
    order.save
    
    return JsonResponse({'session': session, 'order': payment_intent})
 
 
@login_required
def payment_success(request):
    
    try:
       
        order = get_object_or_404(SitePurchase, user=request.user, paid=False)
        order.paid = True
        order.save()
        sitename=order.name
        price=order.paid_amount
        purchaseid= order.id
        user_profile=Profile.objects.get(user=request.user)
        reffferer=user_profile.recommended_by
        print(reffferer)
        if reffferer:
               commission=int(order.paid_amount)*0.1
               reffferer_profile=Profile.objects.get(user=reffferer)
               reffferer_profile.commession +=commission
               reffferer_profile.balance +=commission
               reffferer_profile.save()
                
        else:
          pass
        email_subject2 = " Thank You for Your Purchase on Softbit Website Builder"
        message2 = render_to_string('SendEmail3.html', {
                    'profile':profile,
                    'sitename':sitename,
                    'paid':price ,
                    'purchaseid':purchaseid
                     
              
        })
        email_message2 = EmailMessage(email_subject2, message2, settings.EMAIL_HOST_USER, [request.user.email])
        email_message2.send()
        messages.success(request, 'Now This is your site please enjoye your journery with us')
    
         
        
        

        return render(request, 'success.html')
    except Exception as e:
        print(f"Error: {str(e)}")
        return HttpResponse(status=400)
@login_required    
def payment_cancel(request):
    return render(request,'fail.html')
@login_required
def deployecheckout(request):
     
    try:
        SitePurchase.objects.filter(user=request.user)
    except   SitePurchase.DoesNotExist:
        return redirect('/')
    rates=DeployeRate.objects.all()[:1]
    print(rates)
    pub_key= settings.STRIPE_PUBLIC_KEY
    return render(request,'deployecheckout.html',{'pub_key':pub_key,'rates':rates})
@login_required
def deploye_order(request):
    data = json.loads(request.body)
    print(data)
    name = data.get('name', '')
    raw_paid_amount = data.get('paid_amount', '0.00')
    domain=data.get('domain', '')

# Convert paid_amount to Decimal
    paid_amount = Decimal(raw_paid_amount)

# Multiply by 100 and format the result
    result= int(paid_amount * Decimal('100.00'))
     

    print("Name:", name)
    print("Paid Amount:", result )
    items = []
    price = result # $5.00 USD
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

    order=Deploye.objects.create(
        user=request.user, 
        name=data['name'], 
        domainname=data['domain'],
        paid_amount=data['paid_amount'],
        paid=False
    )
    order.save
    
    return JsonResponse({'session': session, 'order': payment_intent})
@login_required
def payment_success2(request):
 
        order = get_object_or_404(Deploye, user=request.user, paid=False)
        order.paid = True
        order.save()
        sitename=order.name
        domainname=order.domainname
        price=order.paid_amount
        purchaseid= order.id
        email_subject2 = " Thank You for Your Purchase on Softbit Website Builder"
        message2 = render_to_string('SendEmail4.html', {
                    'profile':profile,
                    'sitename':sitename,
                    'paid':price ,
                    'purchaseid':purchaseid,
                    'domainname':domainname
                     
              
        })
        email_message2 = EmailMessage(email_subject2, message2, settings.EMAIL_HOST_USER, [request.user.email])
        email_message2.send()
        messages.success(request, ' Now is your site please enjoye your journery with us')
    
        return render(request, 'success.html')
     
@login_required 
def Deployesite(request):
    
    try:
        siteuser = Deploye.objects.get(user=request.user)
    except  Deploye.DoesNotExist:
        return redirect('/')
    if request.method == 'POST':
        form = DeployesiteForm(request.POST,
                                   request.FILES,
                                   instance=siteuser)
        if  form.is_valid():
            form.save()
            return redirect('mysites')

    else:
        form =DeployesiteForm(instance=siteuser)

    return render(request, 'deploye.html',{'form':form})  


@login_required
def userpurchase(request):
    
    user_purchases = SitePurchase.objects.filter(user=request.user, paid=True)
    website_links = []

    for purchase in user_purchases:
         
        website_links.append({'name': purchase.name, 'link': purchase.name ,'price':purchase.paid_amount})
    if request.htmx:
        return render(request, "webgenrator/purchase.html",{'website_links':website_links})
    else:
       return render(request, 'userpurchasesite.html',{'website_links':website_links})

@login_required
def userdashboard(request):
     
    data=Profile.objects.get(user=request.user)
    comtotal=data.commession
    totalbalance=data.balance
    userbalace=data.balance==0
    usercommession=data.commession==0
    totalwithdraw=data.withdrawl_amount
    user_withdrawal_requests = Withdrawl_Request.objects.filter(user=request.user)
    withdrawal_dates = list(user_withdrawal_requests.values_list('created_at', flat=True))
    withdrawal_dates_json = json.dumps([[date.year, date.month - 1, date.day] for date in withdrawal_dates])

    print(withdrawal_dates_json)
    purchase_plans = SitePurchase.objects.filter(user=request.user)
    total_purchase_amount = sum(plan.paid_amount for plan in purchase_plans)
    deploye_plan=Deploye.objects.filter(user=request.user)
    total_deploye = sum(plan.paid_amount for plan in deploye_plan)
   
    withdraw=Withdrawl_Request.objects.filter(user=request.user)
    Approved=Withdrawl_Request.objects.filter(user=request.user,status='Approved') 
    if request.htmx:
        return render(request, 'webgenrator/userdashboard.html',{'comtotal':comtotal,'totalbalance':totalbalance,'userbalace':userbalace,'totalwithdraw':totalwithdraw,'withdrawal_dates_json':withdrawal_dates_json,'withdraw':withdraw, 'Approved':Approved,'total_purchase_amount':total_purchase_amount,'total_deploye':total_deploye,'usercommession':usercommession})
    else:
         return render(request, 'userdashboard.html',{'comtotal':comtotal,'totalbalance':totalbalance,'userbalace':userbalace,'totalwithdraw':totalwithdraw,'withdrawal_dates_json':withdrawal_dates_json,'withdraw':withdraw, 'Approved':Approved,'total_purchase_amount':total_purchase_amount,'total_deploye':total_deploye,'usercommession':usercommession})
   
@login_required
def withdraw(request):
     
    pro=Profile.objects.get(user=request.user)
    payout=int(pro.balance)
    print(payout)
    if request.method=="POST":
            pmethod=request.POST.get("pmethod")
             
            account_no=request.POST.get("account_no")
            withrwal_amount=int(request.POST.get("amount"))
            bank=request.POST.get("bank")
            route=request.POST.get("route")
            profile=Profile.objects.get(user=request.user)
            if withrwal_amount <= int(profile.balance):
                if withrwal_amount >=10:
                    query=Withdrawl_Request(user=request.user, profile=profile,account_no=account_no,amount=withrwal_amount,pay_method=pmethod, created_at=timezone.now(),bank=bank,routing_no=route)
                    query.save() 
                    profile.balance -=withrwal_amount
                    profile.withdrawl_amount +=withrwal_amount
                    profile.save()
                    email_subject2 = "New Withdrawal Request Received"
                    message2 = render_to_string('SendEmail2.html', {
                    'profile':profile,
                    'pmethod':  pmethod,
                    'bank':bank,
                    'route':route,
                    'account_no':account_no,
                    'withrwal_amount': withrwal_amount,
              
        })
                    email_message2 = EmailMessage(email_subject2, message2, settings.EMAIL_HOST_USER, ['shoaib4311859@gmail.com'])
                    email_message2.send()
                    email_subject2 = "Withdrawl Request Recived"
                    message2 = render_to_string('SendEmail2.html', {
                    'profile':profile,
                    'pmethod':  pmethod,
                     
                    'account_no':account_no,
                    'withrwal_amount': withrwal_amount,
              
        })
                    email_message2 = EmailMessage(email_subject2, message2, settings.EMAIL_HOST_USER, [request.user.email])
                    email_message2.send()
                    messages.success(request, 'Withdrawl Success!! It take 10 to 30 mintue to Arrived in your Account ')
                    return redirect('userdashboard')
                else:
                     messages.success(request, 'Minimum Withdrawl is  $10 ')
                     return redirect('userdashboard')
                
            if withrwal_amount>profile.balance:
              messages.warning(request, 'Your Withdrwal Request Is Greater Than Available Balance.')
              redirect('userdashboard')
    return  render(request,'userdashboard.html')
@login_required
def history(request):
    data=Profile.objects.get(user=request.user)
    usercommession=data.commession==0
    usersite=Deploye.objects.filter(user=request.user)
    user_withdrawal_requests = Withdrawl_Request.objects.filter(user=request.user)
    user_purchase=SitePurchase.objects.filter(user=request.user)
    purchase_plans = SitePurchase.objects.filter(user=request.user)
    total_purchase_amount = sum(plan.paid_amount for plan in purchase_plans)
    deploye_plan=Deploye.objects.filter(user=request.user)
    total_deploye = sum(plan.paid_amount for plan in deploye_plan)
    return render(request,'history.html',{'user_withdrawal_requests':user_withdrawal_requests,'user_purchase':user_purchase,'usersite':usersite,'total_purchase_amount':total_purchase_amount,'total_deploye':total_deploye,'usercommession':usercommession})
@login_required
def mysites(request):
    data=Profile.objects.get(user=request.user)
    usercommession=data.commession==0
    usersite=Deploye.objects.filter(user=request.user)
    return render(request,'sitestatus.html',{'usersite':usersite,'usercommession':usercommession})

@login_required
def referal(request):
     
    data=Profile.objects.get(user=request.user)
     
    usercommession=data.commession==0
        # Get the user's profile
    profile = get_object_or_404(Profile, user=request.user)

        # Extract referral code
    refer_code = profile.code

        # Get recommended profiles
    my_recs = profile.get_recommended_profile()
        
        # Get commission/earning
    my_earning = profile.commession
     
    return render(request, 'Reffral.html', {'refer_code': refer_code, 'my_recs': my_recs, 'my_earning': my_earning,'usercommession':usercommession})
 
def Planexpiredalert(request):
    return render(request,'planexperimeaage.html')
def  Termsandpolicies(request):
    return render(request,'terms.html') 
def PrivacyandPolicy(request):
    return render(request,'privacy.html')
def Affliatemarketing(request):
    return render(request,'affliate.html')
def Userguide(request):
    return render(request,'userguide.html') 
@login_required
def testimonial(request):
    if request.method=="POST":
        star=request.POST.get('star')
        message=request.POST.get('message')
        image=Profile.objects.get(user=request.user)
        profile_image=image.profilepic
        
        print(profile_image)
        query=Testimonial(user=request.user,name=request.user.username,profile_image=profile_image,star=star,message=message)
        query.save()
        return redirect('/')
    
     
