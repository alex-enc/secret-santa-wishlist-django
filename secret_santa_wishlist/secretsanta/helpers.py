from django.urls import reverse
from django.conf import settings
from django.shortcuts import redirect

def login_prohibited(view_function):
    def modified_view_function(request):
        if request.user.is_authenticated:
            #redirect
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        else:
            #execute  view_function
            return view_function(request)
    return modified_view_function

def reverse_with_next(url_name, next_url):
    url = reverse(url_name)
    url += f"?next={next_url}"
    return url

class LogInTester:
    def _is_logged_in(self):
        return '_auth_user_id' in self.client.session.keys()