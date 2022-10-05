from django.db import models

# Create your models here.
class ImageModel(models.Model):
	image = models.ImageField(
		"image",
		upload_to = 'image_media/',
	)

