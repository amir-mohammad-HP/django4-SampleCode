# accounts actions customizing

customizing all the actions and feature Django builtin auth url let us do and add more.

## start project

assume you already know how to start a projects and familiar with Django

```bash
$ django-admin startproject accounts_actions .
$ python3 manage.py startapp accounts

```

```python
# ./accounts_actions/settings.py
INSTALLED_APPS = [
    ...,
    "accounts.apps.AccountsConfig",
]

```

## First approach 

in this approach you have less control to customize your backend process

### configure accounts URLs (login, logout, ...)


to get configure this URLs in to our projects, we should include the in the "./accounts_actions/urls.py" but we include them in a standalone app for more integration .

```python
# ./accounts_actions/urls.py :
urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include("accounts.urls")),
    ...,
]


# ./accounts/urls.py :
urlpatterns = [
    path("", include("django.contrib.auth.urls")),
]
```


now if check the "/accounts/login/" you will get "TemplateDoesNotExist at /accounts/login/" error because you hadn't defined any template for login.

the URL pattern defined by django.auth :
```python

accounts/ login/ [name='login']
accounts/ logout/ [name='logout']
accounts/ password_change/ [name='password_change']
accounts/ password_change/done/ [name='password_change_done']
accounts/ password_reset/ [name='password_reset']
accounts/ password_reset/done/ [name='password_reset_done']
accounts/ reset/<uidb64>/<token>/ [name='password_reset_confirm']
accounts/ reset/done/ [name='password_reset_complete'] 

```

### build and define views for URLs 

for make a custom template for each of these URLs :
create "./accounts/registration/"
then for each URL as they named above name them i.e login.html

```html
<!-- ./accounts/registration/login.html -->
<!DOCTYPE html>
<html>
    <head>
    </head>

    <body>
        {{ form.as_p }}
        <button type='submit' value='submit'>Submit</button>
    </body>
</html>
```

## second approach ( more customizable )
in this method you define arbitrary URLs that you need and make view and URLs pattern by your self:

first let's create our views :

```python
./accounts/views.py
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    # authentication_form = None
    template_name = "accounts/login.html" # here we changed the template name default to a new path 
    # redirect_authenticated_user = False

# ./accounts/urls.py
from django.urls import path, include
from accounts.views import CustomLoginView

app_name = 'accounts'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name = 'login'), # should be above to be overwritten
    path("", include("django.contrib.auth.urls")),
]
```

also if you doesn't need to do overwrite any method but only attributes you can 

```python
./accounts/urls.py
from django.contrib.auth.view import LoginView

urlpatterns = [
    path('login/', LoginView.as_view(template_name = "accounts/login.html"), name = 'login'), 
]

```

well done , now you've overwrite the builtin Django login view 

you are able to do this for other auth views as well; please check the [ documentation ](https://docs.djangoproject.com/en/4.1/topics/auth/default/#module-django.contrib.auth.views)



# good to know
we patterned our URLs to **/accounts/login**  but may the login URL in your project were different and you suppose to define for each views that where your login page is.

but you can make it simple and just configure this in the project setting

```python 
#./accounts_actions/settings.py
LOGIN_URL = '/accounts/login/' 
```
this is the default and you don't need to redefine it unless you want to change the URL

also there is more useful settings you may want to check [ documentation ](https://docs.djangoproject.com/en/4.1/ref/settings/#authentication-backends)
