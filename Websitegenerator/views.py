from django.shortcuts import render,redirect
from DynamicGenerator.forms import SignUpForm 
from DynamicGenerator.models import Profile,Testimonial
from django.contrib.auth.models import User
from DynamicGenerator.proxydetector import proxy_checker
from DynamicGenerator.useractivity import track_user_activity
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
 
 
# Define the chat_with_bot function with the responses dictionary
def chat_with_bot(user_input):
    # Dictionary of responses
    responses = responses = {
    "hello": ["Hi there!", "Hello!", "Hey!"],
    "how are you": ["I'm doing well, thank you!", "I'm fine, thanks for asking.", "I'm great!"],
    "goodbye": ["Goodbye!", "See you later!", "Bye!"],
    "what is your name ": ["My Name is Della And I have creation of UE SSL Team!", "My Name is Della and I created for Question Ans For Softbit WebSite Builder","My Name is Della AI Advisor and I gave Ans and Questions Related To Softbit Website Builder"],
    "what is ssl team": ["SSL Team Is a Team Of 4 Group Member In University Of Education Lahore.This is a team of programer that together to makes Web Applications.But SSL Team Lost A Team member Sameer.But SSL Team Have A new team memeber Called Luna Bahi "],
    "I have an advertising company which website i purchase": ["Hi there! Thanks For Question If You have an Advertising Company Then You purchase Asper which is best for advertising and graphic designer here is link please click or copy this link to purchase this site.Because Asper have responsive and suit your business http://127.0.0.1:8000/sitedetail/1", "Hello!", "Hey!"],
     
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
    return "I'm sorry, I don't understand that."

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
     
    check=proxy_checker(request)
    if check==True:
        return redirect('proxy_warning_view')
    feedback=Testimonial.objects.all()[:6]
    code=str(kwargs.get('ref_code'))
    try:
        profile=Profile.objects.get(code=code)
        request.session['ref_profile']=profile.id
        print('id',profile.id)
    except:
        pass
    print(request.session.get_expiry_age())
    return render(request,'index.html',{'feedback':feedback})
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
            'domain':'https://softbit-website-builder.onrender.com/', 
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

 
