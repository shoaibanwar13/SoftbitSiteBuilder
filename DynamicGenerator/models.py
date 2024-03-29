
from django.db import models
from django.contrib.auth.models import User
from .utlis import generate_ref_code
from django.utils import timezone
class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    code=models.CharField(max_length=5,blank=True)
    recommended_by=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="ref_by")
    profession=models.CharField(max_length=200,null=True)
    bio=models.TextField(null=True)
    profilepic=models.ImageField(upload_to='profilepic/', null=True)
    created=models.DateTimeField(auto_now=True)
    balance=models.IntegerField(default=0)
    withdrawl_amount=models.IntegerField(default=0)
    commession=models.IntegerField(default=0)
    phone=models.CharField(max_length=200,null=True)
    address=models.CharField(max_length=200,null=True)
    city=models.CharField(max_length=200,null=True)
    state=models.CharField(max_length=200,null=True)
    country=models.CharField(max_length=200,null=True)
    facebook = models.URLField(blank=True, null=True)   
    skype= models.URLField(blank=True, null=True)   
    twitter = models.URLField(blank=True, null=True)   
    linkedin = models.URLField(blank=True, null=True)

    def __str__(self) :

        return  f"{self.user.username}-{self.code}"
    def get_recommended_profile(self):
        query=Profile.objects.all()
        my_recs=[]
        for profile in query:
            if profile.recommended_by==self.user:
                my_recs.append(profile)
        return my_recs
    
    def save(self, *args, **kwargs):
        if self.code=="":
            code=generate_ref_code()
            self.code=code
        super().save(*args, **kwargs)
 

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name

class Advertising(models.Model):
    #User info
    user = models.ForeignKey(User, related_name='purchase', blank=True, null=True, on_delete=models.CASCADE)
    
    Companyname = models.CharField(max_length=255,null=True,) #Company Name
    logo = models.ImageField(upload_to='logos/')  # Logo image
    slogan_title = models.CharField(max_length=255,null=True,)  # Brand slogan
   
    short_Discription = models.CharField(max_length=255, null=True)
    image1 = models.ImageField(upload_to='Advertising/')  # Image 1 for advertising
    image2 = models.ImageField(upload_to='Advertising/')  # Image 2 for advertising
    image3 = models.ImageField(upload_to='Advertising/')  # Image 3 for advertising
    short_about_us = models.TextField()  # Short about us description
    brand_strategy = models.TextField()  # Brand strategy description
    product_experience = models.TextField()  # Product experience description
    time_management = models.TextField()  # Time management description
    beautiful_design = models.TextField()  # Beautiful design description

    # About Us Section
    short_about_us2 = models.TextField(null=True) # Short about us description (duplicate field)

    # Extended About Us Section
    about_us_description = models.TextField()  # Extended about us description
    pic1 = models.ImageField(upload_to='Advertising/')  # Image 1 for extended about us
    pic2 = models.ImageField(upload_to='Advertising/')  # Image 2 for extended about us

    # Services Section
    title_service1 = models.CharField(max_length=255)  # Title for service 1
    description_title_service1 = models.TextField()  # Description for service 1
    title_service2 = models.CharField(max_length=255)  # Title for service 2
    description_title_service2 = models.TextField()  # Description for service 2
    title_service3 = models.CharField(max_length=255)  # Title for service 3
    description_title_service3 = models.TextField()  # Description for service 3

    # Studio Information
    slogan = models.CharField(max_length=255)  # Studio slogan
    cover_pic = models.ImageField(upload_to='Advertising/')  # Cover picture for studio
    description = models.TextField()  # Studio description
    video_url = models.URLField()  # Video URL for the studio
    youtube_video_id = models.CharField(max_length=255,blank=True, null=True) 

    # Latest Work Section
    title_1 = models.CharField(max_length=255)  # Title for latest work 1
    pic_1 = models.ImageField(upload_to='Advertising/')  # Picture for latest work 1
    description_1 = models.TextField()  # Description for latest work 1
    title_2 = models.CharField(max_length=255)  # Title for latest work 2
    pic_2 = models.ImageField(upload_to='Advertising/')  # Picture for latest work 2
    description_2 = models.TextField()  # Description for latest work 2
    title_3 = models.CharField(max_length=255)  # Title for latest work 3
    pic_3 = models.ImageField(upload_to='Advertising/')  # Picture for latest work 3
    description_3 = models.TextField()  # Description for latest work 3
    title_4 = models.CharField(max_length=255)  # Title for latest work 4
    pic_4 = models.ImageField(upload_to='Advertising/')  # Picture for latest work 4
    description_4 = models.TextField()  # Description for latest work 4

    # Contact Information
    location = models.CharField(max_length=255)  # Location
    email = models.EmailField()  # Email address
    whatsapp_number = models.CharField(max_length=20)  # WhatsApp number

    # Social Media Links
    facebook_link = models.URLField(blank=True, null=True)  # Facebook link
    youtube_link = models.URLField(blank=True, null=True)  # YouTube link
    instagram_link = models.URLField(blank=True, null=True)  # Instagram link

    def __str__(self):
        return self.Companyname

class Portfolio(models.Model):
    #User info
    user = models.ForeignKey(User, related_name='portfolio', blank=True, null=True, on_delete=models.CASCADE)
    
    Name = models.CharField(max_length=255,null=True,) 
    Profile_Image=models.ImageField(upload_to='Portfolio/')
    Logo = models.ImageField(upload_to='logos/')   
    Profession= models.CharField(max_length=255,null=True,)
    Skill= models.CharField(max_length=255,null=True,)
    Short_Intro = models.TextField()
    #About Us Info
    About_Profession= models.CharField(max_length=255,null=True,)
    Cover_Image=models.ImageField(upload_to='CoverImage/')
    #Sercice 
    First_Service = models.CharField(max_length=255,help_text="First Service Name")   
    First_Service_Description  = models.TextField(help_text="First Service Description")
    Second_Service = models.CharField(max_length=255,help_text="Second Service Name")   
    Second_Service_Description  = models.TextField(help_text="Second Service Description")
    Third_Service = models.CharField(max_length=255,help_text="Third Service Description")   
    Third_Service_Description  = models.TextField(help_text="Third Service Name" )
    Fourth_Service = models.CharField(max_length=255,help_text="Fourth Service Name(optional)" )   
    Fourth_Service_Description  = models.TextField(help_text="Fourth Service Description(optional)")
    #Projects 
    First_Project_Name=models.CharField(max_length=255)
    First_Project_Description  = models.TextField()
    First_Project_Image=models.ImageField(upload_to='ProjectImage/')
    First_Project_Url = models.URLField()
    First_Project_Skill_OR_Framework_Use=models.CharField(max_length=255)

    Second_Project_Name=models.CharField(max_length=255)
    Second_Project_Description  = models.TextField()
    Second_Project_Image=models.ImageField(upload_to='ProjectImage/')
    Second_Project_Url = models.URLField()
    Second_Project_Skill_OR_Framework_Use=models.CharField(max_length=255)


    Third_Project_Name=models.CharField(max_length=255)
    Third_Project_Description  = models.TextField()
    Third_Project_Image=models.ImageField(upload_to='ProjectImage/')
    Third_Project_Url = models.URLField()
    Third_Project_Skill_OR_Framework_Use=models.CharField(max_length=255)
    #History
    Your_Slogan=models.CharField(max_length=255,null=True)
    About_Work_History=models.CharField(max_length=500,null=True)
    Total_Number_Of_Projects=models.IntegerField(default=0)
    Total_Clients=models.IntegerField(default=0)
    Experience=models.IntegerField(default=0)
    Awards=models.IntegerField(default=0)
    #Testimonial
    First_Client_Quote = models.TextField()
    First_Client_Name=models.CharField(max_length=255)
    First_Client_Position=models.CharField(max_length=255)
    First_Clent_Image=models.ImageField(upload_to='ClientImage/',help_text="Please Use Small Image That Display In template ")
    Second_Client_Quote = models.TextField()
    Second_Client_Name=models.CharField(max_length=255,null=True)
    Second_Client_Position=models.CharField(max_length=255)
    Second_Clent_Image=models.ImageField(upload_to='ClientImage/',help_text="Please Use Small Image That Display In template ")
    Third_Client_Quote = models.TextField()
    Third_Client_Name=models.CharField(max_length=255)
    Third_Client_Position=models.CharField(max_length=255)
    Third_Clent_Image=models.ImageField(upload_to='ClientImage/',help_text="Please Use Small Image That Display In template ")
    #Contact
    Whats_App_Number=models.CharField(max_length=255)
    email = models.EmailField()
    Contact_Description=models.CharField(max_length=255)
    facebook_link = models.URLField(blank=True, null=True)  # Facebook link
    youtube_link = models.URLField(blank=True, null=True)  # YouTube link
    instagram_link = models.URLField(blank=True, null=True)  # Instagram link
    linkedin_link = models.URLField(blank=True, null=True) #linked in profile link

    def __str__(self):
        return self.Name







class Oursites(models.Model):
    category=models.ForeignKey(Category,related_name='Oursite',blank=True, null=True, on_delete=models.CASCADE)
    name= models.CharField(max_length=255,null=True,)
    developer=models.CharField(max_length=255,null=True,)
    date= models.DateField()
    image1 = models.ImageField(upload_to='Oursite/')
    image2 = models.ImageField(upload_to='Oursite/')
    description1=models.TextField(null=True)
    description2=models.TextField(null=True)
    summery=models.TextField(null=True)
  
    price = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    class Meta:
        verbose_name_plural='SoftBit Sites'
    def get_ratings(self):
        return Rating.objects.filter(item=self)
      
    def __str__(self):
        return self.name
    
class Rating(models.Model):
    product = models.ForeignKey(Oursites, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to logged-in user
    rating = models.PositiveSmallIntegerField(choices=((1, 1), (2, 2), (3, 3), (4, 4), (5, 5)),null=True)
    created_at = models.DateTimeField(default=timezone.now)
    class Meta:
        unique_together = ('product', 'user')  # Prevent duplicate ratings per user/product
     
class SitePurchase(models.Model):
    profile = models.ForeignKey(Profile,blank=True, null=True, on_delete=models.CASCADE)
    user=models.ForeignKey(User,related_name='SitePurchase',blank=True, null=True, on_delete=models.CASCADE)
    category=models.ForeignKey(Category,related_name='SitePurchase',blank=True, null=True, on_delete=models.CASCADE)
    name= models.CharField(max_length=255,null=True,)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
     
    def __str__(self):
        return self.name

class Withdrawl_Request(models.Model):
    PENDING = 'Pending'
    APPROVED = 'Paid'

    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (APPROVED, 'Paid')
    )
    user = models.ForeignKey(User,  blank=True, null=True, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile,blank=True, null=True, on_delete=models.CASCADE)
    pay_method=models.CharField(max_length=30)
    account_no=models.CharField(max_length=50)
    account_title=models.CharField(max_length=50)
    bank=models.CharField(max_length=50,null=True)
    routing_no=models.CharField(max_length=50,null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(default=timezone.now) 
    amount = models.IntegerField(  default=0)
    class Meta:
        verbose_name_plural='Withdraw Request'
        ordering = ('-created_at',)
   

    def __str__(self):
        return self.account_no
class Deploye(models.Model):
    profile = models.ForeignKey(Profile,blank=True, null=True, on_delete=models.CASCADE)
    user=models.ForeignKey(User,related_name='Deploye',blank=True, null=True, on_delete=models.CASCADE)
    name= models.CharField(max_length=255,null=True,)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    domainname=models.CharField(max_length=255,null=True)
    sitefile=models.FileField(upload_to='fordeployesites')
    paid = models.BooleanField(default=False)
    Processing = 'Processing'
    Live = 'Live'
    STATUS_CHOICES = (
        (Processing, 'Processing'),
        (Live, 'Live')
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=Processing)
    def __str__(self):
        return self.name
class DeployeRate(models.Model):
   rate=models.DecimalField(max_digits=10, decimal_places=2,null=True)
class Contact(models.Model):
    name=models.CharField(max_length=50,null=True)
    email=models.EmailField()
    message=models.TextField(max_length=500,null=True)
    phone=models.IntegerField()

    def __int__(self):
        return self.name