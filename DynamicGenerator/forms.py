from django import forms
from .models import SitePurchase
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile,Portfolio,Advertising,Rating,Deploye
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username','first_name','last_name']
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profilepic','profession','bio','profilepic','phone','address','city','state','country','facebook','skype','linkedin','twitter']
 
class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=50, required=True)
    class Meta:
        model = User
        fields = ['username','first_name','password1','password2' ]
class  Portfoliotemplate(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['Name', 'Profile_Image', 'Logo', 'Profession', 'Skill', 'Short_Intro',
                  'About_Profession', 'Cover_Image', 'First_Service', 'First_Service_Description',
                  'Second_Service', 'Second_Service_Description', 'Third_Service', 'Third_Service_Description',
                  'Fourth_Service', 'Fourth_Service_Description', 'First_Project_Name', 'First_Project_Description',
                  'First_Project_Image', 'First_Project_Url', 'First_Project_Skill_OR_Framework_Use',
                  'Second_Project_Name', 'Second_Project_Description', 'Second_Project_Image', 'Second_Project_Url',
                  'Second_Project_Skill_OR_Framework_Use', 'Third_Project_Name', 'Third_Project_Description',
                  'Third_Project_Image', 'Third_Project_Url', 'Third_Project_Skill_OR_Framework_Use',
                  'Your_Slogan', 'About_Work_History', 'Total_Number_Of_Projects', 'Total_Clients', 'Experience',
                  'Awards', 'First_Client_Quote', 'First_Client_Name', 'First_Client_Position', 'First_Clent_Image',
                  'Second_Client_Quote', 'Second_Client_Name', 'Second_Client_Position', 'Second_Clent_Image',
                  'Third_Client_Quote', 'Third_Client_Name', 'Third_Client_Position', 'Third_Clent_Image',
                  'Whats_App_Number', 'email', 'Contact_Description', 'facebook_link', 'youtube_link', 'instagram_link',
                  'linkedin_link']
class  UpdatePortfoliotemplate(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['Name', 'Profile_Image', 'Logo', 'Profession', 'Skill', 'Short_Intro',
                  'About_Profession', 'Cover_Image', 'First_Service', 'First_Service_Description',
                  'Second_Service', 'Second_Service_Description', 'Third_Service', 'Third_Service_Description',
                  'Fourth_Service', 'Fourth_Service_Description', 'First_Project_Name', 'First_Project_Description',
                  'First_Project_Image', 'First_Project_Url', 'First_Project_Skill_OR_Framework_Use',
                  'Second_Project_Name', 'Second_Project_Description', 'Second_Project_Image', 'Second_Project_Url',
                  'Second_Project_Skill_OR_Framework_Use', 'Third_Project_Name', 'Third_Project_Description',
                  'Third_Project_Image', 'Third_Project_Url', 'Third_Project_Skill_OR_Framework_Use',
                  'Your_Slogan', 'About_Work_History', 'Total_Number_Of_Projects', 'Total_Clients', 'Experience',
                  'Awards', 'First_Client_Quote', 'First_Client_Name', 'First_Client_Position', 'First_Clent_Image',
                  'Second_Client_Quote', 'Second_Client_Name', 'Second_Client_Position', 'Second_Clent_Image',
                  'Third_Client_Quote', 'Third_Client_Name', 'Third_Client_Position', 'Third_Clent_Image',
                  'Whats_App_Number', 'email', 'Contact_Description', 'facebook_link', 'youtube_link', 'instagram_link',
                  'linkedin_link']

class  Advertisingtem(forms.ModelForm):
    class Meta:
        model = Advertising
        fields = ['Companyname', 'logo', 'slogan_title', 'short_Discription', 'image1', 'image2', 'image3',
                  'short_about_us', 'brand_strategy', 'product_experience', 'time_management', 'beautiful_design',
                  'short_about_us2', 'about_us_description', 'pic1', 'pic2', 'title_service1', 'description_title_service1',
                  'title_service2', 'description_title_service2', 'title_service3', 'description_title_service3', 'slogan',
                  'cover_pic', 'description', 'video_url', 'youtube_video_id', 'title_1', 'pic_1', 'description_1',
                  'title_2', 'pic_2', 'description_2', 'title_3', 'pic_3', 'description_3', 'title_4', 'pic_4',
                  'description_4', 'location', 'email', 'whatsapp_number', 'facebook_link', 'youtube_link',
                  'instagram_link']

class  UpdateAdvertisingtem(forms.ModelForm):
    class Meta:
        model = Advertising
        fields = ['Companyname', 'logo', 'slogan_title', 'short_Discription', 'image1', 'image2', 'image3',
                  'short_about_us', 'brand_strategy', 'product_experience', 'time_management', 'beautiful_design',
                  'short_about_us2', 'about_us_description', 'pic1', 'pic2', 'title_service1', 'description_title_service1',
                  'title_service2', 'description_title_service2', 'title_service3', 'description_title_service3', 'slogan',
                  'cover_pic', 'description', 'video_url', 'youtube_video_id', 'title_1', 'pic_1', 'description_1',
                  'title_2', 'pic_2', 'description_2', 'title_3', 'pic_3', 'description_3', 'title_4', 'pic_4',
                  'description_4', 'location', 'email', 'whatsapp_number', 'facebook_link', 'youtube_link',
                  'instagram_link']
        


         


class SitePurchaseForm(forms.ModelForm):
    class Meta:
        model = SitePurchase
        fields = ['user', 'category', 'name',  'paid', 'paid_amount']
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']
class DeployesiteForm(forms.ModelForm):
    class Meta:
        model = Deploye
        fields = ['sitefile']