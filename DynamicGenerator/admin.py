# Import necessary modules
from django.contrib import admin
from .models import Advertising, Category,Oursites,SitePurchase,Profile,Portfolio ,Withdrawl_Request,Rating,Deploye,DeployeRate,Contact # Import specific models from your models module
class PurchasedInline(admin.TabularInline):
    model = SitePurchase
    extra = 0 
class WithdrawlInline(admin.TabularInline):
    model = Withdrawl_Request
    extra = 0 
class ProfileAdmin(admin.ModelAdmin):
    inlines = [PurchasedInline,WithdrawlInline]
# Register your models with the admin site
admin.site.register(Advertising)  # Register the Advertising model
admin.site.register(Category)  # Register the Category model
admin.site.register(Oursites)
admin.site.register(SitePurchase)
admin.site.register(Profile,ProfileAdmin)
admin.site.register(Portfolio)
admin.site.register(Withdrawl_Request)
admin.site.register(Rating)
admin.site.register(Deploye)
admin.site.register(DeployeRate)
admin.site.register(Contact)
