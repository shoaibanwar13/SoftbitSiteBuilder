import requests
from ipware import get_client_ip

def proxy_checker(request):
    # Get the client's IP address
    client_ip, _ = get_client_ip(request)
    
    # For testing purposes, manually setting the client's IP address
    

    # Construct the API URL with the client's IP address
    api_url = 'https://vpnapi.io/api/{}?key=2290f864fc4c4f2e8d9d2fc4f8a75938'.format(client_ip)

    # Make a request to the VPNAPI.io API
    response = requests.get(api_url)
    data = response.json()
    print(data)

    # Check if the IP is associated with a VPN, proxy, Tor, or relay network
    if data['security']['vpn'] or data['security']['proxy'] or data['security']['tor'] or data['security']['relay']:
        return True  # The IP is associated with a VPN, proxy, Tor, or relay
    else:
        return False  # The IP is not associated with a VPN, proxy, Tor, or relay
