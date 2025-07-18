from functools import wraps

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse


def group_required(group_names=None, access_denied_view='coach_appointment_site:access_denied'):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                # not connected
                return redirect(reverse(access_denied_view, kwargs={'required_role': 'authenticated user'}))
            if group_names:
                if not request.user.groups.filter(name__in=group_names).exists():
                    required_role = " or ".join(group_names)
                    # not in the right group
                    return redirect(reverse(access_denied_view, kwargs={'required_role': required_role}))
            # has rights
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator