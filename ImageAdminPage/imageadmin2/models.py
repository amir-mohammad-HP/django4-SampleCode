from django.db import models
from django.utils.html import format_html

# Create your models here.
class ImageModel2(models.Model):
	image = models.ImageField(
		"image",
		upload_to = 'image_media/',
	)

	def image_tag(self):
		return format_html(f'<img src="{self.image.url}" width"auto" height="200px" />' )

	image_tag.short_description = 'Image Preview'
	
class ImageModel_with_advantage(models.Model):
	image = models.ImageField(
		"image",
		upload_to = 'image_media/',
	)

	def image_tag(self, width, height):
		return format_html(f'<img src="{self.image.url}" width"{ width }" height="{ height }" />' )
	
	def image_tag_for_admin(self):
		return self.image_tag('auto', '200px')

	image_tag_for_admin.short_description = 'Image Preview'