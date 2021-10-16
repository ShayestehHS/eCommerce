def get_client_ip(req):
    x_forward_for = req.META.get('HTTP_X_FORWARDED_FOR')
    if x_forward_for:
        ip = x_forward_for.split(',')
    else:
        ip = req.META.get('REMOTE_ADDR')
    return ip
