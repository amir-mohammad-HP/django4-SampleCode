# set myURl.Domain/favicon.ico

add favicon.ico or etc to 'static' folder and set 
```python
STATIC_URL = 'static/'
```
in settings.py 

and in urls.py 
```python
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage

urlpatterns = [
    path("admin/", admin.site.urls),
    path("favicon.ico",RedirectView.as_view(url=staticfiles_storage.url("favicon.png")),),
]
```
