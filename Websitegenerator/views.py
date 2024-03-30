from django.shortcuts import render,redirect

from DynamicGenerator.forms import SignUpForm 
 
from DynamicGenerator.models import Profile
 
from django.contrib.auth.models import User
from django.shortcuts import render ,redirect
 
 
from django.contrib.auth import login
 
from ipware import get_client_ip
import requests
 
    
def index(request,*args,**kwargs):
    client_ip, _ = get_client_ip(request)
     
    print(client_ip)
     # Replace YOUR_TOKEN with your actual IPinfo API token
    api_url = 'https://vpnapi.io/api/{}?key=2290f864fc4c4f2e8d9d2fc4f8a75938'.format(client_ip)
    # Make a request to IPinfo API
    response = requests.get(api_url)
    data = response.json()
    print(data)
    # Check if the IP is associated with a VPN or proxy
    if  data['security']['vpn']or data['security']['proxy'] or data['security']['tor'] or data['security']['relay']==True:
        return redirect('proxy_warning_view')
    code=str(kwargs.get('ref_code'))
    try:
        profile=Profile.objects.get(code=code)
        request.session['ref_profile']=profile.id
        print('id',profile.id)
    except:
        pass
    print(request.session.get_expiry_age())
    return render(request,'index.html',{'data':data})
def signup(request):
    client_ip, _ = get_client_ip(request)
     
    print(client_ip)
     # Replace YOUR_TOKEN with your actual IPinfo API token
    api_url = 'https://vpnapi.io/api/{}?key=2290f864fc4c4f2e8d9d2fc4f8a75938'.format(client_ip)
    # Make a request to IPinfo API
    response = requests.get(api_url)
    data = response.json()
    print(data)
    # Check if the IP is associated with a VPN or proxy
    if  data['security']['vpn']or data['security']['proxy'] or data['security']['tor'] or data['security']['relay']==True:
        return redirect('proxy_warning_view')

    profile_id=request.session.get('ref_profile')
    print('id', profile_id)
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            if profile_id is not None:
                recommended_by_profile=Profile.objects.get(id=profile_id)
                instance=form.save()
                register_user=User.objects.get(id=instance.id)
                register_profile=Profile.objects.get(user=register_user)
                register_profile.recommended_by=recommended_by_profile.user
                register_profile.save()
            
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            return redirect('/')
            
          
    else:
        form = SignUpForm()
        print('error')

    return render(request, 'signup.html', {'form': form})

 
