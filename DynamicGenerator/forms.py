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
        fields = ['username','email','first_name','password1','password2' ]
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
        
from django import forms
from .models import Hospital

class HospitalForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = [
            'name',
            'Logo',
            'Slogan',
            'Short_Intro',
            'Doctors',
            'Patient_Beds',
            'Health_Programs',
            'Whats_App_Number',
            'Video',
            'Service_Slogan',
            'Detail_About_Service',
            'General_Care_Image',
            'General_Care_Info',
            'Pediatric_Care_Image',
            'Pediatric_Care_Info',
            'Neurology_Image',
            'Neurology_Info',
            'Womens_Health_Image',
            'Womens_Health_Service_Info',
            'Emergency_Care_Image',
            'Emergency_Care_Info',
            'Laboratory_Image',
            'Laboratory_Info',
            'About_Treatments',
            'First_Pediatrics_Doctor_Image',
            'First_Pediatrics_Doctor_Name',
            'First_Pediatrics_Doctor_Expertise',
            'Second_Pediatrics_Doctor_Image',
            'Second_Pediatrics_Doctor_Name',
            'Second_Pediatrics_Doctor_Expertise',
            'Neurology_Doctor_Image',
            'Neurology_Doctor_Name',
            'Neurology_Doctor_Expertise',
            'Advanced_Diagnostic_Doctor_Image',
            'Advanced_Diagnostic_Doctor_Name',
            'Advanced_Diagnostic_Doctor_Expertise',
            'Rapid_Response_Experts_Doctor_Image',
            'Rapid_Response_Experts_Doctor_Name',
            'Rapid_Response_Experts_Doctor_Expertise',
            'Hospital_Image',
            'Hospital_Address',
            'Laboratory_Name',
            'Monday_to_Friday',
            'Saturday_Timing',
            'Sunday_Timing',
            'Laboratory_Address',
            'Patient_Image',
            'Doctor_Image',
            'Question1_Accept_Insurance_Policy',
            'Question2_Is_Emergency_Unit_Available',
            'Question3_Provide_Telehealth_Health',
            'Email',
            'Youtube',
            'Facebook',
            'LinkedIn',
        ]

class HospitalEditForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = HospitalForm.Meta.fields  # Use the same fields as the creation form



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
 

 
