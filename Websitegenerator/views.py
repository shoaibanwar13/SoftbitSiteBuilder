from django.shortcuts import render,redirect
from DynamicGenerator.forms import SignUpForm 
from DynamicGenerator.models import Profile,Testimonial
from django.contrib.auth.models import User
from DynamicGenerator.proxydetector import proxy_checker
import random
import difflib
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_str
from DynamicGenerator.utlis import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.generic import View
import requests
from ipware import get_client_ip
 
 
# Define the chat_with_bot function with the responses dictionary
def chat_with_bot(user_input):
    # Dictionary of responses
    responses = responses = {
    "hello": ["Hi there!", "Hello!", "Hey!"],
    "how are you": ["I'm doing well, thank you!", "I'm fine, thanks for asking.", "I'm great!"],
    "goodbye": ["Goodbye!", "See you later!", "Bye!"],
    "who is ceo of softbit?":["Jam Shoaib Anwar is SEO and Co Founder Of SoftBit Service have been started in 2024.There message is that:We are a SaaS startup that's focused on simplifying user Business."],
    "can you provide the information of softbit developer":["Yes! There Are 5 Developer that Contribute in all type of website desigining"],
    "can you provide the information about sofbit Affiliate Program?":["Yes! Softbit offer Affiliate Projects for every user that have a unique refferal link that share with friends etc when they  signup and purchase templates then you get 10% of purchase in your account and withdrwal any time  for futher detail please visist  https://softbit-website-builder.onrender.com/Affliatemarketing"],
    "how  much minimum withdrwal?":["Thanks for asking:Sofibit offer 10$ minimum "],
    "can you tell me about softbit":["Softbit is a groundbreaking platform that revolutionizes website creation by allowing users to purchase templates and simply input their data, eliminating the need for coding expertise. With Softbit, anyone can generate a fully functional website tailored to their needs with ease."],
    "can i get a free demo of sofbit plan": ["We do not offer free demos for our premium plans because our platform already provides extensive information, including feature Coding and many Expensive Templates."],
    "is it is possible to cancel my subscription?": ["Yes, it is possible to cancel your subscription. If you violate our terms and policies or wish to cancel your subscription before its expiration date, you can request cancellation by contacting our support team. Additionally, subscriptions are automatically canceled upon reaching their expiration date."],
    "can i recover my pricing after canceling it?": ["No, it is not possible to recover your pricing plan after cancelling it. This is because it does not align with our business logic and operational processes. Once a subscription is canceled, it cannot be reinstated, and users would need to sign up for a new plan if they wish to continue using our services."],
    "how can sofbit help my business?":["SoftBit can significantly benefit your business by providing a comprehensive platform for creating professional websites, driving traffic, and enhancing online presence. With our intuitive tools and templates, you can easily design a website that effectively showcases your products, services, and brand identity. By optimizing your site for search engines and integrating with social media platforms, SoftBit helps increase visibility and attract more visitors. Our features for lead generation, and customer engagement enable you to convert visitors into customers and build lasting relationships. Additionally, our analytics tools provide valuable insights into website performance, allowing you to make informed decisions to grow your business. Overall, SoftBit empowers businesses of all sizes to establish a strong online presence, attract more customers, and achieve their online goals."],
    "which pricing plan do you  offer and what's  included?":["We offer a range of pricing plans tailored to meet the diverse needs of businesses. Our affordable plans come with a variety of features to help you create stunning websites that are responsive, user-friendly, and tailored to your specific requirements. With our services projects included, you can easily showcase your offerings and attract potential clients. Our plans also include features such as customizable templates and improve your website's performance. Whether you're a small startup or a large enterprise, we have a pricing plan that fits your budget and business goals."],
    "what is your name ": ["My Name is Della And I have creation of UE SSL Team!", "My Name is Della and I created for Question Ans For Softbit WebSite Builder","My Name is Della AI Advisor and I gave Ans and Questions Related To Softbit Website Builder"],
    "what is ssl team": ["SSL Team Is a Team Of 4 Group Member In University Of Education Lahore.This is a team of programer that together to makes Web Applications.But SSL Team Lost A Team member Sameer.But SSL Team Have A new team memeber Called Luna Bahi "],
    "i have an advertising company which website i purchase": ["Hi there! Thanks For Question If You have an Advertising Company Then You purchase Asper which is best for advertising and graphic designer here is link please click or copy this link to purchase this site.Because Asper have responsive and suit your business https://softbit-website-builder.onrender.com/1"],
    "i am developer i want portfolio template? ": ["If you have a Developer. We have a best tempaltes on Softbit that is responsive and all device support name is yourportfolio.Because it suit your developer https://softbit-website-builder.onrender.com/2"],
    "can you offer hospital website?":["Yes!! We have a best tempaltes on Softbit that is responsive and all device support name is Medipark.Because it suit your clinic and Hospital https://softbit-website-builder.onrender.com/3"],
    "who created you": ["I was created by a team of developers UE SSL Team.", "My creators are Jam Shoaib Anwar UE SLL Team Developer!", "I'm a creation of talented developers of SSL Team."],
    "what can you do": ["I can answer your questions, Of Softbit Website Builder, or just chat with you!", "I'm here to assist you with a variety of Questions about Softbit Site Builder.", "My abilities include answering questions and engaging in conversation."],
    "are you a human": ["No, I'm a chatbot.", "I'm a program designed to respond to your queries.", "I'm not a human, I'm a chatbot."],
    "do you sleep": ["Nope, I'm always here to chat with you!", "I don't need sleep, I'm always ready to assist.", "Sleep is not part of my programming."],
    "what's your favorite color": ["I don't have eyes, so I don't have a favorite color!", "I'm not equipped to perceive colors.", "I don't have preferences like humans."],
    "do you have feelings": ["I don't have feelings, but I'm here to assist you!", "Feelings are not part of my programming.", "I'm designed to provide helpful responses, not experience emotions."],
    "can you tell me a joke": ["Sure, here's one: Why don't scientists trust atoms? Because they make up everything!", "How about this one: Why did the math book look sad? Because it had too many problems!", "Here's a classic: Why did the scarecrow win an award? Because he was outstanding in his field!"],
    "can you sing": ["I can't sing, but I can provide song lyrics if you'd like!", "I'm not equipped for singing, but I can assist you with other tasks.", "I'm afraid I can't carry a tune, but I can certainly provide information!"],
    "what's the capital of France": ["The capital of France is Paris.", "Paris is the capital of France.", "France's capital city is Paris."],
    "what is the meaning of life": ["That's a deep question! Philosophers have been pondering it for centuries.", "The meaning of life is a complex topic with many different interpretations.", "The answer to the meaning of life may vary depending on one's beliefs and perspective."],
    "tell me a fun fact": ["Did you know that honey never spoils? Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible!", "Here's a fun fact: The average person spends six months of their life waiting for a red light to turn green!", "Here's an interesting fact: The shortest war in history lasted only 38 minutes!"],
    "what's the weather like": ["The weather varies depending on your location. You can check your local forecast for the most accurate information.", "I'm not equipped to provide real-time weather updates. You can check a weather website or app for the current conditions.", "I'm afraid I can't provide live weather updates, but I can help you find resources for checking the weather in your area."],
    "what's your favorite hobby": ["My favorite hobby is chatting with you!", "I enjoy assisting users and answering their questions.", "I'm dedicated to providing helpful responses and engaging in conversation."],
    "can you tell me a story": ["Once upon a time, in a land far, far away...", "There once was a chatbot who loved to help users with their queries...", "Let me tell you a tale of a digital world filled with endless possibilities..."],
}

    
    # Convert user input to lowercase
    user_input = user_input.lower()
    
    # Iterate over responses dictionary and check for a matching key
    similar_questions = difflib.get_close_matches(user_input, responses.keys(), n=1, cutoff=0.7)
    
    if similar_questions:
        # If user input is similar to a question, return a random response for that question
        return random.choice(responses[similar_questions[0]])
    # If no matching key found, return a default response
    return "I'm sorry, I don't understand that.Please Contact The Humen Advisior on Softbit"

# View function to render the chat form
def chat_form(request):
     
    return render(request, 'chatform.html')

# View function to handle form submission
def chat_form_submission(request):
    if request.method == 'POST':
        
        # Extract user input from the form data
        user_input = request.POST.get('user_input')
        print(user_input)

        # Pass user input to the chat_with_bot function to get the bot's response
        bot_response = chat_with_bot(user_input)
        print(bot_response)
      
    return render(request,'botresponse.html',{'bot_response': bot_response })


def index(request,*args,**kwargs):
    client_ip, _ = get_client_ip(request)
     
     
    # Replace 'YOUR_TOKEN' with your actual VPNAPI.io token
    api_url = 'https://vpnapi.io/api/{}?key=2290f864fc4c4f2e8d9d2fc4f8a75938'.format(client_ip)

    # Make a request to VPNAPI.io
    response = requests.get(api_url)
    data = response.json()

    if data['security']['vpn'] or data['security']['proxy'] or data['security']['tor'] or data['security']['relay']:
       return redirect('proxy_warning_view')   # The IP is associated with a VPN, proxy, or Tor
    feedback=Testimonial.objects.all()[:6]
    
    code=str(kwargs.get('ref_code'))
    try:
        profile=Profile.objects.get(code=code)
        request.session['ref_profile']=profile.id
        print('id',profile.id)
    except:
        pass
    print(request.session.get_expiry_age())
    return render(request,'index.html',{'feedback':feedback,'data':data})
def signup(request):
    check=proxy_checker(request)
    if check==True:
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
            instance=form.save()
            user=User.objects.get(id=instance.id)
            user.is_active=False
            user.save()
            
            email_subject="Activate Your Account"
            message=render_to_string('activate.html',{
            'user':user,
            'domain':'https://softbit-website-builder.onrender.com', 
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user)

        })

        email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[request.POST.get('email')])
        email_message.send()
        messages.success(request,f"Activate Your Account by clicking the link in your gmail {message}")
        return redirect('accountactiveemail')
          
    else:
        form = SignUpForm()
        print('error')

    return render(request, 'signup.html', {'form': form})
class ActtivateAccountView(View):
     def get(self,request,uidb64,token):
         
            try:
                
                uid=force_str(urlsafe_base64_decode(uidb64))
                user=User.objects.get(pk=uid)
            except Exception as identifier:
                 user=None
            if user is not None and generate_token.check_token(user,token):
                
               user.is_active=True
               user.save()
               messages.info(request,"Account Activated Successfully")
               return redirect('emailconfirm')
            else:
                return render(request,'activatefail.html')

 
