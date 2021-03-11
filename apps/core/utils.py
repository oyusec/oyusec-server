def is_admin(request):
    if not request.user.is_authenticated or not request.user.user_type == 'admin':
        return False

    return True