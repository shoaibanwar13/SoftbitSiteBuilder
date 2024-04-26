# Import necessary modules
import requests  # For making HTTP requests
from ipware import get_client_ip  # For retrieving client IP address
from .models import UserMonitering  # Import the UserMonitering model

# Function to track user activity
def track_user_activity(request):
    # Retrieve client IP address
    client_ip, _ = get_client_ip(request)
    # For testing purposes, set a fixed IP address (replace with actual client IP retrieval in production)
     
     
    # VPNAPI.io API URL with client IP and API key
    api_url = 'https://vpnapi.io/api/{}?key=2290f864fc4c4f2e8d9d2fc4f8a75938'.format(client_ip)

    # Make a request to VPNAPI.io
    response = requests.get(api_url)
    data = response.json()
    
    # Check if the user's IP address exists in the UserMonitering table
    if not UserMonitering.objects.filter(ip_address=client_ip).exists():
        # If not present, store the login history
        data = UserMonitering(user=request.user, ip_address=client_ip, country=data['location']['country'], city=data['location']['city'], restricted=False)
        data.save()
    
    # Check if the user is restricted
    check_restricted = UserMonitering.objects.filter(user=request.user, restricted=True).last()
    if check_restricted:
        return True
    
    # Retrieve the last login record
    last_login = UserMonitering.objects.filter(user=request.user).last()
    
    # If last login record exists and country has changed, update the record and mark as restricted
    if last_login and data['location']['country'] != last_login.country:
        data = UserMonitering(user=request.user, ip_address=client_ip, country=data['location']['country'], city=data['location']['city'], restricted=True)
        data.save()
        return True
    
    # If last login record exists and country has not changed, check for previous restriction
    if last_login and data['location']['country'] != last_login.country:
        return True
    
    # If no previous restrictions or country changes, return False
    return False
