# Image Admin Preview

show image preview in admin page 

add this to ModelAdmin in "admin.py"
```python
from django.contrib import admin
from models import models
from django.utils.html import format_html

class ImageAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" width="auto" height="200px" />'.format(obj.image.url))

    image_tag.short_description = 'Image Preview'
    readonly_fields = ['image_tag']


admin.site.register(models.IMAGE, ImageAdmin)

```

make sure image configurations were done before
```python 
# project folder 
#         - urls.py 
#         - settings.py 

# urls.py

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


# settings.py

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media/'
```


# content preview:
## start project
## configure media root
## methods:
### imageadmin 
create app in very normal approach and add preview settings in adminModel
### imageadmin2
put image tag inside the app in which can be accessible more in our custom templates too!

a very usefull advantage of the second approache is to use with custom tags that we can make advantage of this
later on with help of custom template tags you can use this function to contain images tags in your templates
