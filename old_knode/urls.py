from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from vibesite import views
from django.conf import settings
from django.conf.urls.static import static 
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [

    # auth_views.login automatically looks for template file at registration/login.html
	url(r'^login/$', auth_views.login, name ='login'),
	url(r'^logout/$', auth_views.logout, {'template_name': 'registration/login.html'},  name = 'logout'),
    url(r'^$', views.home, name = 'home'),
    url(r'^edit/$', views.edit, name = 'edit'),

    url(r'^signup/$', views.signup , name = 'signup'),
    url(r'^addcontent/$',views.add_content,name="add_content"),
    url(r'^relatedposts/$',views.related_posts,name="related_posts"),
    url(r'^subfollow/$',views.sub_follow,name='sub_follow'),
    url(r'^addpostfeed/$',views.update_post_feed,name="update_post_feed"),
    url(r'^addquick/$',views.addquick,name='addquick'),
    url(r'^reroute/$',views.reroute,name='reroute'),
    url(r'^addsub/$',views.sub_create,name='addsub'),
    url(r'^subsection/$',views.sub,name='subsection'),
    url(r'^comment/$',views.comment,name='comment'),
    url(r'^updatetoptool/$',views.update_top_tool,name='update_top_tool'),
    url(r'^updatetoppost/$',views.update_top_post,name='update_top_post'),
    url(r'^update/$',views.update,name='update'),
    url(r'^search/$', views.search, name='search'),
	url(r'^admin/', admin.site.urls), 
	url(r'^(?P<topic>[\w ]+)/(?P<subtopic>[\w ]+)/$', views.subtopic, name='subtopic'),
	url(r'^(?P<username>[\w ]+)/(?P<topic>[\w ]+)/(?P<subtopic>[\w ]+)/$', views.subtopic_guest, name='subtopic_guest'),
	url(r'^(?P<username>[\w ]+)/$', views.userprofile, name='userprofile'),
	url('activity/', include('actstream.urls')),

]  +   static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    	#^^^^^^^^^^^NOT TO USE IN PRODUCTION.  SERVE STATIC FILES A DIFFERENT WAY 
# urlpatterns += staticfiles_urlpatterns()