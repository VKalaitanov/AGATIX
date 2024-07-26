from platform_main.models import Campaign


def global_settings(request):
    if request.user.is_authenticated:
        if request.user.is_admin or request.user.is_superuser:
            len_waiting = len(Campaign.objects.filter(next_status__isnull=False))
        elif request.user.is_manager:
            len_waiting = len(Campaign.objects.filter(next_status__isnull=False, user__manager=request.user))
        else:
            len_waiting = ''
    else:
        len_waiting = ''
    return {
        'len_waiting': len_waiting,
    }
