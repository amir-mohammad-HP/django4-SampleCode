# Email Authentication System

this project will represent how to create an email authentication system for a django application.

NOTE : presumed that you will start the app by a custom user model(because we rewrite User email) and if you hadn't, make sure each USER use a unique email address.

### Create a project
we call project folder to **email_authetication**
```batch 
django-admin startproject email_authentication .
```
### start app 
let's call the app **authenticate**

```batch 
python3 manage.py startapp authenticate
```
NOTE : do not makemigrations untill we create a custom User model

now add the app to **INSTALLED_APPS** in *./email_authetication/settings.py*

## Built Custom User Model :

let's create a custom User model, it is helpful to always create a User model even if you won't need it at the time.

but now we need to rewite the email_field to make sure we won't get two users with the same email address 

**1-** in *./authenticate/models.py* 
```python
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    email = models.EmailField(
        _("email address"),
        unique=True,
        blank=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
        )
```
**2-** in *./authenticate/admin.py*
```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

admin.site.register(User, UserAdmin)
```
**3-** in *./email_authentication/settings.py* we need to tell django to use our custom User model
```python 
AUTH_USER_MODEL = 'authenticate.User'
```
django will look to *authenticate* app then in *models* look for *User* model.

now ... let's do the first *makemigrations* and *migrate* the changes

```batch
python3 manage.py makemigrations
python3 manage.py migrate
```

congratulations, now we built our custom model ... for making sure we use the right User model, you can have access to User model by the following path:
```python 
# not recommended
from authentication.models import User

# recommended
from django.contrib.auth import get_user_model # a function that return the current user model
from django.conf import settings # get settings.AUTH_USER_MODEL
```
the two recommended ways are kinda the same 

## <p id='built_authentication'> Build Authentication Backend </p>

we need to create a new authentication backend to tell django to also use this backend to authentify users

create a new file and name it *./authenticate/backends.py*
```python
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailAuthentication(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None
        except UserModel.MultipleObjectsReturned:
            return None # in case multiple users with the same email exist none of them will authentify
        else:
            if user.check_password(password):
                return user
        return None
```

in *./email_authentication/settings.py*
```python
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend', # keep username and password authentication
    'authenticate.backends.EmailAuthentication', # add email and password authentication
    ]
```
add django and our custom backends to settings to tell Django use this backend too, then
our email authentication system is complete

now you can authenticate the user in both *username and passsword* or *email and password*

you can also use the same method above to create an authentication backend to authentify with a secure key or etc

e.g
```python
from django.contrib.auth import authenticate

# authenticate username and password
authenticate(request, username = username, password = password)
# authenticate email and password
authenticate(request, email = email, password = password)
```

let's create a superuser and test :
```batch
$ python3 manage.py shell
>>> from django.contrib.auth import authenticate
>>> authenticate(email = 'hamidipour97@gmail.com', password = 'my password')
<User: amir-mohammad-HP>
```
see the user model returned

## *build Authentication Form* <small>( use with Django LoginView )</small>

unfortunately Django hadn't provide a built in email authentication system and so there is no default login by email but we can do the trick by our selves 

we had just built out [custom authentication backend](#built_authentication)  and now we can use it to create our custom email authentication form to use with builtin <u>[django.contrib.auth.views.LoginView](https://docs.djangoproject.com/en/4.1/topics/auth/default/#django.contrib.auth.views.LoginView)</u>

let's create a file and name it *./authenticate/forms.py*
```python
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, get_user_model
from django.utils.text import capfirst
from django.core.exceptions import ValidationError

UserModel = get_user_model()

class EmailAuthenticationForm(forms.Form):
    """
    Base class for authenticating users by email. Extend this to get a form that accepts
    email/password logins.
    """

    email = forms.EmailField(
        label = _("Email"),
        widget = forms.EmailInput(),
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    error_messages = {
        "invalid_login": _(
            "Please enter a correct %(email)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        "inactive": _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        # Set the max length and label for the "emial" field.
        self.email_field = UserModel._meta.get_field(UserModel.EMAIL_FIELD)
        email_max_length = self.email_field.max_length or 254
        self.fields["email"].max_length = email_max_length
        self.fields["email"].widget.attrs["maxlength"] = email_max_length
        if self.fields["email"].label is None:
            self.fields["email"].label = capfirst(self.email_field.verbose_name)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email is not None and password:
            self.user_cache = authenticate(
                self.request, email=email, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages["invalid_login"],
            code="invalid_login",
            params={"email": self.email_field.verbose_name},
        )
```

this is just a copy of <u>[django.contrib.auth.forms.AuthenticationForm](https://docs.djangoproject.com/en/4.1/topics/auth/default/#django.contrib.auth.forms.AuthenticationForm)</u> that overwritten for email

to use this form by django,need to include <u>[django.contrib.auth.views](https://docs.djangoproject.com/en/4.1/topics/auth/default/#using-the-views)</u> in urlpatterns:

```python
from django.urls import path
from django.contrib.auth.views import LoginView
from authenticate.forms import EmailAuthenticationForm

urlpatterns = [
    path("login/", 
        LoginView.as_view(authentication_form =  EmailAuthenticationForm), 
        name = 'login'
    ),
    ...,
]
```
NOTE : if you're not familiar with authentication views you can read [URLs & views authentication customizing](https://github.com/amir-mohammad-HP/django4-SampleCode/tree/main/accounts%20URL%20customizing)