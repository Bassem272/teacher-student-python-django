
from django.contrib.auth.decorators import login_required, permission_required, staff_member_required
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.utils.decorators import method_decorator
from django.dispatch import receiver

from authentication.user_model import User

# 1. @login_required: Ensures that the user is authenticated before accessing the view.
@login_required
def protected_view(request):
    # Your view logic here
    pass

# 2. @permission_required: Restricts access to users with specific permissions.
@permission_required('auth.add_user')
def restricted_view(request):
    # Your view logic here
    pass

# 3. @staff_member_required: Allows access only to staff members.
@staff_member_required
def staff_only_view(request):
    # Your view logic here
    pass

# 4. @csrf_exempt: Exempts the view from CSRF protection.
@csrf_exempt
def csrf_exempt_view(request):
    # Your view logic here
    pass

# 5. @cache_control: Sets cache-related HTTP headers.
@cache_control(max_age=3600)
def cached_view(request):
    # Your view logic here
    pass

# 6. @require_http_methods: Specifies allowed HTTP methods for a view.
@require_http_methods(["GET", "POST"])
def allowed_methods_view(request):
    # Your view logic here
    pass

# 7. @transaction.atomic: Wraps the view in a database transaction.
@transaction.atomic
def transactional_view(request):
    # Your view logic here
    pass

# 8. @method_decorator: Applies a function-based decorator to a class-based view method.
class MyView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

# 9. @receiver: Registers a signal handler function.
from django.db.models.signals import post_save

@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
        # Perform actions when a new user is created
        pass

from rest_framework.decorators import api_view
from rest_framework.response import Response

# This view is decorated as an API view explicitly
@api_view(['GET'])
def api_view_function(request):
    return Response({'message': 'This is an API view'})

# This view is not an API view unless explicitly decorated with @api_view
def regular_function(request):
    return Response({'message': 'This is a regular view'})
