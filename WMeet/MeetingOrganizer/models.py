from django.db import models

# for contact form in index.html
class ContactModel(models.Model):
	name = models.CharField(max_length=120,null=False)
	email = models.EmailField(null=False)
	message = models.TextField(null=False)
	
	def __str__(self):
		return self.name
	