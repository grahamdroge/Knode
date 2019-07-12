from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
import requests
from django.contrib.auth import authenticate, login
from vibesite.models import UserProfile, Interests, Tools, Posts, SubSections, Saved, Comments, Notifications,RelatedPosts
from django.contrib.auth.models import User
from django.db.models import Q, Max
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import TopicForm, EditProfileForm, EditSubSectionsForm, AddTool, AddPost, SignUpForm
from actstream.models import following, followers, user_stream,actor_stream,target_stream,action_object_stream,model_stream,Action
from actstream.actions import follow, unfollow
from actstream.signals import action
import json
import operator
API_KEY = "b524964889f14643a884a1bfce281012"
topics = [
			'health',
			'finance',
			'auto',
			'film/photography',
			'entrepreneurship',
			'sports',
			'books',
			'politics',
			'music',
			'beauty',
			'technology',
			'fashion',
			'business',
			]

def search(request):
		
		if request.is_ajax():
			search_input = request.GET.get('term','')
			users = User.objects.filter(Q(username__istartswith = search_input) | Q(first_name__istartswith=search_input) | Q(last_name__istartswith=search_input))
			posts = Posts.objects.filter(post_title__istartswith = search_input)

			results = []	
			for user in users:	
				
				user_json = {

					'value': user.username,

					}

				results.append(user_json)

			for post in posts:

				post_json = {
					'value': post.post_title,
				}
			
				results.append(post_json)


			data = json.dumps(results)
			mimetype = 'application/json'
			
			return HttpResponse(data, mimetype)


@login_required
def userprofile(request,username):

	if User.objects.filter(username=username).exists():

		profile = User.objects.get(username=username)

		# if profile.username == request.user.username:
		# 	return redirect('home')

		topics = [
		'health',
		'finance',
		'auto',
		'film/photography',
		'entrepreneurship',
		'sports',
		'books',
		'politics',
		'music',
		'beauty',
		'technology',
		'fashion',
		'business',
		]

		sub_sections = {


		} 

		topics_set = {

			'health': bool(profile.userprofile.interests_set.filter(section='health').exists()),
			'finance': bool(profile.userprofile.interests_set.filter(section='finance').exists()),
			'auto': bool(profile.userprofile.interests_set.filter(section='auto').exists()),
			'film': bool(profile.userprofile.interests_set.filter(section='film').exists()),
			'entrepreneurship': bool(profile.userprofile.interests_set.filter(section='entrepreneurship').exists()),
			'sports': bool(profile.userprofile.interests_set.filter(section='sports').exists()),
			'books': bool(profile.userprofile.interests_set.filter(section='books').exists()),
			'politics': bool(profile.userprofile.interests_set.filter(section='politics').exists()),
			'music': bool(profile.userprofile.interests_set.filter(section='music').exists()),
			'beauty': bool(profile.userprofile.interests_set.filter(section='beauty').exists()),
			'crafts': bool(profile.userprofile.interests_set.filter(section='crafts').exists()),
			'technology': bool(profile.userprofile.interests_set.filter(section='technology').exists()),
			'fashion': bool(profile.userprofile.interests_set.filter(section='fashion').exists()),
			'business': bool(profile.userprofile.interests_set.filter(section='business').exists()),

		}

		if request.method == "GET":

			interests = profile.userprofile.interests_set.all()

			for interest in interests:
				sub_sections[interest.section] = interest.subsections_set.all()
				interest.subscribers = len(followers(interest))

			profile.userprofile.save()

			stream = user_stream(request.user,with_user_activity=False)
			profile_following = following(profile)
			profile_following_set = set()
			user_following = following(request.user)
			user_following_set = set()	

			saved = profile.userprofile.saved_set.all()

# ------------------------------------- For top post and top gear

			top_post_dict = {}
			top_gear_dict = {}

			for interest in interests:
				for sub in interest.subsections_set.all():
					for post in sub.posts_set.all():
						if (post.post_title != '') and (post.post_title != None):
							top_post_dict[post] = post.num_saved

			for interest in interests:
				for sub in interest.subsections_set.all():
					for tool in sub.tools_set.all():
						top_gear_dict[tool] = tool.num_saved

			sorted_post = sorted(top_post_dict.items(), key=operator.itemgetter(1))
			sorted_gear = sorted(top_gear_dict.items(), key=operator.itemgetter(1))
			
# -------------------------------------

			# for user in user_following:
			# 	if user:
			# 		user_following_set.add(user.section)

			# for user in profile_following:
			# 	if user:
			# 		profile_following_set.add(user.section)

			topic_form = TopicForm(initial=topics_set)

			return render(request,'userprofile.html', 
				{
				'sub_sections': sub_sections,
				'interests': interests, 
				'topics': topics, 
				'profile': profile,
				'stream': stream, 
				'profile_following': profile_following, 
				'profile_following_set': profile_following_set,
				'user_following_set': user_following_set,
				'top_post': sorted_post[:-6:-1],
				'top_gear': sorted_gear[:-6:-1],

				'topic_form': topic_form,

				'saved': saved,

				'section_feed': request.session['section_feed'],
				'post_feed': request.session['post_feed'],
				'tool_feed': request.session['tool_feed'],
				 }
			)
			
		elif request.method == 'POST':
			if "search-user" in request.POST:

				data = request.POST['search-user']

				if request.user.username == data:
					return redirect('home')

				elif User.objects.filter(username=data).exists():	
					return redirect('userprofile', username=data)

				elif Posts.objects.filter(post_title=data).exists():
					post = Posts.objects.get(post_title=data)
					return redirect('subtopic_guest', username=post.sub_section.interest.userprofile.user, topic=post.sub_section.interest, subtopic=post.sub_section)

				else:
					return type('Response%d' % 204, (HttpResponse, ), {'status_code': 204})()

			if 'feed-filter' in request.POST:
				feed_filt = request.POST.get('feed-filter')

				if feed_filt == "tool":
					request.session['tool_feed'] = True
					request.session['post_feed'] = False
					request.session['section_feed'] = False

				elif feed_filt == "post":
					request.session['tool_feed'] = False
					request.session['post_feed'] = True
					request.session['section_feed'] = False

				elif feed_filt == "none":
					request.session['tool_feed'] = False
					request.session['post_feed'] = False
					request.session['section_feed'] = False

				else:
					request.session['tool_feed'] = False
					request.session['post_feed'] = False
					request.session['section_feed'] = feed_filt

				
				return redirect('userprofile', username=username)

			if "topic" in request.POST:			
				topic_form = TopicForm(request.POST or None)
				if topic_form.is_valid():

				
					health = topic_form.cleaned_data['health']
					finance = topic_form.cleaned_data['finance']
					auto = topic_form.cleaned_data['auto']
					film = topic_form.cleaned_data['film']
					entrepreneurship = topic_form.cleaned_data['entrepreneurship']
					sports = topic_form.cleaned_data['sports']
					books = topic_form.cleaned_data['books']
					politics = topic_form.cleaned_data['politics']
					music = topic_form.cleaned_data['music']
					beauty = topic_form.cleaned_data['beauty']
					technology = topic_form.cleaned_data['technology']
					fashion = topic_form.cleaned_data['fashion']
					business = topic_form.cleaned_data['business']

					if health:
						if request.user.userprofile.interests_set.filter(section='health'):
							pass
						else:
							request.user.userprofile.interests_set.create(section='health')
							request.user.userprofile.save()
					else:
						if topics_set['health']:
							request.user.userprofile.interests_set.filter(section='health').delete()
						else:
							pass

					if business:
						if request.user.userprofile.interests_set.filter(section='business'):
							pass
						else:
							request.user.userprofile.interests_set.create(section='business')
							request.user.userprofile.save()
					else:
						if topics_set['business']:
							request.user.userprofile.interests_set.filter(section='business').delete()
						else:
							pass
						
					if finance:
						if request.user.userprofile.interests_set.filter(section='finance'):
							pass
						else:
							request.user.userprofile.interests_set.create(section='finance')
							request.user.userprofile.save()

					else:
						if topics_set['finance']:
							request.user.userprofile.interests_set.filter(section='finance').delete()
						else:
							pass

					if auto:
						if request.user.userprofile.interests_set.filter(section='auto'):
							pass
						else:
							request.user.userprofile.interests_set.create(section='auto')
							request.user.userprofile.save()

					else:
						if topics_set['auto']:
							request.user.userprofile.interests_set.filter(section='auto').delete()
						else:
							pass

					if film:
						if request.user.userprofile.interests_set.filter(section='film'):
							pass
						else:
							request.user.userprofile.interests_set.create(section='film')
							request.user.userprofile.save()

					else:
						if topics_set['film']:
							request.user.userprofile.interests_set.filter(section='film').delete()
						else:
							pass

					if entrepreneurship:
						if request.user.userprofile.interests_set.filter(section='entrepreneurship'):
							pass
						else:
							request.user.userprofile.interests_set.create(section='entrepreneurship')
							request.user.userprofile.save()

					else:
						if topics_set['entrepreneurship']:
							request.user.userprofile.interests_set.filter(section='entrepreneurship').delete()
						else:
							pass

					if sports:
						if request.user.userprofile.interests_set.filter(section='sports'):
							pass
						else:
							request.user.userprofile.interests_set.create(section='sports')
							request.user.userprofile.save()

					else:
						if topics_set['sports']:
							request.user.userprofile.interests_set.filter(section='sports').delete()
						else:
							pass

					if books:
						if request.user.userprofile.interests_set.filter(section='books'):
							pass
						else:
							request.user.userprofile.interests_set.create(section='books')
							request.user.userprofile.save()

					else:
						if topics_set['books']:
							request.user.userprofile.interests_set.filter(section='books').delete()
						else:
							pass

					if politics:
						if request.user.userprofile.interests_set.filter(section='politics'):
							pass
						else:
							request.user.userprofile.interests_set.create(section='politics')
							request.user.userprofile.save()

					else:
						if topics_set['politics']:
							request.user.userprofile.interests_set.filter(section='politics').delete()
						else:
							pass

					if music:
						if request.user.userprofile.interests_set.filter(section='music'):
							pass
						else:
							request.user.userprofile.interests_set.create(section='music')
							request.user.userprofile.save()

					else:
						if topics_set['music']:
							request.user.userprofile.interests_set.filter(section='music').delete()
						else:
							pass

					if beauty:
						if request.user.userprofile.interests_set.filter(section='beauty'):
							pass
						else:
							request.user.userprofile.interests_set.create(section='beauty')
							request.user.userprofile.save()

					else:
						if topics_set['beauty']:
							request.user.userprofile.interests_set.filter(section='beauty').delete()
						else:
							pass

					if technology:
						if request.user.userprofile.interests_set.filter(section='technology'):
							pass
						else:
							request.user.userprofile.interests_set.create(section='technology')
							request.user.userprofile.save()

					else:
						if topics_set['technology']:
							request.user.userprofile.interests_set.filter(section='technology').delete()
						else:
							pass

					if fashion:
						if request.user.userprofile.interests_set.filter(section='fashion'):
							pass
						else:
							request.user.userprofile.interests_set.create(section='fashion')
							request.user.userprofile.save()

					else:
						if topics_set['fashion']:
							request.user.userprofile.interests_set.filter(section='fashion').delete()
						else:
							pass

				return redirect('userprofile',username=username)	

	else:

		return render(request,'faileduserprofile.html')

@login_required
def subtopic_guest(request,subtopic,topic,username):

	user = User.objects.get(username=username)

	subtopic_tools = user.userprofile.interests_set.get(section=topic).subsections_set.get(title=subtopic).tools_set.all()
	subtopic_posts = user.userprofile.interests_set.get(section=topic).subsections_set.get(title=subtopic).posts_set.all()


	return render(request, 'tools_topics_guest.html',{'subtopic_tools': subtopic_tools, 'subtopic_posts': subtopic_posts, 'subtopic': subtopic, 'topic': topic})

@login_required
def subtopic(request, subtopic, topic):

	

	if request.method == 'POST':

		if "tool" in request.POST:
			add_tool_form = AddTool(request.POST)
			if add_tool_form.is_valid():
				tool_name = add_tool_form.cleaned_data['tool_name']
				tool_link = add_tool_form.cleaned_data['tool_link']

				new_tool = request.user.userprofile.interests_set.get(section=topic).subsections_set.get(title=subtopic).tools_set.create(tool_name=tool_name, tool_link=tool_link)

				interest = request.user.userprofile.interests_set.get(section=topic)
				sub_section = request.user.userprofile.interests_set.get(section=topic).subsections_set.get(title=subtopic)

				action.send(request.user, verb="posted-tool", action_object=new_tool, target=sub_section)

				return redirect('/'+topic+'/'+subtopic)

		if "post" in request.POST:
			add_post_form = AddPost(request.POST,request.FILES)
			interest = request.POST.get('section')
			sub_section = request.POST.get('sub_section')

			if add_post_form.is_valid():
				post_title = add_post_form.cleaned_data['post_title']
				post_content = add_post_form.cleaned_data['post_content']
				post_video = add_post_form.cleaned_data['post_video']
				post_video_id = None
				if post_video:
					post_video_id = post_video.split("=")[1]

				if request.FILES:

					new_post = request.user.userprofile.interests_set.get(section=interest).subsections_set.get(title=sub_section).posts_set.create(post_title=post_title, post_content=post_content,post_image=request.FILES['post_image'])

				else:
					
					new_post = request.user.userprofile.interests_set.get(section=interest).subsections_set.get(title=sub_section).posts_set.create(post_title=post_title, post_content=post_content, post_video=post_video_id)	

				interest = request.user.userprofile.interests_set.get(section=interest)
				sub_section = request.user.userprofile.interests_set.get(section=interest).subsections_set.get(title=sub_section)

				action.send(request.user, verb="posted-post", action_object=new_post, target=sub_section)

				return redirect('/'+topic+'/'+subtopic)

		
	add_tool_form = AddTool()
	add_post_form = AddPost()	

	subtopic_tools = request.user.userprofile.interests_set.get(section=topic).subsections_set.get(title=subtopic).tools_set.all()
	subtopic_posts = request.user.userprofile.interests_set.get(section=topic).subsections_set.get(title=subtopic).posts_set.all()

	return render(request, 'tools_topics.html',{'subtopic_tools': subtopic_tools, 'subtopic_posts': subtopic_posts, 'subtopic': subtopic, 'topic': topic, 'add_tool_form': add_tool_form, 'add_post_form': add_post_form})



@login_required
def edit(request):

	if request.method == 'POST':
		# userform = EditUserForm(request.POST)
		profileform = EditProfileForm(request.POST)
		if profileform.is_valid():
			# user_data = userform.save(commit=False)
			# user_data.save()
			bio = profileform.cleaned_data['bio']
			location = profileform.cleaned_data['location']
			request.user.userprofile.bio = bio
			request.user.userprofile.location = location
			request.user.userprofile.save()

			return HttpResponseRedirect('/')
		else:
			return HttpResponseRedirect('/login/')
	else:
		# current_user_data = {
		# 	'first_name': request.user.first_name,
		# 	'last_name': request.user.last_name,
		# 	'email': request.user.email,
		# 	'username': request.user.username,
		# }

		current_profile_data = {
			'bio': request.user.userprofile.bio,
			'location': request.user.userprofile.location,
		}
		# userform = EditUserForm(initial=current_user_data)
		profileform = EditProfileForm(initial=current_profile_data)
		return render(request,'editprofile.html',{'profileform': profileform})


def sub_create(request):
	user = User.objects.get(username=request.user.username)
	interest = request.POST.get('interest')
	sub_name = request.POST.get('subtopic')

	if (interest) and (sub_name):

		user.userprofile.interests_set.get(section=interest).subsections_set.create(title=sub_name)




@login_required
def home(request):

	topics = [

		'health',
		'finance',
		'auto',
		'film/photography',
		'entrepreneurship',
		'sports',
		'books',
		'politics',
		'music',
		'beauty',
		'technology',
		'fashion',
		'business',
	]

	sub_sections = {


	} 

	if request.session.get('articles') == None:
		tech_crunch = requests.get("https://newsapi.org/v1/articles?source=techcrunch&sortBy=latest&apiKey="+API_KEY).json()
		tech_radar = requests.get("https://newsapi.org/v1/articles?source=techradar&sortBy=latest&apiKey="+API_KEY).json()
		verge = requests.get("https://newsapi.org/v1/articles?source=the-verge&sortBy=latest&apiKey="+API_KEY).json()
		the_next_web = requests.get("https://newsapi.org/v1/articles?source=the-next-web&sortBy=latest&apiKey="+API_KEY).json()

		the_next_web_articles = the_next_web['articles']
		verge_articles = verge['articles']
		tech_crunch_articles = tech_crunch['articles'] 
		tech_radar_articles = tech_radar['articles']

		# request.session['articles'] = [the_next_web_articles,verge_articles,tech_crunch_articles,tech_radar_articles]
		request.session['articles'] = [the_next_web,verge,tech_crunch,tech_radar]
		request.session['news'] = 'technology'


	topics_set = {

		'health': bool(request.user.userprofile.interests_set.filter(section='health').exists()),
		'finance': bool(request.user.userprofile.interests_set.filter(section='finance').exists()),
		'auto': bool(request.user.userprofile.interests_set.filter(section='auto').exists()),
		'film': bool(request.user.userprofile.interests_set.filter(section='film').exists()),
		'entrepreneurship': bool(request.user.userprofile.interests_set.filter(section='entrepreneurship').exists()),
		'sports': bool(request.user.userprofile.interests_set.filter(section='sports').exists()),
		'books': bool(request.user.userprofile.interests_set.filter(section='books').exists()),
		'politics': bool(request.user.userprofile.interests_set.filter(section='politics').exists()),
		'music': bool(request.user.userprofile.interests_set.filter(section='music').exists()),
		'beauty': bool(request.user.userprofile.interests_set.filter(section='beauty').exists()),
		'technology': bool(request.user.userprofile.interests_set.filter(section='technology').exists()),
		'fashion': bool(request.user.userprofile.interests_set.filter(section='fashion').exists()),
		'business': bool(request.user.userprofile.interests_set.filter(section='business').exists()),

	}


	interests = request.user.userprofile.interests_set.all()
	topic_form = TopicForm(initial=topics_set)
	subtopic_form = EditSubSectionsForm()


	for interest in interests:
		sub_sections[interest.section] = interest.subsections_set.all()
		interest.subscribers = len(followers(interest))

	request.user.userprofile.save()	

	

	if request.method == 'POST':
		

		
		# if "subtopic" in request.POST:
		# 	subtopic_form = EditSubSectionsForm(request.POST)
		# 	if subtopic_form.is_valid():
		# 		sub_input_sport = subtopic_form.cleaned_data['sport_title']
		# 		sub_input_film = subtopic_form.cleaned_data['film_title']
		# 		sub_input_health = subtopic_form.cleaned_data['health_title']
		# 		sub_input_finance = subtopic_form.cleaned_data['finance_title']
		# 		sub_input_auto = subtopic_form.cleaned_data['auto_title']
		# 		sub_input_entrepreneurship = subtopic_form.cleaned_data['entrepreneurship_title']
		# 		sub_input_books = subtopic_form.cleaned_data['books_title']
		# 		sub_input_politics = subtopic_form.cleaned_data['politics_title']
		# 		sub_input_music = subtopic_form.cleaned_data['music_title']
		# 		sub_input_beauty = subtopic_form.cleaned_data['beauty_title']
		# 		sub_input_technology = subtopic_form.cleaned_data['technology_title']
		# 		sub_input_fashion = subtopic_form.cleaned_data['fashion_title']
		# 		sub_input_business = subtopic_form.cleaned_data['business_title']


				
		# 		if sub_input_sport:
		# 			titles_sport = sub_input_sport.split(':')
		# 			for title in titles_sport:
		# 				if not request.user.userprofile.interests_set.get(section='sports').subsections_set.filter(title=title).exists():
		# 					request.user.userprofile.interests_set.get(section='sports').subsections_set.create(title=title)

		# 		if sub_input_business:
		# 			titles_business = sub_input_business.split(':')
		# 			for title in titles_business:
		# 				if not request.user.userprofile.interests_set.get(section='business').subsections_set.filter(title=title).exists():
		# 					request.user.userprofile.interests_set.get(section='business').subsections_set.create(title=title)
				
		# 		if sub_input_film:
		# 			titles_film = sub_input_film.split(':')
		# 			for title in titles_film:
		# 				if not request.user.userprofile.interests_set.get(section='film').subsections_set.filter(title=title).exists():
		# 					request.user.userprofile.interests_set.get(section='film').subsections_set.create(title=title)

		# 		if sub_input_health:
		# 			titles_health = sub_input_health.split(':')
		# 			for title in titles_health:
		# 				if not request.user.userprofile.interests_set.get(section='health').subsections_set.filter(title=title).exists():
		# 					request.user.userprofile.interests_set.get(section='health').subsections_set.create(title=title)


		# 		if sub_input_finance:
		# 			titles_finance = sub_input_finance.split(':')
		# 			for title in titles_finance:
		# 				if not request.user.userprofile.interests_set.get(section='finance').subsections_set.filter(title=title).exists():
		# 					request.user.userprofile.interests_set.get(section='finance').subsections_set.create(title=title)

		# 		if sub_input_auto:
		# 			titles_auto = sub_input_auto.split(':')
		# 			for title in titles_auto:
		# 				if not request.user.userprofile.interests_set.get(section='auto').subsections_set.filter(title=title).exists():
		# 					request.user.userprofile.interests_set.get(section='auto').subsections_set.create(title=title)

		# 		if sub_input_entrepreneurship:
		# 			titles_entrepreneurship = sub_input_entrepreneurship.split(':')
		# 			for title in titles_entrepreneurship:
		# 				if not request.user.userprofile.interests_set.get(section='entrepreneurship').subsections_set.filter(title=title).exists():
		# 					request.user.userprofile.interests_set.get(section='entrepreneurship').subsections_set.create(title=title)

		# 		if sub_input_books:
		# 			titles_books = sub_input_books.split(':')
		# 			for title in titles_books:
		# 				if not request.user.userprofile.interests_set.get(section='books').subsections_set.filter(title=title).exists():
		# 					request.user.userprofile.interests_set.get(section='books').subsections_set.create(title=title)


		# 		if sub_input_politics:
		# 			titles_politics = sub_input_politics.split(':')
		# 			for title in titles_politics:
		# 				if not request.user.userprofile.interests_set.get(section='politics').subsections_set.filter(title=title).exists():
		# 					request.user.userprofile.interests_set.get(section='politics').subsections_set.create(title=title)

		# 		if sub_input_music:
		# 			titles_music = sub_input_music.split(':')
		# 			for title in titles_music:
		# 				if not request.user.userprofile.interests_set.get(section='music').subsections_set.filter(title=title).exists():
		# 					request.user.userprofile.interests_set.get(section='music').subsections_set.create(title=title)

		# 		if sub_input_technology:
		# 			titles_technology = sub_input_technology.split(':')
		# 			for title in titles_technology:
		# 				if not request.user.userprofile.interests_set.get(section='technology').subsections_set.filter(title=title).exists():
		# 					request.user.userprofile.interests_set.get(section='technology').subsections_set.create(title=title)

		# 		if sub_input_fashion:
		# 			titles_fashion = sub_input_fashion.split(':')
		# 			for title in titles_fashion:
		# 				if not request.user.userprofile.interests_set.get(section='fashion').subsections_set.filter(title=title).exists():
		# 					request.user.userprofile.interests_set.get(section='fashion').subsections_set.create(title=title)

		# 		if sub_input_beauty:
		# 			titles_beauty = sub_input_beauty.split(':')
		# 			for title in titles_beauty:
		# 				if not request.user.userprofile.interests_set.get(section='beauty').subsections_set.filter(title=title).exists():
		# 					request.user.userprofile.interests_set.get(section='beauty').subsections_set.create(title=title)


		# 		# subtopic_form = EditSubSectionsForm()	
		# 		# stream = user_stream(request.user,with_user_activity=False)
		# 		# user_following = following(request.user,User)

		# 		# return render(request, 'home.html', {'topics': topics, 'topic_form': topic_form, 'interests': interests, 'sub_sections': sub_sections, 'subtopic_form': subtopic_form, 'stream': stream})
		# 		return redirect('home')
			
		if "search-user" in request.POST:

			data = request.POST['search-user']

			if request.user.username == data:
				return redirect('home')

			elif User.objects.filter(username=data).exists():	
				return redirect('userprofile', username=data)

			elif Posts.objects.filter(post_title=data).exists():
				post = Posts.objects.get(post_title=data)
				return redirect('subtopic_guest', username=post.sub_section.interest.userprofile.user, topic=post.sub_section.interest, subtopic=post.sub_section)

			else:
				return type('Response%d' % 204, (HttpResponse, ), {'status_code': 204})()

		if "tool" in request.POST:
			from actstream.signals import action
			try:
				add_tool_form = AddTool(request.POST)
				interest = request.POST.get('section')
				sub_section = request.POST.get('sub_section')
				user = User.objects.get(username=request.user.username)

				if add_tool_form.is_valid():
					tool_name = add_tool_form.cleaned_data['tool_name']
					tool_link = add_tool_form.cleaned_data['tool_link']

					new_tool = user.userprofile.interests_set.get(section=interest).subsections_set.get(title=sub_section).tools_set.create(tool_name=tool_name, tool_link=tool_link)

					
					sub_section = user.userprofile.interests_set.get(section=interest).subsections_set.get(title=sub_section)

					action.send(request.user, verb="posted-tool", action_object=new_tool, target=sub_section)


					return redirect('home')

			except:
				return type('Response%d' % 204, (HttpResponse, ), {'status_code': 204})()

		if "post" in request.POST:
			from actstream.signals import action
			try:
				add_post_form = AddPost(request.POST,request.FILES)
				interest = request.POST.get('section')
				sub_section = request.POST.get('sub_section')
				try:
					relate_post = request.POST.get('postname').split('_')[0]
					relate_sub = request.POST.get('postname').split('_')[1]
				except:
					relate_post = None
					relate_sub = None

				user = User.objects.get(username=request.user.username)

				if add_post_form.is_valid():
					post_title = add_post_form.cleaned_data['post_title']
					post_content = add_post_form.cleaned_data['post_content']
					post_video = add_post_form.cleaned_data['post_video']
					post_file = add_post_form.cleaned_data['post_file']
					# post_image = add_post_form.cleaned_data['post_image']
					post_video_id = None
					if post_video:
						post_video_id = post_video.split("=")[1]

					if request.FILES:
						if post_file:	
							new_post = user.userprofile.interests_set.get(section=interest).subsections_set.get(title=sub_section).posts_set.create(post_title=post_title,post_content=post_content,post_file=request.FILES['post_file'])
							if relate_post:
								main_post = user.userprofile.interests_set.get(section=interest).subsections_set.get(title=relate_sub).posts_set.get(post_title=relate_post)
								RelatedPosts.objects.create(main_post=main_post,rel_post=new_post)
						else:
							new_post = user.userprofile.interests_set.get(section=interest).subsections_set.get(title=sub_section).posts_set.create(post_title=post_title,post_content=post_content,post_image=request.FILES['post_image'])
							if relate_post:
								main_post = user.userprofile.interests_set.get(section=interest).subsections_set.get(title=relate_sub).posts_set.get(post_title=relate_post)
								RelatedPosts.objects.create(main_post=main_post,rel_post=new_post)

						# sub_section = user.userprofile.interests_set.get(section=interest).subsections_set.get(title=sub_section)
						# sub_section = user.userprofile.interests_set.get(section=interest).subsections_set.get(title=sub_section)
						# action.send(request.user,verb="posted-post",action_object=new_post,target=sub_section)
						# Action.objects.create(actor=request.user,action_object=new_post,verb="posted-post",target=sub_section)
					else:	
						new_post = user.userprofile.interests_set.get(section=interest).subsections_set.get(title=sub_section).posts_set.create(post_title=post_title, post_content=post_content, post_video=post_video_id)	
						if relate_post:
								main_post = user.userprofile.interests_set.get(section=interest).subsections_set.get(title=relate_sub).posts_set.get(post_title=relate_post)
								RelatedPosts.objects.create(main_post=main_post,rel_post=new_post)

						
					# sub_section = user.userprofile.interests_set.get(section=interest).subsections_set.get(title=sub_section)
					# action.send(request.user,verb="posted-post",action_object=new_post,target=sub_section)
					# action.send(request.user,verb='posted-post',action_object=post,target=sub_section)
					# Action.objects.create(actor=request.user,action_object=new_post,verb="posted-post",target=sub_section)

				sub_section = user.userprofile.interests_set.get(section=interest).subsections_set.get(title=sub_section)
				action.send(request.user,verb="posted-post",action_object=new_post,target=sub_section)

				return redirect('home')

			except:
				return type('Response%d' % 204, (HttpResponse, ), {'status_code': 204})()

		if request.is_ajax():
			if request.method == "POST":
				username = request.POST.get('username')
				title = request.POST.get('title')
				kind = request.POST.get('type')
				sub = request.POST.get('sub')
				interest = request.POST.get('interest')
				action = request.POST.get('action')

				if action == 'save':
					if kind == "post":
						user = User.objects.get(username=username)
						post = user.userprofile.interests_set.get(section=interest).subsections_set.get(title=sub).posts_set.get(post_title=title)
						post.num_saved += 1
						post.save()
						request.user.userprofile.saved_set.create(post=post)
						request.user.userprofile.save()
						
					if kind == "tool":
						user = User.objects.get(username=username)
						tool = user.userprofile.interests_set.get(section=interest).subsections_set.get(title=sub).tools_set.get(tool_name=title)
						tool.num_saved += 1
						tool.save()
						request.user.userprofile.saved_set.create(tool=tool)
						request.user.userprofile.save()

				if action == 'unsave':
					if kind == "post":
						user = User.objects.get(username=username)
						post = user.userprofile.interests_set.get(section=interest).subsections_set.get(title=sub).posts_set.get(post_title=title)
						post.num_saved -= 1
						post.save()
						request.user.userprofile.saved_set.get(post=post).delete()
						request.user.userprofile.save()
						
					if kind == "tool":
						user = User.objects.get(username=username)
						tool = user.userprofile.interests_set.get(section=interest).subsections_set.get(title=sub).tools_set.get(tool_name=title)
						tool.num_saved -= 1
						tool.save()
						request.user.userprofile.saved_set.get(tool=tool).delete()
						request.user.userprofile.save()

				else: 
					return redirect('login')



		if 'feed-filter' in request.POST:
			feed_filt = request.POST.get('feed-filter')

			if feed_filt == "tool":
				request.session['tool_feed'] = True
				request.session['post_feed'] = False
				request.session['section_feed'] = False

			elif feed_filt == "post":
				request.session['tool_feed'] = False
				request.session['post_feed'] = True
				request.session['section_feed'] = False

			elif feed_filt == "none":
				request.session['tool_feed'] = False
				request.session['post_feed'] = False
				request.session['section_feed'] = False

			else:
				request.session['tool_feed'] = False
				request.session['post_feed'] = False
				request.session['section_feed'] = feed_filt

			
			return redirect('home')


		else:
			return HttpResponseRedirect('/login/')
				


	else:
		saved = request.user.userprofile.saved_set.all()

		stream = user_stream(request.user,with_user_activity=False) 
		user_following = following(request.user)
		# user_following_set = set()
		# for user in user_following:
		# 	if user:
		# 		user_following_set.add(user.section)

		# followers_set = {

		# }

		# for interest in interests:
		# 	followers_set[interest.section] = followers(interest)


		if (request.session.get('section_feed') == None and request.session.get('post_feed') == None and request.session.get('tool_feed') == None):
			request.session['tool_feed'] = False
			request.session['post_feed'] = False
			request.session['section_feed'] = False
		# ------------------------------------------------------------ FOR TOP POSTS

		all_posts = Posts.objects.all().order_by('-num_saved')
		top_post = []
		for post in all_posts:
			if post.sub_section.interest.section == 'technology' and post.post_title:
				top_post.append(post)

		all_tools = Tools.objects.all().order_by('-num_saved')
		top_tool = []
		for tool in all_tools:
			if tool.sub_section.interest.section == 'technology':
				top_tool.append(tool)

		# ------------------------------------------------------------

		add_tool_form = AddTool()
		add_post_form = AddPost()


		notifications = Notifications.objects.filter(user=request.user)


		context = {
			'topics': topics, 
			'topic_form': topic_form, 
			'interests': interests, 
			'sub_sections': sub_sections, 

			'notifications': notifications,
 
			'stream': stream, 
			'user_following': user_following, 
			# 'user_following_set': user_following_set,
			# 'followers_set': followers_set, 
			'section_feed': request.session['section_feed'],
			'post_feed': request.session['post_feed'],
			'tool_feed': request.session['tool_feed'],
			# 'tech_crunch_articles': tech_crunch_articles,
			# 'tech_radar_articles': tech_radar_articles,
			# 'verge_articles': verge_articles,
			# 'the_next_web_articles': the_next_web_articles,
			'articles': request.session['articles'],
			'news': request.session['news'],
			'saved': saved,
			'top_post': top_post,
			'top_tool': top_tool,

			'add_tool_form': add_tool_form,
			'add_post_form': add_post_form,
			
			}

		try: 
			subsections = request.user.userprofile.interests_set.get(section=interests[0].section).subsections_set.all()
		except:
			subsections = []
		
		return render(request, 'home.html', context)
		return render(request,'content_right.html',context)
		return render(request,'top_post.html',context)
		return render(request,'post_feed_sub.html',{'subsections': subsections})
		



def sub(request):
	
	try:
		string = request.GET.get('string')
		split = string.split('-')

		subsection_name = split[0].replace('_',' ')
		username = split[1]
		section = split[2]

		subsection = User.objects.get(username=username).userprofile.interests_set.get(section=section).subsections_set.get(title=subsection_name)

		posts = User.objects.get(username=username).userprofile.interests_set.get(section=section).subsections_set.get(title=subsection_name).posts_set.all()
		tools = User.objects.get(username=username).userprofile.interests_set.get(section=section).subsections_set.get(title=subsection_name).tools_set.all()

		context = {
			'posts': reversed(posts),
			'tools': reversed(tools),
			'subsection': subsection
		}


		return render(request,'section_left.html',context)

	except:
		username = request.GET.get('username')
		profile = User.objects.get(username=username)

		top_post_dict = {}
		top_gear_dict = {}

		for interest in profile.userprofile.interests_set.all():
			for sub in interest.subsections_set.all():
				for post in sub.posts_set.all():
					if (post.post_title != '') and (post.post_title != None):
						top_post_dict[post] = post.num_saved

		for interest in profile.userprofile.interests_set.all():
			for sub in interest.subsections_set.all():
				for tool in sub.tools_set.all():
					top_gear_dict[tool] = tool.num_saved

		sorted_post = sorted(top_post_dict.items(), key=operator.itemgetter(1))
		sorted_gear = sorted(top_gear_dict.items(), key=operator.itemgetter(1))

		saved = profile.userprofile.saved_set.all()

		context = {
			'profile': profile,
			'top_post': sorted_post[:-6:-1],
			'top_gear': sorted_gear[:-6:-1],
			'saved': saved,
		}

		return render(request,'content_left.html',context)

def addquick(request):
	interest = request.POST.get('interest')
	subsection = request.POST.get('subsection')
	post_content = request.POST.get('post_content')

	user = User.objects.get(username=request.user.username)
	sub_section = user.userprofile.interests_set.get(section=interest).subsections_set.get(title=subsection)
	post = user.userprofile.interests_set.get(section=interest).subsections_set.get(title=subsection).posts_set.create(post_content=post_content)

	action.send(request.user,verb='posted-post',action_object=post,target=sub_section)

def update_post_feed(request):
	interest = request.GET.get('interest')
	user = User.objects.get(username=request.user.username)

	subsections = user.userprofile.interests_set.get(section=interest).subsections_set.all()

	return render(request,'post_feed_sub.html',{'subsections': subsections})

def related_posts(request):
	interest = request.GET.get('interest')
	interest_posts = []

	for sub in request.user.userprofile.interests_set.get(section=interest).subsections_set.all():
		for post in sub.posts_set.all():
			if not (RelatedPosts.objects.filter(rel_post=post)):
				interest_posts.append(post)



	return render(request,'related_posts.html',{'interest_posts': interest_posts}) 


def add_content(request):
	post_title = request.POST.get('post_title')
	post_content = request.POST.get('post_content')
	post_image = request.FILES.get('post_image')

def sub_follow(request):
	check = request.POST.get('check')
	sub = request.POST.get('sub')
	interest = request.POST.get('interest')
	username = request.POST.get('user')

	interest = User.objects.get(username=username).userprofile.interests_set.get(section=interest)
	sub_section = User.objects.get(username=username).userprofile.interests_set.get(section=interest).subsections_set.get(title=sub)

	if check == 'not_following':

		unfollow(request.user,interest)
		follow(request.user,sub_section,actor_only=False)
		sub_section.number_followers += 1
		interest.subscribers += 1
		sub_section.save()
		interest.save()


	else:
		
		unfollow(request.user, sub_section)	
		sub_section.number_followers -= 1
		interest.subscribers -= 1
		sub_section.save()
		interest.save()		

def update_top_post(request):
	section = request.GET.get('section')


	all_posts = Posts.objects.all().order_by('-num_saved')
	top_post = []
	for post in all_posts:
		if post.sub_section.interest.section == section and post.post_title:
			top_post.append(post)


	context = {
		'top_post': top_post,
	}

	return render(request,'top_post.html',context)

def comment(request):
	title = request.POST.get('title')
	kind = request.POST.get('type')
	comment = request.POST.get('comment')

	interest = request.POST.get('interest')
	subsection = request.POST.get('subsection')
	full_name = request.POST.get('user')
	first_name = full_name.split(' ')[0]
	last_name = full_name.split(' ')[1]

	user = User.objects.get(first_name=first_name,last_name=last_name)

	if kind == 'post':
		post = user.userprofile.interests_set.get(section=interest).subsections_set.get(title=subsection).posts_set.get(post_title=title)
		Comments.objects.create(user=request.user,post=post,comment=comment)

		Notifications.objects.create(user=user,actor=request.user,verb='commented on',action_object=post)
	else:
		tool = user.userprofile.interests_set.get(section=interest).subsections_set.get(title=subsection).tools_set.get(tool_name=title)
		Comments.objects.create(user=request.user,tool=tool,comment=comment)

		Notifications.objects.create(user=user,actor=request.user,verb='commented on',action_object=tool)

def reroute(request):
	username = request.POST.get('username')
	title = request.POST.get('title')
	subsection = request.POST.get('subsection')
	interest = request.POST.get('interest')
	kind = request.POST.get('kind')
	new_sub = request.POST.get('new_sub')

	user = User.objects.get(username=username)

	if request.user.userprofile.interests_set.filter(section=interest) and user != request.user:

		if kind == 'post':
			try:
				post = user.userprofile.interests_set.get(section=interest).subsections_set.get(title=subsection).posts_set.get(post_title=title)
				interest = request.user.userprofile.interests_set.get(section=interest)
				new_sub = request.user.userprofile.interests_set.get(section=interest).subsections_set.get(title=new_sub)
				action.send(request.user,verb='rerouted_post',action_object=post,target=new_sub)
				post.num_reroute += 1

				post.save()
			except:
				return redirect('login.html')

		elif kind == 'tool':
			try:
				tool = user.userprofile.interests_set.get(section=interest).subsections_set.get(title=subsection).tools_set.get(tool_name=title)
				interest = request.user.userprofile.interests_set.get(section=interest)
				new_sub = request.user.userprofile.interests_set.get(section=interest).subsections_set.get(title=new_sub)
				action.send(request.user,verb='rerouted_tool',action_object=tool,target=new_sub)
				tool.num_reroute += 1

				tool.save()
			except:
				return redirect('login.html')

	else:
		return redirect('editprofile.html')
	

def update_top_tool(request):
	section = request.GET.get('section')


	all_tools = Tools.objects.all().order_by('-num_saved')
	top_tool = []
	for tool in all_tools:
		if tool.sub_section.interest.section == section:
			top_tool.append(tool)


	context = {
		'top_tool': top_tool,
	}

	return render(request,'top_tool.html',context)


def update(request):
	topic = request.GET.get('topic')
	
	if topic == 'business':		
		cnbc = requests.get("https://newsapi.org/v1/articles?source=cnbc&sortBy=top&apiKey="+API_KEY)
		business_insider = requests.get("https://newsapi.org/v1/articles?source=business-insider&sortBy=top&apiKey="+API_KEY)
		business_insider = business_insider.json()
		cnbc = cnbc.json()
		cnbc_articles = cnbc['articles']
		business_insider_articles = business_insider['articles']	

		# request.session['articles'] = [cnbc_articles,business_insider_articles]
		request.session['articles'] = [cnbc,business_insider]
		request.session['news'] = 'business'


		return render(request,'content_right.html',{'articles': request.session['articles'],'news': request.session['news'],'topics': topics})

	elif topic == 'technology':
		tech_crunch = requests.get("https://newsapi.org/v1/articles?source=techcrunch&sortBy=latest&apiKey="+API_KEY)
		tech_radar = requests.get("https://newsapi.org/v1/articles?source=techradar&sortBy=latest&apiKey="+API_KEY)
		verge = requests.get("https://newsapi.org/v1/articles?source=the-verge&sortBy=latest&apiKey="+API_KEY)
		the_next_web = requests.get("https://newsapi.org/v1/articles?source=the-next-web&sortBy=latest&apiKey="+API_KEY)
		
		tech_crunch = tech_crunch.json()
		tech_radar = tech_radar.json()
		verge = verge.json()
		the_next_web = the_next_web.json()

		the_next_web_articles = the_next_web['articles']
		verge_articles = verge['articles']
		tech_crunch_articles = tech_crunch['articles'] 
		tech_radar_articles = tech_radar['articles']


		# request.session['articles'] = [the_next_web_articles,verge_articles,tech_crunch_articles,tech_radar_articles]
		request.session['articles'] = [the_next_web,verge,tech_crunch,tech_radar]
		request.session['news'] = 'technology'

		return render(request,'content_right.html',{'articles': request.session['articles'],'news': request.session['news'],'topics': topics})
		
	else:
		return render(request,'editprofile.html')





def signup(request):

	if request.method == 'POST':
		form = SignUpForm(request.POST)

		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password')
			user = authenticate(username=username,password=raw_password)
			# login(request,user)
			return redirect('login')

	else:
		form = SignUpForm()
	return render(request, 'registration/signup.html', {'form': form})