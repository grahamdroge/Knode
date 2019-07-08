from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):

	# Create a Profile table that links to User Table. 
	user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
	bio = models.TextField()
	location = models.CharField(max_length=30, blank=True)
	education = models.CharField(max_length=30,blank=True,null=True)
	birth_date = models.DateField(null=True, blank=True)
	# image = models.ImageField(upload_to='image/',null=True,default='image/default-profile.png')
	phoneNumber = models.IntegerField(null=True,blank=True)
	country = models.CharField(max_length=30,null=True)
	subscribers = models.IntegerField(default=0)

	def  __str__(self):
		return self.user.username