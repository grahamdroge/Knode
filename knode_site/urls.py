from django.urls import path
from . import views 


urlpatterns = [
	# ex: /knode_site/
	path('', views.home, name="home"),
	path('signin', views.signin, name="signin"),
	path('signup', views.signup, name="signup"),
]