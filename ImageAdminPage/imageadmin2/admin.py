from django.contrib import admin
from imageadmin2.models import ImageModel2 as IM
from imageadmin2.models import ImageModel_with_advantage as IA


# Register your models here.
class ImageModel2Admin(admin.ModelAdmin):
	readonly_fields = ['image_tag']

class ImageModel_WA_Admin(admin.ModelAdmin):
	readonly_fields = ['image_tag_for_admin']

admin.site.register(IM, ImageModel2Admin)

admin.site.register(IA, ImageModel_WA_Admin)
