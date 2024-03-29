from django.shortcuts import redirect

class ProxyCheckMiddleware:
    PROXY_HEADERS = (
        'HTTP_X_FORWARDED_FOR',
        'HTTP_VIA',
        'HTTP_PROXY_CONNECTION',
        'HTTP_X_PROXY_ID',
        'HTTP_PROXY_CONNECTION',
        'HTTP_X_FORWARDED_FOR',
        'HTTP_CLIENT_IP',
        'HTTP_FORWARDED_FOR',
        'HTTP_FORWARDED',
        'HTTP_X_CLUSTER_CLIENT_IP',
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        for header in self.PROXY_HEADERS:
            if request.META.get(header):
                # User might be accessing through a proxy or VPN, redirect them
                return redirect('proxy_warning')  # Redirect to a view that displays a message for these users

        response = self.get_response(request)
        return response
