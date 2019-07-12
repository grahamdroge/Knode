from django import template
from vibesite.models import Linked
from django.contrib.auth.models import User
from vibesite.models import RelatedPosts

register = template.Library()

@register.filter(name='art_lookup')
def lookup(dict,key):
	
	# return dict.get(key)
	# if key == "source":
	# 	return dict.get(key)
	# elif key == "articles":
	# 	dict.get(key)
	if key == 'source_url':
		url = dict.get("source").replace("-","")
		return url

	return dict.get(key)

@register.filter(name='relate_lookup')
def relate_lookup(obj,kind):
	if kind == 'title':
		try:
			rel_post = RelatedPosts.objects.get(rel_post=obj)
			return rel_post.main_post.post_title
		except:
			return None
	if kind == 'img':
		try:
			rel_post = RelatedPosts.objects.get(rel_post=obj)
			return rel_post.main_post.sub_section.interest.userprofile.image
		except:
			return None
	if kind == 'full_name':
		try:
			rel_post = RelatedPosts.objects.get(rel_post=obj)
			return rel_post.main_post.sub_section.interest.userprofile.user.get_full_name()
		except:
			return None
	if kind == 'sub':
		try:
			rel_post = RelatedPosts.objects.get(rel_post=obj)
			return rel_post.main_post.sub_section
		except:
			return None
	if kind == 'post_image':
		try:
			rel_post = RelatedPosts.objects.get(rel_post=obj)
			return rel_post.main_post.post_image.url
		except:
			return None
	if kind == 'post_content':
		try:
			rel_post = RelatedPosts.objects.get(rel_post=obj)
			return rel_post.main_post.post_content
		except:
			return None

	if kind == 'post_video':
		try:
			rel_post = RelatedPosts.objects.get(rel_post=obj)
			return rel_post.main_post.post_video
		except:
			return None

	if kind == 'post_file':
		try:
			rel_post = RelatedPosts.objects.get(rel_post=obj)
			return rel_post.main_post.post_file
		except:
			return None

	if kind == 'num_relates':
		try:
			rel_post = RelatedPosts.objects.get(rel_post=obj)
			if len(RelatedPosts.objects.filter(main_post=rel_post.main_post)) > 1:
				return True
			else:
				return False

		except:
			return None

	if kind == 'num_saved':
		try:
			rel_post = RelatedPosts.objects.get(rel_post=obj)
			return rel_post.main_post.num_saved
				
		except:
			return None

	if kind == 'username':
		try:
			rel_post = RelatedPosts.objects.get(rel_post=obj)
			return rel_post.main_post.sub_section.interest.userprofile.user.username
				
		except:
			return None

	if kind == 'comments_len':
		try:
			rel_post = RelatedPosts.objects.get(rel_post=obj)
			return len(rel_post.main_post.post_comments.all())
				
		except:
			return None

	if kind == 'comments':
		try:
			rel_post = RelatedPosts.objects.get(rel_post=obj)
			return rel_post.main_post.post_comments.all()
				
		except:
			return None

	if kind == 'num_reroute':
		try:
			rel_post = RelatedPosts.objects.get(rel_post=obj)
			return rel_post.main_post.num_reroute
				
		except:
			return None

	if kind == 'post':
		try:
			rel_post = RelatedPosts.objects.get(rel_post=obj)
			return rel_post.main_post
				
		except:
			return None

@register.filter(name='save_lookup_post')
def saved(post,user):
	found = False
	for save_inst in post.saved_post.all():
		if save_inst.userprofile.user.username == user.username:
			found = True
			break

	return found

@register.filter(name='reroute_sub')
def reroute_sub(inst_obj,user):
	interest = inst_obj.sub_section.interest

	try:
		return user.userprofile.interests_set.get(section=interest).subsections_set.all()
	except:
		return None

@register.filter(name='save_lookup_tool')
def saved(post,user):
	found = False
	for save_inst in post.saved_tool.all():
		if save_inst.userprofile.user.username == user.username:
			found = True
			break

	return found

@register.filter(name='total_followers')
def followers(username,interest):
	total = 0 
	for sub in interest.subsections_set.all():
		total += sub.number_followers

	return total

@register.filter(name='link_lookup')
def link(ob,kind):
	user = ob.sub_section.interest.userprofile.user
	
	if kind == 'post':
		try:		
			link_list = Linked.objects.filter(post=ob,user=user)
			list_length = 0
			for link in link_list:
				list_length+=1
			return list_length
		except:
			return False
	elif kind == 'tool':
		try:
			link_list = Linked.objects.filter(tool=ob,user=user)
			list_length = 0
			for link in link_list:
				list_length+=1
			return list_length
		except:
			return False

	elif kind == 'toolnames':
		link_list = Linked.objects.filter(post=ob,user=user)

		return link_list

	else:
		link_list = Linked.objects.filter(tool=ob,user=user)

		return link_list









