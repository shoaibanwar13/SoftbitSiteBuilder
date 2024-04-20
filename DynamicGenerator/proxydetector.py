
import requests
from ipware import get_client_ip
from .models import UserMonitering
def track_user_activity(request):
    client_ip, _ = get_client_ip(request)
     
    client_ip='182.185.199.193'
    # Replace 'YOUR_TOKEN' with your actual VPNAPI.io token
    api_url = 'https://vpnapi.io/api/{}?key=2290f864fc4c4f2e8d9d2fc4f8a75938'.format(client_ip)

    # Make a request to VPNAPI.io
    response = requests.get(api_url)
    data = response.json()
    
    if not UserMonitering.objects.filter(ip_address=client_ip).exists():
                # If not present, store the login history
       data=UserMonitering(user=request.user, ip_address=client_ip, country=data['location']['country'], city=data['location']['city'],restricted=False)
       data.save()
    check_ristricted=UserMonitering.objects.filter(user=request.user,restricted=True).last()
    if check_ristricted:
        return True
    last_login = UserMonitering.objects.filter(user=request.user).last()
    if last_login and data['location']['country'] != last_login.country:
        data=UserMonitering(user=request.user, ip_address=client_ip, country=data['location']['country'], city=data['location']['city'],restricted=True)
        data.save()
    if last_login and data['location']['country'] != last_login.country:
        
        return  True
    
    print(last_login)

    if last_login and data['location']['country'] != last_login.country:
        data=UserMonitering(user=request.user, ip_address=client_ip, country=data['location']['country'], city=data['location']['city'],restricted=True)
        data.save()
    if last_login and data['location']['country'] != last_login.country:
        
        return  True
    else:
        return False

    


def proxy_checker(request):
    client_ip, _ = get_client_ip(request)
     
    client_ip='182.185.199.193'
    # Replace 'YOUR_TOKEN' with your actual VPNAPI.io token
    api_url = 'https://vpnapi.io/api/{}?key=2290f864fc4c4f2e8d9d2fc4f8a75938'.format(client_ip)

    # Make a request to VPNAPI.io
    response = requests.get(api_url)
    data = response.json()

    # Check if the IP is associated with a VPN, proxy, or Tor network
    if data['security']['vpn'] or data['security']['proxy'] or data['security']['tor'] or data['security']['relay']:
        return True  # The IP is associated with a VPN, proxy, or Tor
    else:
        return False  