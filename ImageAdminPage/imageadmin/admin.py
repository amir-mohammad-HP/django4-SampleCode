from django.contrib import admin
from imageadmin.models import ImageModel as IM
from django.utils.html import format_html

# Register your models here.
class ImageModelAdmin(admin.ModelAdmin):
	def image_tag(self, obj):
		return format_html(f'<img src="{obj.image.url}" width"auto" height="200px" />' )
	image_tag.short_description = 'Image Preview'
	readonly_fields = ['image_tag']

admin.site.register(IM, ImageModelAdmin)
