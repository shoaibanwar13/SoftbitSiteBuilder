from django.shortcuts import render,redirect

from DynamicGenerator.forms import SignUpForm 
 
from DynamicGenerator.models import Profile
 
from django.contrib.auth.models import User
from django.shortcuts import render ,redirect
 
 
from django.contrib.auth import login
 
from ipware import get_client_ip
import requests
 
    
def index(request,*args,**kwargs):
   
    code=str(kwargs.get('ref_code'))
    try:
        profile=Profile.objects.get(code=code)
        request.session['ref_profile']=profile.id
        print('id',profile.id)
    except:
        pass
    print(request.session.get_expiry_age())
    return render(request,'index.html')
def signup(request):
   

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

 
