# robots.txt

this helps search engines to realize which URLs they allow or not allow to index

put this file some where in templates folder and then refer it in your "urls.py" in project folder 

```bash
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("robots.txt",TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
]
```

now you can access it in [https://domain.com/robots.txt]()
