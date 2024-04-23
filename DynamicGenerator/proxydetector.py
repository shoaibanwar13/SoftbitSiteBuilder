
import requests
from ipware import get_client_ip
 

    


def proxy_checker(request):
    client_ip, _ = get_client_ip(request)
     
    
    # Replace 'YOUR_TOKEN' with your actual VPNAPI.io token
    api_url = 'https://vpnapi.io/api/{}?key=2290f864fc4c4f2e8d9d2fc4f8a75938'.format(client_ip)

    # Make a request to VPNAPI.io
    response = requests.get(api_url)
    data = response.json()
    print(data)

    # Check if the IP is associated with a VPN, proxy, or Tor network
    if data['security']['vpn'] or data['security']['proxy'] or data['security']['tor'] or data['security']['relay']:
        return True  # The IP is associated with a VPN, proxy, or Tor
    else:
        return False  