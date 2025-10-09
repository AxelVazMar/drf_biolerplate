def get_client_ip(request):
    x_fordarwared_for = request.META.get('HTTP_X_FORWARED_FOR')
    if x_fordarwared_for:
        ip = x_fordarwared_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    return ip