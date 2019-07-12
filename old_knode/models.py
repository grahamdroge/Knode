from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver 
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from PIL import Image

# Create your models here.

class UserProfile(models.Model):

	# Create a Profile table that links to User Table. 

	user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
	bio = models.TextField()
	location = models.CharField(max_length=30, blank=True)
	education = models.CharField(max_length=30,blank=True,null=True)
	birth_date = models.DateField(null=True, blank=True)
	image = models.ImageField(upload_to='image/',null=True,default='image/default-profile.png')
	phoneNumber = models.IntegerField(null=True,blank=True)
	country = models.CharField(max_length=30,null=True)
	subscribers = models.IntegerField(default=0)

	def  __str__(self):
		return self.user.username

def create_user_profile(sender,instance,created,**kwargs):
	if created:
		UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile,sender=User)

class Notifications(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
	actor = models.ForeignKey(User,on_delete=models.CASCADE,related_name='actor')
	verb = models.CharField(max_length=30,blank=False)
	content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	action_object = GenericForeignKey('content_type', 'object_id')

	def __unicode__(self):
		return unicode(self.actor) + ' ' + unicode(self.verb) + ' ' + unicode(self.action_object)

class Interests(models.Model):

	userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
	subscribers = models.IntegerField(default=0)
	section = models.CharField(max_length=25,null=True)
	

	def __str__(self):
		return self.section

	def __unicode__(self):
		return unicode(self.section)

class SubSections(models.Model):

	interest = models.ForeignKey(Interests, on_delete=models.CASCADE)
	title = models.CharField(max_length=50,null=True)
	number_posts = models.IntegerField(default=0)
	number_tools = models.IntegerField(default=0)
	number_followers = models.IntegerField(default=0)

	def __str__(self):
		return self.title

	def __unicode__(self):
		return unicode(self.title)

class Tools(models.Model):
	sub_section = models.ForeignKey(SubSections, on_delete=models.CASCADE)
	tool_name = models.CharField(max_length=155)
	tool_link = models.URLField(null=True,default='')
	num_saved = models.IntegerField(default=0)
	num_reroute = models.IntegerField(default=0)

	def __str__(self):
		return self.tool_name

	def __unicode__(self):
		return unicode(self.tool_name)

class QuickPost(models.Model):
	sub_section = models.ForeignKey(SubSections,on_delete=models.CASCADE)
	post_content =models.TextField(default='')

class Posts(models.Model):
	sub_section = models.ForeignKey(SubSections, on_delete=models.CASCADE)
	post_title = models.CharField(max_length=155,null=True)
	post_content = models.TextField(default='',null=True)
	post_image = models.ImageField(upload_to='image/post-image/',default=None,null=True)
	post_file = models.FileField(upload_to='postdocs/',null=True)
	post_video = models.URLField(default=None,null=True)
	num_saved = models.IntegerField(default=0)
	num_reroute = models.IntegerField(default=0)

	def __str__(self):
		return self.post_title

	def __unicode__(self):
		return unicode(self.post_title)

class RelatedPosts(models.Model):
	main_post = models.ForeignKey(Posts,related_name='relatepost')
	rel_post = models.ForeignKey(Posts,related_name='mainpost')


	def __str__(self):
		return self.rel_post.post_title + ' related to ' + self.main_post.post_title

	def __unicode__(self):
		return unicode(self.rel_post.post_title) + ' related to ' + unicode(self.main_post.post_title)

# class RelatedPosts(models.Model):
# 	post = models.ForeignKey(Posts,on_delete=models.CASCADE)
# 	relpost_title = models.CharField(max_length=155,null=True)
# 	relpost_content = models.TextField(default='',null=True)
# 	relpost_image = models.ImageField(upload_to='image/post-image/',default=None,null=True)
# 	relpost_video = models.URLField(default=None,null=True)
# 	num_saved = models.IntegerField(default=0)
# 	num_reroute = models.IntegerField(default=0)
		

class Linked(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	post = models.ForeignKey(Posts,on_delete=models.CASCADE,related_name='linked_post')
	tool = models.ForeignKey(Tools,on_delete=models.CASCADE,related_name='linked_tool')

	def __str__(self):
		return self.post.post_title + " linked with " + self.tool.tool_name


class Saved(models.Model):

	userprofile = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
	post = models.ForeignKey(Posts,null=True,related_name="saved_post")
	tool = models.ForeignKey(Tools,null=True,related_name="saved_tool")

	def __str__(self):
		return self.userprofile.user.username + self.post.post_title

	def __unicode__(self):
		return unicode(self.userprofile.user.username + self.post.post_title)

class Comments(models.Model):
	post = models.ForeignKey(Posts,on_delete=models.CASCADE,related_name="post_comments",null=True)
	tool = models.ForeignKey(Tools,on_delete=models.CASCADE,related_name="tool_comments",null=True)
	user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_comments")
	comment = models.TextField()

	def __str__(self):
		return self.user.username + " commented " + self.comment
		

		
		

	

# If user updates data or is created update the appropriate UserProfile table
# @receiver(post_save, sender=User)
# def update_user_profile(sender,instance,created,**kwargs)
# 	if created:
# 		UserProfile.objects.create(user=instance)
# 	instance.profile.save()	